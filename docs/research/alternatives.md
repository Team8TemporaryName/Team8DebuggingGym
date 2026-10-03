# Alternatives research

**Problem space.** Software developers and programming-language learners want
targeted, hands-on practice that trains a specific debugging skill, but the
existing platforms offer general exercises rather than exercises for a
particular kind of debugging problem.

This file documents three alternatives researched for the Debugging Gym
project. They were chosen from the wide candidate list
([`reports/week-01/candidate-list.md`](../../reports/week-01/candidate-list.md))
to cover the required mix:

- **ALT-01** — CodinGame: an adjacent substitute that is closest to
  interactive training.
- **ALT-02** — LeetCode: the generic coding-problem platform developers
  already use; the general baseline.
- **ALT-03** — Rustlings: an open-source, self-hostable "fix the broken code"
  track.

For every claim below we point at what we actually looked at. The working
evidence (screenshots and notes) lives on the shared research board; link it
here once created:

> **Research board (view-only):** *TODO — add link when you create the board.*
> At least two screenshots per alternative of the screens that matter for the
> comparison properties are stored on the board and referenced in the sections
> below.

The properties we compare on were chosen **before** evaluating anything and
are fixed in
[`comparison.md`](./comparison.md):

1. Debugging specificity — does the exercise teach a named debugging skill?
2. Exercise generation — can the platform generate new exercises?
3. User's own environment — can the user debug in their real IDE/editor?
4. Grading/feedback — does the platform tell the user whether they fixed it?
5. Target audience — developers, learners, or interview candidates?
6. Openness/cost — is it open source, self-hostable, and at what price?

---

## ALT-01 — CodinGame

**Type:** adjacent substitute (interactive game-based coding practice).
**URL:** https://www.codingame.com

### Observations (what we looked at)

We browsed the public challenges page, a representative single-player puzzle,
and the free/paid account structure.

- The site organises challenges by theme and difficulty and runs them in the
  browser with a custom game world and feedback loop.
- Each puzzle has a leaderboard; solutions are ranked and time/score based.
- Progress is per-puzzle and account-based; the user writes code in a
  browser editor, not in their own IDE.
- There is no category called "debugging". Puzzles are solved by writing a
  correct program, not by finding a planted bug in a program that almost works.

### Strengths

- Strong, engaging feedback loop (visual game world, instant pass/fail,
  leaderboard) that keeps users practising — a proven engagement model.
- Runs entirely in the browser with no environment setup, lowering the
  barrier to starting a session.

### Weaknesses

- **Not debugging-specific:** a puzzle is "write a program that passes",
  never "find and fix the defect in this existing program". It cannot target a
  named debugging skill such as reading a stack trace or narrowing a crash.
- **No exercise generation:** all exercises are hand-curated and fixed; there
  is no way to request exercises for a particular problem category.
- **No real environment:** the user debugs in a browser editor, not their own
  IDE, so skills do not transfer to the tools they actually use at work.

### Why it matters for us

CodinGame proves the engagement model (gamified, immediate feedback, public
gallery/leaderboard) but is the wrong *content model*: it does not train
debugging and does not let users work in their own environment. Our project
adopts the engagement model and inverts the content model (existing, broken
code instead of fresh code), and the environment (the user's IDE instead of a
browser).

---

## ALT-02 — LeetCode

**Type:** adjacent substitute / general baseline (the coding-problem platform
developers already use).
**URL:** https://leetcode.com

### Observations (what we looked at)

We reviewed the problem-set structure, the editor/runner, and the study-plan
features visible without an account.

- Problems are described by topic tags (arrays, dynamic programming, …) and
  difficulty; the user submits a solution and gets pass/fail against hidden
  tests.
- The user writes and runs code in a web editor (or via a paid CLI / in-editor
  plugin in newer plans), with test cases shown for failures.
- There are free and paid tiers; paid features include more problems,
  company-tagged problems, and some AI hints.
- There is no debugging category or mode. When a submission fails, the user
  sees which test failed but is not guided to *debug* their code methodically.

### Strengths

- Huge, familiar catalogue with topic tagging and difficulty levels — the
  standard the market expects for "practice by category".
- Clear, immediate feedback: hidden test cases give an objective pass/fail
  signal.

### Weaknesses

- **Debugging is incidental, not taught:** a failing submission is a score to
  improve, not an exercise about a debugging skill. Nothing trains reading
  stack traces, using breakpoints, or isolating a regression.
- **No user environment by default:** debugging happens in a web editor; the
  IDE plugins are an afterthought and not the point of the platform.
- **No exercise generation:** the catalogue is fixed and curated; users
  choose from what exists, they cannot generate exercises for a chosen kind of
  problem.

### Why it matters for us

LeetCode is the audience default ("I practice coding problems there"), so it
is the natural benchmark users will compare us against for *category selection*
and *pass/fail feedback*. It demonstrates a gap: nothing in the catalogue maps
to "train the skill of debugging X". It also confirms users are used to
practising by topic — which validates our "choose a problem category" idea.

---

## ALT-03 — Rustlings

**Type:** open-source, self-hostable "fix the broken code" track.
**URL:** https://github.com/rustlings/rustlings

### Observations (what we looked at)

We looked at the repository README, the exercise directory layout, and how the
exercises are structured and checked.

- Rustlings is a set of small Rust exercises, each a file that intentionally
  does not compile or fails a test; the user edits the file until it compiles
  and passes.
- It runs locally (`rustlings watch`), so the user edits in their own editor
  and uses their local toolchain. It is free and open source (MIT).
- Exercises are grouped by topic directories (variables, functions, traits,
  errors, …) and the runner gives hints and checks the result.
- The content is hand-written and fixed; there is no generator and no
  web/gallery component. It is Rust-only.

### Strengths

- **Most direct precedent for "fix the broken code":** the whole model is
  "a file is wrong, make it right" — closer to a debugging exercise than any
  generic platform above.
- **Runs in the user's own environment and editor**, with local toolchain, and
  is fully open source and self-hostable (MIT).

### Weaknesses

- **Single language and toolchain:** Rust-only, tied to `cargo`/`rustc`.
  It cannot cover the breadth of problem kinds a debugging trainer needs.
- **No exercise generation and no feedback grading beyond compile/test:** the
  set is fixed, and the "answer" is binary (it compiles / the test passes)
  with no analysis of *how* the learner debugged it.
- **No gallery or sharing:** exercises stay on your machine; there is no
  public collection to browse.

### Why it matters for us

Rustlings is the strongest evidence for both the opportunity and the
constraints. It shows that "fix the broken program in your own editor" is an
enjoyable, effective learning model and is feasible to build open source. It
also shows exactly where that model stops: fixed content, one language, no
generation, no gallery. Our project is, in effect, "Rustlings generalised":
LLM-generated exercises for many problem kinds, debugged in the user's own
VS Code, with a shared public gallery.

---

## Research board

[Link to research board](https://www.figma.com/design/7bwb24mxusLGMo43t5VsVH/Untitled)

---

*Researched: 2026-10-01. Search recorded in
[`reports/week-01/candidate-list.md`](../../reports/week-01/candidate-list.md).*