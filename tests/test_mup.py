"""Tests for the Debugging Gym MUP slice.

Run with: python -m pytest
"""

import asyncio

from app import generator
from app.harness_runner import verify_fix


def _run(coro):
    return asyncio.run(coro)


def test_all_kinds_are_buggy_when_generated():
    """Every generated exercise's harness fails while the bug is present."""
    for kind in generator.KINDS:
        ex = _run(generator.create_exercise(kind))
        result = verify_fix(ex["id"], ex["source"], ex["harness"])
        assert result["passed"] is False, f"{kind} should start buggy"


def test_fixing_off_by_one_passes():
    """Fixing the off-by-one makes the harness pass."""
    ex = _run(generator.create_exercise("off-by-one"))
    fixed = ex["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    result = verify_fix(ex["id"], fixed, ex["harness"])
    assert result["passed"] is True


def test_harness_reports_defect_present_and_absent():
    """The verdict flips from fail to pass once the defect is gone."""
    ex = _run(generator.create_exercise("off-by-one"))
    before = verify_fix(ex["id"], ex["source"], ex["harness"])
    after = verify_fix(
        ex["id"], ex["source"].replace("range(len(nums) - 1)", "range(len(nums))"), ex["harness"]
    )
    assert before["passed"] is False
    assert after["passed"] is True


def test_unknown_kind_rejected():
    """An unknown kind is rejected."""
    try:
        _run(generator.create_exercise("no-such-kind"))
        assert False, "should have raised"
    except ValueError:
        pass


def test_webapp_serves_the_ux_polish_front_end():
    """The web app serves the front end with the Week 4 UX polish: an editable
    editor, a finish button, and a harness-run control."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    index = client.get("/").text
    assert "editor" in index
    assert 'id="finish"' in index
    assert 'id="run-verify"' in index

    js = client.get("/static/app.js").text
    assert "highlightPython" in js
    assert "finishExercise" in js
    assert "Run the harness" in client.get("/").text


def test_webapp_generate_verify_and_launch_flow():
    """The web app API supports choose, generate, verify, and launch."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    kinds = client.get("/api/kinds").json()
    assert "off-by-one" in kinds

    ex = client.post("/api/exercises", json={"kind": "off-by-one"}).json()
    assert ex["id"] and ex["source"] and ex["harness"]

    buggy = client.post(f"/api/exercises/{ex['id']}/verify", json={"source": ex["source"]}).json()
    assert buggy["passed"] is False

    fixed = ex["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    ok = client.post(f"/api/exercises/{ex['id']}/verify", json={"source": fixed}).json()
    assert ok["passed"] is True

    launch = client.get(f"/api/exercises/{ex['id']}/launch").json()
    assert launch["launch_json"]["configurations"][0]["type"] == "debugpy"
