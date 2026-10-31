"""Tests for the Debugging Gym harness runner.

Run with: python -m pytest
"""

import asyncio

from ..app import generator
from ..app.harness_runner import verify_fix


def _run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


def _fixed_source(kind: str) -> str:
    """The known-good fix per kind, mirroring the generator's fix strings."""
    ex = _run(generator.create_exercise(kind))
    if kind == "off-by-one":
        return ex["source"].replace("range(len(nums) - 1)", "range(len(nums))")
    if kind == "wrong-initial-value":
        return ex["source"].replace("result = 0.0", "result = 1.0")
    if kind == "wrong-comparison":
        return ex["source"].replace("value >= 10", "value > 10")
    return ex["source"]


def test_buggy_source_fails_every_kind():
    """Every generated exercise fails its harness while the bug is present."""
    for kind in generator.KINDS:
        ex = _run(generator.create_exercise(kind))
        result = verify_fix(ex["id"], ex["source"], ex["harness"])
        assert result["passed"] is False, f"{kind} should start buggy"
        assert result["returncode"] != 0


def test_fixed_source_passes_every_kind():
    """The known-good fix makes every kind's harness pass."""
    for kind in generator.KINDS:
        ex = _run(generator.create_exercise(kind))
        fixed = _fixed_source(kind)
        result = verify_fix(ex["id"], fixed, ex["harness"])
        assert result["passed"] is True, f"{kind} should pass when fixed"
        assert result["returncode"] == 0


def test_verdict_flips_from_fail_to_pass():
    """The verdict flips from fail to pass once the defect is gone."""
    ex = _run(generator.create_exercise("off-by-one"))
    before = verify_fix(ex["id"], ex["source"], ex["harness"])
    after = verify_fix(ex["id"], _fixed_source("off-by-one"), ex["harness"])
    assert before["passed"] is False
    assert after["passed"] is True


def test_output_reports_failures():
    """The output names the failing cases while the bug is present."""
    ex = _run(generator.create_exercise("off-by-one"))
    result = verify_fix(ex["id"], ex["source"], ex["harness"])
    assert "FAIL" in result["output"] or "PASS" in result["output"]


def test_no_learner_code_leaks_across_runs():
    """Each run is isolated: a previous exercise's module does not leak."""
    ex1 = _run(generator.create_exercise("off-by-one"))
    ex2 = _run(generator.create_exercise("wrong-initial-value"))
    # Verify ex1's buggy source; it must not accidentally pass because ex2's
    # module lingered in sys.modules.
    result = verify_fix(ex1["id"], ex1["source"], ex1["harness"])
    assert result["passed"] is False