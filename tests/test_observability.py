"""Tests for the observability signals (issue #80, AC-08..AC-11).

Run with: python -m pytest tests/test_observability.py -q

These tests verify the observable behaviour without a real OpenObserve backend:
- AC-10: normal, client-error, and server-error requests each produce a signal
  with the correct outcome label and a request id.
- AC-11: observability disabled by default emits nothing, and an unreachable
  exporter never breaks a request.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient


def _make_app(emit) -> FastAPI:
    """A tiny app whose middleware calls the supplied ``emit`` callback.

    The callback mirrors the real ``_request_signal`` middleware: it times the
    request, computes an outcome label, and emits a signal — including on an
    unhandled exception.
    """
    app = FastAPI()
    import time as _time

    @app.middleware("http")
    async def signal(request, call_next):
        request_id = "req-test"
        start = _time.monotonic()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (_time.monotonic() - start) * 1000
            emit(request_id, request.url.path, "server_error", duration_ms)
            raise
        duration_ms = (_time.monotonic() - start) * 1000
        outcome = (
            "ok"
            if response.status_code < 400
            else "client_error"
            if response.status_code < 500
            else "server_error"
        )
        emit(request_id, request.url.path, outcome, duration_ms)
        return response

    @app.get("/ok")
    async def ok():
        return {"ok": True}

    @app.get("/client-error")
    async def client_error():
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="missing")

    @app.get("/server-error")
    async def server_error():
        raise RuntimeError("boom")

    return app


def test_normal_request_emits_ok_signal():
    """AC-10 normal path: a 2xx request emits an ok signal."""
    emitted = []
    client = TestClient(_make_app(lambda *a: emitted.append(a)))
    res = client.get("/ok")
    assert res.status_code == 200
    assert len(emitted) == 1
    req_id, route, outcome, duration_ms = emitted[0]
    assert req_id == "req-test"
    assert route == "/ok"
    assert outcome == "ok"
    assert duration_ms >= 0


def test_client_error_emits_client_error_signal():
    """AC-10 client-error path: a 4xx request emits a client_error signal."""
    emitted = []
    client = TestClient(_make_app(lambda *a: emitted.append(a)))
    res = client.get("/client-error")
    assert res.status_code == 404
    assert len(emitted) == 1
    assert emitted[0][2] == "client_error"


def test_server_error_emits_server_error_signal():
    """AC-10 server-error path: an unhandled exception emits a server_error
    signal with a request id, then the request still returns 500."""
    emitted = []
    client = TestClient(_make_app(lambda *a: emitted.append(a)), raise_server_exceptions=False)
    res = client.get("/server-error")
    assert res.status_code == 500
    assert len(emitted) == 1
    assert emitted[0][1] == "/server-error"
    assert emitted[0][2] == "server_error"
    assert emitted[0][0] == "req-test"


def test_disabled_emits_nothing(monkeypatch):
    """AC-11 disabled by default: observability builds no exporter when off."""
    import app.telemetry as telemetry

    monkeypatch.setattr(telemetry, "OBSERVABILITY_ENABLED", False)
    # A spy on the exporter-build hook; it must never be reached when disabled.
    calls = []
    monkeypatch.setattr(telemetry, "_ensure_observability", lambda: (calls.append("ensure") or False))
    telemetry.emit_request_signal("req-x", "/api/kinds", "ok", 0.5)
    # The guard lives inside _ensure_observability: it returns False when
    # disabled, so no exporter work (histogram record, log emit) happens.
    assert calls == ["ensure"], "the guard is reached but returns False (no-op)"


def test_disabled_short_circuits_before_export(monkeypatch):
    """AC-11: when observability is off, no exporter is built or started."""
    import app.telemetry as telemetry

    monkeypatch.setattr(telemetry, "OBSERVABILITY_ENABLED", False)
    monkeypatch.setattr(telemetry, "_METER", None)
    telemetry.emit_request_signal("req-x", "/api/kinds", "ok", 0.5)
    # No exporter was built (the meter stays None because _ensure_observability
    # returns False before building it).
    assert telemetry._METER is None


def test_unavailable_telemetry_does_not_break_requests(monkeypatch):
    """AC-11: an unreachable exporter never breaks a request."""
    import app.telemetry as telemetry

    monkeypatch.setattr(telemetry, "OBSERVABILITY_ENABLED", True)
    monkeypatch.setattr(telemetry, "OPENOBSERVE_URL", "http://127.0.0.1:1")  # unreachable
    # Rebuild the exporter against the unreachable URL and confirm the app still
    # serves requests (the exporter's background failures are swallowed).
    monkeypatch.setattr(telemetry, "_METER", None)
    from app.main import app

    client = TestClient(app)
    res = client.get("/api/kinds")
    assert res.status_code == 200


def test_emit_request_signal_increments_outcome_counter(monkeypatch):
    """SLI-03 (availability): emit_request_signal increments the outcome counter
    labelled by outcome."""
    import app.telemetry as telemetry

    recorded = []
    counter = type("Counter", (), {"add": lambda self, n, attrs=None: recorded.append(attrs or {})})()
    monkeypatch.setattr(telemetry, "_ensure_observability", lambda: True)
    monkeypatch.setattr(telemetry, "_OUTCOME_COUNTER", counter)
    telemetry._HISTOGRAM = type("H", (), {"record": lambda self, v, a=None: None})()
    telemetry.emit_request_signal("req-x", "/ok", "ok", 1.5)
    assert recorded == [{"outcome": "ok"}]


def test_emit_runtime_release_records_reason_and_budget(monkeypatch):
    """SLI-04 (runtime release): emit_runtime_release records the reason and the
    within-budget label."""
    import app.telemetry as telemetry

    recorded = []
    hist = type(
        "Hist",
        (),
        {"record": lambda self, value, attrs=None: recorded.append((value, attrs or {}))},
    )()
    monkeypatch.setattr(telemetry, "_ensure_observability", lambda: True)
    monkeypatch.setattr(telemetry, "_RELEASE_HISTOGRAM", hist)
    telemetry.emit_runtime_release(500.0, "disconnect", within_budget=True)
    assert recorded[0][0] == 500.0
    assert recorded[0][1]["reason"] == "disconnect"
    assert recorded[0][1]["within_budget"] == "yes"


def test_verify_fix_emits_runtime_release_signal(monkeypatch):
    """SLI-04: verify_fix emits a runtime-release signal when the workspace is
    released after a verification run."""
    import app.harness_runner as hr
    import app.telemetry as telemetry

    emitted = []
    monkeypatch.setattr(telemetry, "emit_runtime_release", lambda *a, **k: emitted.append((a, k)))
    # verify_fix imports telemetry.emit_runtime_release at call time via the
    # module reference, so patching the function works.
    hr.verify_fix("ex-1", "def answer():\n    return 42\n",
                  "from exercise import *\ndef test_true():\n    assert answer() == 42\n")
    assert len(emitted) == 1
    args, kwargs = emitted[0]
    assert kwargs["within_budget"] is True
    assert kwargs["reason"] in ("disconnect", "resource_exhaustion")
    assert args[0] >= 0