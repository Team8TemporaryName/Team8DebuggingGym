"""Run the browser frontend's Node.js tests as part of the clean-checkout suite."""

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_TEST = ROOT / "tests" / "test_frontend.cjs"


def test_frontend_behavior_with_node():
    """The JavaScript frontend tests must pass as part of the full pytest suite."""
    node = shutil.which("node")
    assert node is not None, (
        "Node.js 22 or newer is required to run tests/test_frontend.cjs; "
        "install it as documented in docs/setup.md."
    )
    result = subprocess.run(
        [node, "--test", str(FRONTEND_TEST)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"Frontend tests failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
