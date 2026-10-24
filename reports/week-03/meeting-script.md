# Week 3 validation meeting script

## Context

**Problem space.** Software developers and programming-language learners want targeted, hands-on practice that trains a specific debugging skill, but the existing platforms offer general exercises rather than exercises for a particular kind of debugging problem.

**What we already believe.** The minimum usable product candidate is right: a learner chooses a problem kind, gets a generated exercise, connects their own VS Code, and verifies the fix against a tamper-proof harness. The customer confirmed this direction in Week 2 ([DEC-004](../week-02/meeting-report.md), [DEC-005](../week-02/meeting-report.md)).

**Target.** This meeting settles whether the finished MUP stories do what the customer needs, and what comes next.

## Agenda

1. **Permission questions** (1 min) — may we record, may we publish a sanitized transcript, may we share it privately if publication is refused.
2. **Demo the finished stories** (8 min) — show the working slice: choose a kind, generate, verify, connect VS Code; ask questions 1–3 while each runs.
3. **Stories we will not finish + what comes next** (4 min) — ask questions 4 and 5.
4. **Read-back** (2 min) — read the decisions and action points back to the customer.

Total: ~15 minutes.

## Questions

1. Does the generated exercise for a chosen kind let a learner practice the specific skill they chose? (open)
2. Is the harness's pass/fail verdict a trustworthy signal that the bug is gone? (open)
3. Is attaching from the learner's own installed VS Code the right experience? (closed)
4. Which candidate story, if any, should we not finish by the deadline? (closed)
5. What should come next after the MUP? (open)

## Roles

- **Moderator:** Magel0n
- **Note taker:** Doosuur14
- **Observer:** Tedor49

## Key improvements

1. **Question 4, before:** "What do you think of the candidate?" — **after:** "Which candidate story, if any, should we not finish by the deadline?" — *principle:* name the decision you need instead of asking for a general opinion.
2. **Question 2, before:** "Are the problem kinds in the catalogue the ones a learner would recognize?" — **after:** "Is the harness's pass/fail verdict a trustworthy signal that the bug is gone?" — *principle:* cut a question no answer could change the build for, and keep the one that tests the core signal.
