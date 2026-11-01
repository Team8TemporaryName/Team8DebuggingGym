"""Scripted checks for temporary workspace cleanup in the local harness runner.

These tests cover the subprocess-based verifier. They do not prove remote Docker
container cleanup; that separate QR-03 scenario requires the deployed manual test.
"""

from __future__ import annotations

import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

from app import harness_runner


def _record_temporary_directories(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    observed: list[Path] = []
    original_temporary_directory = harness_runner.tempfile.TemporaryDirectory

    @contextmanager
    def recording_temporary_directory(*args, **kwargs):
        with original_temporary_directory(*args, **kwargs) as directory:
            observed.append(Path(directory))
            yield directory

    monkeypatch.setattr(
        harness_runner.tempfile,
        "TemporaryDirectory",
        recording_temporary_directory,
    )
    return observed


def test_verifier_removes_temporary_workspace_after_normal_completion(monkeypatch):
    temporary_directories = _record_temporary_directories(monkeypatch)
    result = harness_runner.verify_fix(
        "cleanup-normal",
        "def answer():\n    return 42\n",
        "from exercise import *\ndef test_true():\n\tassert answer() == 42\n\tprint('PASS')",
    )

    assert result["passed"] is True
    assert len(temporary_directories) == 1
    assert not temporary_directories[0].exists()


def test_verifier_removes_temporary_workspace_when_code_times_out(monkeypatch):
    temporary_directories = _record_temporary_directories(monkeypatch)
    # Shorten only this test's timeout so CI does not spend ten seconds here.
    monkeypatch.setattr(harness_runner, "HARNESS_TIMEOUT_SECONDS", 0.2)

    with pytest.raises(subprocess.TimeoutExpired):
        harness_runner.verify_fix(
            "cleanup-timeout",
            "while True:\n    pass\n",
            "print('This line is not reached')\n",
        )

    assert len(temporary_directories) == 1
    assert not temporary_directories[0].exists()
