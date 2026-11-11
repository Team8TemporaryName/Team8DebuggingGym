"""Tests for the server-side exercise store and the teacher/student interfaces.

Covers US-013 (server-stored exercises), US-014 (teacher access key),
US-015 (teacher generation), US-016 (student browse-only), US-017 (extension
download), and US-019 (progress tracking).
"""

import os

from fastapi.testclient import TestClient

from app import store
from app.main import app


def _client(tmp_db: str) -> TestClient:
    os.environ["DEBUGGING_GYM_DB"] = tmp_db
    # Re-initialise the store module against the temp database.
    store.DB_PATH = tmp_db
    store.TEACHER_KEY = "teacher-demo-key"
    store.init_db()
    return TestClient(app)


def _teacher_headers(client: TestClient) -> dict:
    """A teacher session header, since only teachers can generate (US-016)."""
    session_response = client.post("/api/auth/teacher", json={"key": "teacher-demo-key"})
    session = session_response.json()["session"]
    return {"x-session": session}


def test_generated_exercise_is_stored_and_refetchable(tmp_path):
    """US-013: a generated exercise is persisted and retrievable by id."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    ex = client.post(
        "/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers(client)
    ).json()
    fetched = client.get(f"/api/exercises/{ex['id']}").json()
    assert fetched["id"] == ex["id"]
    assert fetched["kind"] == "off-by-one"
    assert fetched["source"] == ex["source"]
    assert fetched["harness"] == ex["harness"]


def test_list_exercises_returns_stored_exercises(tmp_path):
    """US-016: the library endpoint lists the stored exercises."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    client.post("/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers(client))
    items = client.get("/api/exercises").json()
    assert len(items) == 1
    assert items[0]["id"].startswith("ex-")
    assert items[0]["kind"] == "off-by-one"


def test_teacher_login_with_valid_key(tmp_path):
    """US-014: a valid teacher key returns a teacher session."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    res = client.post("/api/auth/teacher", json={"key": "teacher-demo-key"})
    assert res.status_code == 200
    assert res.json()["role"] == "teacher"
    assert res.json()["session"]


def test_teacher_login_rejects_invalid_key(tmp_path):
    """US-014: an invalid teacher key is rejected."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    assert client.post("/api/auth/teacher", json={"key": "nope"}).status_code == 403


def test_teacher_can_generate_and_store_with_name_and_description(tmp_path):
    """US-015: a teacher stores a named exercise from a prompt."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    session_response = client.post("/api/auth/teacher", json={"key": "teacher-demo-key"})
    session = session_response.json()["session"]
    res = client.post(
        "/api/exercises/teacher",
        headers={"x-session": session},
        json={
            "prompt": "an off-by-one total",
            "name": "My Off-by-one",
            "description": "A demo",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "My Off-by-one"
    assert data["description"] == "A demo"
    # The stored exercise appears in the library with its name.
    items = client.get("/api/exercises").json()
    assert any(i["name"] == "My Off-by-one" for i in items)


def test_teacher_generation_requires_teacher_session(tmp_path):
    """US-016: a non-teacher cannot generate via the teacher endpoint."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    res = client.post(
        "/api/exercises/teacher",
        json={"prompt": "x", "name": "x"},
    )
    assert res.status_code == 403


def test_teacher_generation_rejects_missing_name(tmp_path):
    """US-015: name and prompt are required."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    session_response = client.post("/api/auth/teacher", json={"key": "teacher-demo-key"})
    session = session_response.json()["session"]
    res = client.post(
        "/api/exercises/teacher",
        headers={"x-session": session},
        json={"prompt": "x"},
    )
    assert res.status_code == 400


def test_extension_download_serves(tmp_path):
    """US-017: the extension download endpoint responds."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    res = client.get("/api/extension/download")
    assert res.status_code == 200


def test_completed_exercise_shows_marker(tmp_path):
    """US-019: a passing verify marks the exercise complete for the learner."""
    tmp_db = str(tmp_path / "gym.db")
    client = _client(tmp_db)
    ex = client.post(
        "/api/exercises", json={"kind": "off-by-one"}, headers=_teacher_headers(client)
    ).json()
    # The generated off-by-one program is buggy; verify with a fixed source.
    fixed = ex["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    res = client.post(
        f"/api/exercises/{ex['id']}/verify",
        json={"source": fixed},
        headers={"x-learner": "alice"},
    )
    assert res.json()["passed"] is True
    items = client.get("/api/exercises", headers={"x-learner": "alice"}).json()
    completed = [i for i in items if i["id"] == ex["id"]]
    assert completed and completed[0]["completed"] is True
