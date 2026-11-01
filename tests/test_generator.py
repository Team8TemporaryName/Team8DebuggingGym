"""Tests for the Debugging Gym exercise generator.

Run with: python -m pytest tests/ -q
"""

import asyncio

from app import generator


def _run(coro):
    return asyncio.run(coro)


def test_catalogue_has_all_expected_kinds():
    """The catalogue exposes the problem kinds the product documents."""
    assert set(generator.KINDS) >= {
        "off-by-one",
        "wrong-initial-value",
        "wrong-comparison",
    }
    for kind in generator.KINDS:
        assert generator.KINDS[kind]["summary"]


def test_generated_exercise_has_all_parts():
    """A generated exercise carries an id, kind, task, source, and harness."""
    exercise = _run(generator.create_exercise("off-by-one"))
    for field in ("id", "kind", "task", "source", "harness", "generator"):
        assert field in exercise, f"missing {field}"
    assert exercise["kind"] == "off-by-one"
    assert exercise["id"].startswith("ex-")
    assert exercise["generator"] in {"deterministic", "llm"}


def test_deterministic_fallback_works_without_llm_key():
    """The deterministic path works when no LLM key is configured."""
    old_key = generator.LLM_API_KEY
    try:
        generator.LLM_API_KEY = ""
        exercise = _run(generator.create_exercise("off-by-one"))
        assert exercise["generator"] == "deterministic"
        assert exercise["source"]
        assert exercise["harness"]
    finally:
        generator.LLM_API_KEY = old_key


def test_exercises_are_not_identical_for_same_kind():
    """Two exercises for the same kind have different ids."""
    first = _run(generator.create_exercise("off-by-one"))
    second = _run(generator.create_exercise("off-by-one"))
    assert first["id"] != second["id"]


def test_each_kind_has_a_pytest_harness():
    """Every kind's harness is a pytest file importing the learner's module."""
    for kind in generator.KINDS:
        harness = generator._harness(kind)
        assert "from exercise import *" in harness
        assert harness.count("def test_") >= 3
        assert "pytest" in harness


def test_unknown_kind_rejected():
    """An unknown kind is rejected with ValueError."""
    try:
        _run(generator.create_exercise("no-such-kind"))
    except ValueError:
        pass
    else:
        raise AssertionError("unknown kind should have raised ValueError")
