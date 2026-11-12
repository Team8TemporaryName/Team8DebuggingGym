"""API tests for the Debugging Gym web app.

Run with: python -m pytest
"""

from fastapi.testclient import TestClient

from app import store
from app.main import app


def _client() -> TestClient:
    store.TEACHER_KEY = "teacher-demo-key"
    return TestClient(app)


def _teacher_headers() -> dict:
    """A teacher session header, since only teachers can generate (US-016)."""
    session_response = _client().post("/api/auth/teacher", json={"key": "teacher-demo-key"})
    session = session_response.json()["session"]
    return {"x-session": session}


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
    """POST /api/exercises returns a generated exercise (teacher only)."""
    client = _client()
    ex = client.post(
        "/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers()
    ).json()
    assert ex["id"].startswith("ex-")
    assert ex["kind"] == "off-by-one"
    assert ex["source"] and ex["harness"] and ex["task"]


def test_create_exercise_rejects_unknown_kind():
    """POST /api/exercises with an unknown kind returns 400."""
    resp = _client().post("/api/exercises", json={"kind": "no-such"}, headers=_teacher_headers())
    assert resp.status_code == 400


def test_student_cannot_generate():
    """US-016: a student (no session) cannot generate an exercise."""
    resp = _client().post("/api/exercises", json={"kind": "off-by-one"})
    assert resp.status_code == 403


def test_verify_rejects_missing_source():
    """POST /api/exercises/{id}/verify without source returns 400."""
    client = _client()
    ex = client.post(
        "/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers()
    ).json()
    resp = client.post(f"/api/exercises/{ex['id']}/verify", json={})
    assert resp.status_code == 400


def test_verify_unknown_exercise_returns_404():
    """POST /api/exercises/{unknown}/verify returns 404."""
    resp = _client().post("/api/exercises/ex-missing/verify", json={"source": "x"})
    assert resp.status_code == 404


def test_launch_returns_debugpy_config():
    """GET /api/exercises/{id}/launch returns a debugpy attach configuration."""
    client = _client()
    ex = client.post(
        "/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers()
    ).json()
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


def test_learner_id_persists_and_first_visit_is_tracked(monkeypatch):
    from app import main

    events = []

    async def fake_track_event(event_name, learner_id, properties):
        events.append((event_name, learner_id, properties))
        return True

    monkeypatch.setattr(main, "track_event", fake_track_event)

    client = _client()
    first_response = client.get("/")
    second_response = client.get("/")

    assert first_response.cookies.get("dg_learner_id")
    assert (
        first_response.cookies["dg_learner_id"]
        == second_response.cookies["dg_learner_id"]
    )

    visits = [event for event in events if event[0] == "app_opened"]
    assert len(visits) == 2
    assert visits[0][2]["first_visit"] is True
    assert visits[1][2]["first_visit"] is False


def test_exercise_routes_track_analytics_events(monkeypatch):
    from app import main

    events = []

    async def fake_track_event(event_name, learner_id, properties):
        events.append((event_name, learner_id, properties))
        return True

    monkeypatch.setattr(main, "track_event", fake_track_event)

    client = _client()
    # exercise = client.post(
    #     "/api/exercises",
    #     json={"kind": "off-by-one"},
    # ).json()

    exercise = client.post(
    "/api/exercises",
    json={"kind": "off-by-one"},
    headers=_teacher_headers(),
    ).json()

    client.get(f"/api/exercises/{exercise['id']}/launch")

    fixed_source = exercise["source"].replace(
        "range(len(nums) - 1)",
        "range(len(nums))",
    )

    response = client.post(
        f"/api/exercises/{exercise['id']}/verify",
        json={"source": fixed_source},
    )

    assert response.status_code == 200
    assert response.json()["passed"] is True

    event_names = [event[0] for event in events]
    assert "exercise_generated" in event_names
    assert "exercise_started" in event_names
    assert "verification_run" in event_names
    assert "exercise_completed" in event_names

    learner_ids = {event[1] for event in events}
    assert len(learner_ids) == 1


def test_analytics_events_include_valid_sources(monkeypatch):
    from app import main

    events = []

    async def fake_track_event(event_name, learner_id, properties):
        events.append(properties)
        return True

    monkeypatch.setattr(main, "track_event", fake_track_event)

    client = _client()
    # exercise = client.post(
    #     "/api/exercises",
    #     json={"kind": "off-by-one"},
    # ).json()
    exercise = client.post(
    "/api/exercises",
    json={"kind": "off-by-one"},
    headers=_teacher_headers(),
    ).json()

    client.get(f"/api/exercises/{exercise['id']}/launch")

    for properties in events:
        assert properties["source"] in {
            "web",
            "usability-test",
            "smoke",
        }