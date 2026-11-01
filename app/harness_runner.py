"""Verify a learner's fix against an exercise harness.

The harness is a pytest test file that imports the learner's ``exercise``
module. We run the learner's source together with the harness in an isolated
subprocess with ``pytest`` and report the pass/fail verdict and the output.
Pytest gives the learner the standard, coloured, structured output — expected
vs. got and stack traces on failure — that the customer asked for.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

HARNESS_TIMEOUT_SECONDS = 10


def verify_fix(exercise_id: str, source: str, harness: str) -> dict[str, object]:
    """Run the learner's ``source`` with the exercise's pytest ``harness``.

    Returns a dict with ``passed`` (bool), ``output`` (str), and ``returncode``.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # The learner's program is written as the fixed module name the harness
        # imports from, and the harness is written alongside it.
        program = tmp_path / "exercise.py"
        program.write_text(source, encoding="utf-8")
        (tmp_path / "harness.py").write_text(harness, encoding="utf-8")

        result = subprocess.run(
            ["python", "-m", "pytest", "harness.py", "-q", "--color=yes"],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=HARNESS_TIMEOUT_SECONDS,
        )
        print(result)
        output = result.stdout + result.stderr
    return {
        "exercise_id": exercise_id,
        "passed": result.returncode == 0,
        "returncode": result.returncode,
        "output": output,
    }
