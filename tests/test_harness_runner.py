"""Tests for the Debugging Gym harness runner.

Run with: python -m pytest tests/ -q
"""

import asyncio

from app import generator
from app.harness_runner import verify_fix


def _run(coro):
    return asyncio.run(coro)


def _fixed_source(kind: str) -> str:
    """Return a known-good fix for each currently supported problem kind."""
    exercise = _run(generator.create_exercise(kind))
    if kind == "off-by-one":
        return exercise["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    if kind == "wrong-initial-value":
        return exercise["source"].replace("result = 0.0", "result = 1.0")
    if kind == "wrong-comparison":
        return exercise["source"].replace("value >= 10", "value > 10")
    raise ValueError(f"unsupported kind: {kind}")


def test_buggy_source_fails_every_kind():
    """Every generated exercise fails its harness while the bug is present."""
    for kind in generator.KINDS:
        exercise = _run(generator.create_exercise(kind))
        result = verify_fix(exercise["id"], exercise["source"], exercise["harness"])
        assert result["passed"] is False, f"{kind} should start buggy"
        assert result["returncode"] != 0


def test_fixed_source_passes_every_kind():
    """The known-good fix makes every kind's harness pass."""
    for kind in generator.KINDS:
        exercise = _run(generator.create_exercise(kind))
        result = verify_fix(exercise["id"], _fixed_source(kind), exercise["harness"])
        assert result["passed"] is True, f"{kind} should pass when fixed"
        assert result["returncode"] == 0


def test_verdict_flips_from_fail_to_pass():
    """The verdict flips to passing once the defect is removed."""
    exercise = _run(generator.create_exercise("off-by-one"))
    before = verify_fix(exercise["id"], exercise["source"], exercise["harness"])
    after = verify_fix(exercise["id"], _fixed_source("off-by-one"), exercise["harness"])
    assert before["passed"] is False
    assert after["passed"] is True


def test_output_reports_a_verification_result():
    """The runner returns the harness output for learner feedback."""
    exercise = _run(generator.create_exercise("off-by-one"))
    result = verify_fix(exercise["id"], exercise["source"], exercise["harness"])
    assert "FAIL" in result["output"] or "PASS" in result["output"]


def test_no_learner_code_leaks_across_runs():
    """A later exercise does not replace the module under verification."""
    first = _run(generator.create_exercise("off-by-one"))
    second = _run(generator.create_exercise("wrong-initial-value"))
    assert first["id"] != second["id"]
    result = verify_fix(first["id"], first["source"], first["harness"])
    assert result["passed"] is False
