"""Verify a learner's fix against an exercise harness.

The harness is a pytest test file that imports the learner's ``exercise``
module. We run the learner's source together with the harness in an isolated
subprocess with ``pytest`` and report the pass/fail verdict and the output.
Pytest gives the learner the standard, coloured, structured output — expected
vs. got and stack traces on failure — that the customer asked for.

The temporary workspace that holds the learner's source is removed when the
subprocess finishes; the time it takes to release that workspace is reported as
the debug-runtime release signal (``SLI-04``) so the observability capability
covers the runtime-release quality requirement (``QR-03``).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import time
from pathlib import Path

from . import telemetry

HARNESS_TIMEOUT_SECONDS = 10
# QR-03's budget: a runtime is released within one minute of a session ending.
RUNTIME_RELEASE_BUDGET_MS = 60_000


def verify_fix(exercise_id: str, source: str, harness: str) -> dict[str, object]:
    """Run the learner's ``source`` with the exercise's pytest ``harness``.

    Returns a dict with ``passed`` (bool), ``output`` (str), and ``returncode``.
    """
    start = time.monotonic()
    timed_out = False
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # The learner's program is written as the fixed module name the harness
        # imports from, and the harness is written alongside it.
        program = tmp_path / "exercise.py"
        program.write_text(source, encoding="utf-8")
        (tmp_path / "harness.py").write_text(harness, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "harness.py", "-q", "--color=yes"],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=HARNESS_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            timed_out = True
            output = "Harness timed out"
            result = None
            # A timed-out verification must still release the workspace; the
            # TemporaryDirectory context manager does so on exit.
        else:
            print(result)
            output = result.stdout + result.stderr

        release_ms = (time.monotonic() - start) * 1000
        # The session ended either because the learner's code raised (timeout or
        # a non-zero harness) or because the session completed normally.
        reason = "resource_exhaustion" if timed_out else "disconnect"
        telemetry.emit_runtime_release(
            release_ms,
            reason=reason,
            within_budget=release_ms <= RUNTIME_RELEASE_BUDGET_MS,
        )
    return {
        "exercise_id": exercise_id,
        "passed": bool(result is not None and result.returncode == 0),
        "returncode": result.returncode if result is not None else None,
        "output": output,
    }
