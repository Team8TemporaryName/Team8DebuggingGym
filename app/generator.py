"""Exercise generation for Debugging Gym.

The MUP slice generates an exercise for a chosen problem kind. Two paths:

- A deterministic, template-based local generator (always available), so the
  slice runs from a clean checkout without an API key and works even when the
  LLM budget or network is unavailable (RISK-02 fallback).
- An LLM path through the provider's OpenAI-compatible API, used when an API
  key is configured, which varies the wording of the generated exercise.

Every generated exercise carries a planted defect that the harness reports as
present, and that a learner's fix turns into a pass.
"""

from __future__ import annotations

import os
import secrets
from typing import Any

import httpx

# The problem kinds in the catalogue. Each kind maps to a template that builds
# a buggy program plus its harness.
KINDS = {
    "off-by-one": {
        "summary": "The code stops one element short of the end of a sequence.",
        "fix": "return total / len(nums)",
    },
    "wrong-initial-value": {
        "summary": "A running total starts at the wrong value, so the result is off by a constant.",
        "fix": "total = 0.0",
    },
    "wrong-comparison": {
        "summary": "A comparison uses the wrong operator, so a boundary case is handled wrongly.",
        "fix": "if value > 10:",
    },
}

LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")

EXERCISES: dict[str, dict[str, Any]] = {}


def _program(kind: str, n: int) -> str:
    """The buggy program template for a kind, parameterised by n."""
    if kind == "off-by-one":
        return f'''"""Exercise: find the bug in ``total``."""


def total(nums):
    """Return the sum of a list of numbers."""
    total = 0.0
    for i in range(len(nums) - 1):
        total += nums[i]
    return total


def average(nums):
    """Return the average of a list of numbers."""
    if not nums:
        return 0.0
    return total(nums) / len(nums)
'''
    if kind == "wrong-initial-value":
        return f'''"""Exercise: find the bug in ``product``."""


def product(nums):
    """Return the product of a list of numbers."""
    result = 0.0
    for value in nums:
        result *= value
    return result
'''
    if kind == "wrong-comparison":
        return f'''"""Exercise: find the bug in ``classify``."""


def classify(value):
    """Return "big" if value is greater than 10, else "small"."""
    if value >= 10:
        return "big"
    return "small"
'''
    raise ValueError(f"unknown kind: {kind}")


def _harness(kind: str) -> str:
    """The harness for a kind: known-good cases and a pass/fail verdict."""
    if kind == "off-by-one":
        cases = [
            ("empty", "average([])", "0.0"),
            ("single", "average([5])", "5.0"),
            ("three", "average([1, 2, 3])", "2.0"),
            ("two", "average([10, 20])", "15.0"),
        ]
    elif kind == "wrong-initial-value":
        cases = [
            ("single", "product([3])", "3.0"),
            ("three", "product([1, 2, 3])", "6.0"),
            ("two", "product([4, 5])", "20.0"),
        ]
    else:  # wrong-comparison
        cases = [
            ("ten", "classify(10)", '"small"'),
            ("eleven", "classify(11)", '"big"'),
            ("minus", "classify(-1)", '"small"'),
        ]

    case_lines = "\n".join(
        f'    ("{label}", lambda: {expr}, {expected}),'
        for label, expr, expected in cases
    )
    return f'''"""Harness for the exercise. Reports pass/fail for each case."""


def check(label, fn, expected):
    actual = fn()
    ok = actual == expected
    print(f"{{'PASS' if ok else 'FAIL'}}: {{label:12s}} expected={{expected!r:10}} got={{actual!r:10}}")
    return ok


CASES = [
{case_lines}
]


def run():
    results = [check(label, fn, expected) for label, fn, expected in CASES]
    print(f"\\n{{sum(results)}}/{{len(results)}} cases passed")
    return all(results)


if __name__ == "__main__":
    import sys

    sys.exit(0 if run() else 1)
'''


def _task_statement(kind: str, n: int) -> str:
    return (
        f"Find and fix the bug in this program. "
        f"The program has a '{kind}' defect: {KINDS[kind]['summary']} "
        f"When you fix it, all harness cases pass."
    )


def _deterministic_exercise(kind: str) -> dict[str, Any]:
    """A deterministic exercise for a kind, guaranteed to work offline."""
    n = secrets.randbelow(1000)
    return {
        "id": f"ex-{secrets.token_hex(4)}",
        "kind": kind,
        "task": _task_statement(kind, n),
        "source": _program(kind, n),
        "harness": _harness(kind),
        "generator": "deterministic",
    }


async def _llm_exercise(kind: str) -> dict[str, Any] | None:
    """Try to generate an exercise through the LLM; return None if unavailable."""
    if not LLM_API_KEY:
        return None
    prompt = (
        f"Write a small Python exercise that has exactly one planted bug of "
        f"kind '{kind}' ({KINDS[kind]['summary']}). Return a JSON object with "
        f"keys 'source' (the buggy program), 'harness' (a runnable harness that "
        f"prints PASS/FAIL per case and exits non-zero while the bug is present), "
        f"and 'task' (one-sentence instruction). Keep it short and self-contained."
    )
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                LLM_ENDPOINT,
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                json={
                    "model": LLM_MODEL,
                    "response_format": {"type": "json_object"},
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            resp.raise_for_status()
            data = resp.json()
        content = data["choices"][0]["message"]["content"]
        import json

        parsed = json.loads(content)
        return {
            "id": f"ex-{secrets.token_hex(4)}",
            "kind": kind,
            "task": parsed.get("task", _task_statement(kind, 0)),
            "source": parsed.get("source", _program(kind, 0)),
            "harness": parsed.get("harness", _harness(kind)),
            "generator": "llm",
        }
    except Exception:
        return None


async def create_exercise(kind: str) -> dict[str, Any]:
    """Create and store an exercise for a kind, LLM first with a local fallback."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind: {kind}")
    exercise = await _llm_exercise(kind) or _deterministic_exercise(kind)
    EXERCISES[exercise["id"]] = exercise
    return exercise