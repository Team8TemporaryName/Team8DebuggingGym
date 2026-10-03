# Gap analysis

**Problem space.** Software developers and programming-language learners want
targeted, hands-on practice that trains a specific debugging skill, but the
existing platforms offer general exercises rather than exercises for a
particular kind of debugging problem.

Every gap below must pass all four tests from the process requirements:

1. **Somebody needs it** — there is a real user whose pain it removes.
2. **The alternatives do not serve it** — traced back to a comparison cell.
3. **It is reachable** — the technology exists and is feasible.
4. **A team of 3–4 could build it in this course** — the scope is bounded.

Each accepted gap gets a `GAP-nn` id. We also record the gaps we **rejected**
and why — that list is not optional; it is what the customer will argue with.

## Accepted gaps

### GAP-01 — No practice aimed at a named debugging skill

- **What:** There is no mainstream way to train *a particular debugging skill*
  (read a stack trace, isolate a null-pointer crash, bisect a regression,
  debug a race) as the point of the exercise, the way CodinGame/LeetCode train
  *algorithms*.
- **Test 1 (somebody needs it):** Developers and learners repeatedly hit the
  same failure kinds and want targeted reps, not another "write correct code"
  puzzle. The wide candidate list shows debugging practice only ever appears
  incidentally in other platforms (candidate-list).
- **Test 2 (alternatives do not serve it):** Comparison row 1: CodinGame and
  LeetCode have no debugging category; Rustlings's "broken file" is debugging-
  shaped but Rust-only and compile/test only.
- **Test 3 (reachable):** A generator can produce broken programs from a
  problem category; auto-checking a defect is a test the user's code must
  pass.
- **Test 4 (buildable):** One category + one language is a bounded first
  scope; the mechanics (generate, serve, check) are standard.
- **Cost if we build it:** the LLM-generated exercises must actually contain
  the intended bug and a fair pass condition; garbage exercises would destroy
  trust.

### GAP-02 — No generation of fresh exercises on demand

- **What:** Every alternative has a fixed, hand-curated set. Users cannot ask
  for *a new exercise for a category they choose*; once they finish the set
  there is nothing new.
- **Test 1:** The learner's bottleneck is volume and specificity — enough
  targeted reps for the skill they are currently weak on.
- **Test 2:** Comparison row 2: no alternative generates exercises.
- **Test 3:** LLM generation of code with an injected defect is feasible
  today; the hard part is verifying the defect is present and the exercise is
  solvable, which is a validation step we can build.
- **Test 4:** Generation + a validation guardrail is a well-scoped component.
- **Cost:** generation quality control; a generated exercise that is broken in
  the wrong way (or unsolvable) is a worse product than no exercise.

### GAP-03 — No debugging practice in the user's own IDE

- **What:** Developers debug with their real tools (VS Code breakpoints,
  stack traces, watch). Alternatives make users debug in a browser editor or a
  single fixed toolchain, so the skill does not transfer.
- **Test 1:** Learners want to train the exact workflow they use at work; a
  browser editor teaches habits they then must unlearn.
- **Test 2:** Comparison row 3: only Rustlings runs in the user's environment,
  and it is Rust-only.
- **Test 3:** VS Code + Debug Adapter Protocol (DAP) makes "connect to a
  remote exercise and debug it locally" a solved, standards-based problem.
- **Test 4:** A container that hosts the exercise and a DAP bridge is a
  bounded, buildable feature for one editor first.
- **Cost:** running arbitrary user code and letting them attach a debugger is
  a security/isolation problem that needs a real answer (containers, timeouts,
  resource limits).

## Rejected gaps (and why)

| Rejected gap | Why we rejected it |
|--------------|--------------------|
| **A full debugging curriculum / course** (modules, lessons, certificates). | Scope is too large and it competes with MOOC-style courses (C02/C05/C06/C16 in the candidate list) that already do curricula well. Our alternatives research found no demand for *us* being a school; the pain is targeted practice, not more courseware. |
| **Debugging interview-prep platform** (human-reviewed mock sessions). | Pramp/Interviewing.io already own interview prep (C07/C08). It requires expensive human grading and a different audience; it does not close a gap the alternatives leave open. |
| **A community forum / Q&A for debugging questions.** | Stack Overflow et al. already serve Q&A. No defensible gap; would dilute our focus. |
| **Generic "fix-the-bug" gamified arcade with no skill targeting.** | It is just CodinGame with a bug theme; it does not satisfy the *named debugging skill* requirement and adds no differentiation. |
| **Multi-language support from day one.** | Feasible later, but a 3–4 team cannot isolate many language runtimes well in Week 1 scope; single/major-language first (aligned with GAP-03) is the reachable slice. We prefer to do one language well. |

## Summary

The three accepted gaps are the same theme viewed from three angles — *content*
(a named debugging skill), *volume* (generation on demand), and *environment*
(your own IDE). They are mutually reinforcing: you cannot have targeted,
fresh, in-your-IDE debugging practice unless you solve all three together,
which is exactly why no single alternative already covers it. The rejected
list shows we deliberately did not grab at curriculum, interview prep, forums,
or gamification-only.

The next file, [`value-proposition.md`](./value-proposition.md), turns these
gaps into positioning statements.