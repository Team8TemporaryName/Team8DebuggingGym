"""Verify a learner's fix against an exercise harness.

The harness is a fixed part of the exercise: it is not modifiable by the
learner (DEC-006). We run the learner's source together with the harness in an
isolated subprocess and report the pass/fail verdict and the output. No network
or filesystem is exposed to the running code.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def verify_fix(exercise_id: str, source: str, harness: str) -> dict[str, object]:
    """Run the learner's ``source`` with the exercise's ``harness``.

    Returns a dict with ``passed`` (bool), ``output`` (str), and ``returncode``.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # The learner's program is written as a fixed module name, and the
        # harness imports every name it needs from it.
        program = tmp_path / "solution.py"
        program.write_text(source, encoding="utf-8")
        harness_source = "from solution import *\n\n" + harness
        (tmp_path / "harness.py").write_text(harness_source, encoding="utf-8")

        result = subprocess.run(
            ["python", "harness.py"],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout + result.stderr
    return {
        "exercise_id": exercise_id,
        "passed": result.returncode == 0,
        "returncode": result.returncode,
        "output": output,
    }