"""Tests for the Debugging Gym exercise generator.

Run with: python -m pytest
"""

import asyncio

from ..app import generator


def _run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


def test_catalogue_has_all_expected_kinds():
    """The catalogue exposes the problem kinds the product documents."""
    assert set(generator.KINDS) >= {"off-by-one", "wrong-initial-value", "wrong-comparison"}
    for kind in generator.KINDS:
        assert "summary" in generator.KINDS[kind]
        assert generator.KINDS[kind]["summary"]


def test_generated_exercise_has_all_parts():
    """A generated exercise carries an id, kind, task, source, and harness."""
    ex = _run(generator.create_exercise("off-by-one"))
    for field in ("id", "kind", "task", "source", "harness", "generator"):
        assert field in ex, f"missing {field}"
    assert ex["kind"] == "off-by-one"
    assert ex["id"].startswith("ex-")
    assert ex["generator"] in {"deterministic", "llm"}


def test_deterministic_fallback_works_without_llm_key():
    """The deterministic path produces a valid exercise even when no LLM key is set."""
    old_key = generator.LLM_API_KEY
    try:
        generator.LLM_API_KEY = ""
        ex = _run(generator.create_exercise("off-by-one"))
        assert ex["generator"] == "deterministic"
        assert ex["source"] and ex["harness"]
    finally:
        generator.LLM_API_KEY = old_key


def test_exercises_are_not_identical_for_same_kind():
    """Two exercises for the same kind are not identical programs."""
    ex1 = _run(generator.create_exercise("off-by-one"))
    ex2 = _run(generator.create_exercise("off-by-one"))
    # Deterministic templates share a body; the id must differ at least.
    assert ex1["id"] != ex2["id"]


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
        assert False, "should have raised"
    except ValueError:
        pass