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
    """The harness for a kind as a pytest script.

    Using pytest gives a learner the standard, coloured output the customer
    asked for (expected vs. got, and stack traces on failure) through the same
    testing framework they would use on real code. The harness imports every
    name it needs from the learner's ``exercise`` module. The learner may edit
    this file (DEC-017); the server's hidden tests still decide the true
    verdict.
    """
    if kind == "off-by-one":
        cases = [
            ("test_average_empty", "average([])", "0.0"),
            ("test_average_single", "average([5])", "5.0"),
            ("test_average_three", "average([1, 2, 3])", "2.0"),
            ("test_average_two", "average([10, 20])", "15.0"),
        ]
    elif kind == "wrong-initial-value":
        cases = [
            ("test_product_single", "product([3])", "3.0"),
            ("test_product_three", "product([1, 2, 3])", "6.0"),
            ("test_product_two", "product([4, 5])", "20.0"),
        ]
    else:  # wrong-comparison
        cases = [
            ("test_classify_ten", "classify(10)", '"small"'),
            ("test_classify_eleven", "classify(11)", '"big"'),
            ("test_classify_minus", "classify(-1)", '"small"'),
        ]

    test_lines = "\n".join(
        f'''
def {name}():
    assert {expr} == {expected}
'''
        for name, expr, expected in cases
    )
    return f'''"""Harness for the exercise, written as a pytest test file.

The learner may edit this file (DEC-017); the server's hidden tests still
decide the true verdict. Run it locally with:

    python -m pytest harness.py -q

"""

from exercise import *  # noqa: F401,F403  (the learner's module)
{test_lines}'''


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
        f"keys 'source' (the buggy program), 'harness' (a pytest test file that "
        f"imports everything it needs from the learner's 'exercise' module with "
        f"'from exercise import *', with one 'def test_...():' function per case "
        f"using plain asserts), and 'task' (one-sentence instruction). Keep it "
        f"self-contained. The harness runs under pytest. Aim for 10 lines of "
        f"code in the source, other fields can be any length. Keep comments to "
        f"a minimum."
    )
    try:
        import json
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                LLM_ENDPOINT,
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                data=json.dumps({
                    "model": LLM_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                }),
            )
            print(resp.content)
            resp.raise_for_status()
            data = json.loads(resp.content)
        content = data["choices"][0]["message"]["content"]

        parsed = json.loads(content)
        return {
            "id": f"ex-{secrets.token_hex(4)}",
            "kind": kind,
            "task": parsed.get("task", _task_statement(kind, 0)),
            "source": parsed.get("source", _program(kind, 0)),
            "harness": parsed.get("harness", _harness(kind)),
            "generator": "llm",
        }
    except Exception as e:
        print(e)
        return None


async def create_exercise(kind: str) -> dict[str, Any]:
    """Create and store an exercise for a kind, LLM first with a local fallback."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind: {kind}")
    exercise = await _llm_exercise(kind) or _deterministic_exercise(kind)
    EXERCISES[exercise["id"]] = exercise
    return exercise