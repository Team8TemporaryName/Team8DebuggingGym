"""API tests for the Debugging Gym web app.

Run with: python -m pytest
"""

from fastapi.testclient import TestClient

from app.main import app


def _client() -> TestClient:
    return TestClient(app)


def test_root_serves_the_front_end():
    """The root route serves the front end with the choose/verify controls."""
    client = _client()
    html = client.get("/").text
    assert "Debugging Gym" in html
    assert 'id="run-verify"' in html
    assert 'id="finish"' in html
    assert 'id="editor"' in html


def test_kinds_returns_the_catalogue():
    """GET /api/kinds returns the problem kinds with summaries."""
    kinds = _client().get("/api/kinds").json()
    assert "off-by-one" in kinds
    assert "summary" in kinds["off-by-one"]


def test_create_exercise_returns_a_valid_exercise():
    """POST /api/exercises returns a generated exercise."""
    ex = _client().post("/api/exercises", json={"kind": "off-by-one"}).json()
    assert ex["id"].startswith("ex-")
    assert ex["kind"] == "off-by-one"
    assert ex["source"] and ex["harness"] and ex["task"]


def test_create_exercise_rejects_unknown_kind():
    """POST /api/exercises with an unknown kind returns 400."""
    resp = _client().post("/api/exercises", json={"kind": "no-such"})
    assert resp.status_code == 400


def test_verify_rejects_missing_source():
    """POST /api/exercises/{id}/verify without source returns 400."""
    client = _client()
    ex = client.post("/api/exercises", json={"kind": "off-by-one"}).json()
    resp = client.post(f"/api/exercises/{ex['id']}/verify", json={})
    assert resp.status_code == 400


def test_verify_unknown_exercise_returns_404():
    """POST /api/exercises/{unknown}/verify returns 404."""
    resp = _client().post("/api/exercises/ex-missing/verify", json={"source": "x"})
    assert resp.status_code == 404


def test_launch_returns_debugpy_config():
    """GET /api/exercises/{id}/launch returns a debugpy attach configuration."""
    client = _client()
    ex = client.post("/api/exercises", json={"kind": "off-by-one"}).json()
    launch = client.get(f"/api/exercises/{ex['id']}/launch").json()
    conf = launch["launch_json"]["configurations"][0]
    assert conf["type"] == "debugpy"
    assert conf["request"] == "attach"
    assert "connect" in conf


def test_launch_unknown_exercise_returns_404():
    """GET /api/exercises/{unknown}/launch returns 404."""
    resp = _client().get("/api/exercises/ex-missing/launch")
    assert resp.status_code == 404


def test_static_app_js_served():
    """The front-end bundle is served."""
    js = _client().get("/static/app.js").text
    assert "highlightPython" in js
    assert "finishExercise" in js


def test_generic_verify_with_harness():
    """POST /api/verify verifies a source against an explicit harness.

    This lets a learner reopen a saved exercise whose id is no longer in the
    server's memory (feedback point 4).
    """
    import asyncio

    from app import generator

    ex = asyncio.new_event_loop().run_until_complete(generator.create_exercise("off-by-one"))
    client = _client()
    buggy = client.post(
        "/api/verify", json={"source": ex["source"], "harness": ex["harness"]}
    ).json()
    assert buggy["passed"] is False

    fixed = ex["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    ok = client.post("/api/verify", json={"source": fixed, "harness": ex["harness"]}).json()
    assert ok["passed"] is True


def test_generic_verify_requires_harness():
    """POST /api/verify rejects a missing harness."""
    resp = _client().post("/api/verify", json={"source": "x"})
    assert resp.status_code == 400
