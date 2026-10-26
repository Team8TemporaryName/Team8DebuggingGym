# Week 4 validation meeting script

## Context

**Problem space.** Software developers and programming-language learners want targeted, hands-on practice that trains a specific debugging skill, but the existing platforms offer general exercises rather than exercises for a particular kind of debugging problem.

**What we already believe.** The MUP core loop works, and the customer re-scoped it in Week 3: only instructors generate exercises, students access instructor-curated problems from a public gallery ([DEC-010](../week-03/meeting-report.md), [DEC-011](../week-03/meeting-report.md)), and the product should move toward a VS Code extension ([DEC-012](../week-03/meeting-report.md)). This week we added the requirements and the architecture behind that product, plus the first VS Code extension that brings the choose–generate–verify flow into the learner's editor.

**Target.** This meeting settles whether the quality requirements, the architecture, and the VS Code extension answer the drivers, and what comes next.

## Agenda

1. **Permission questions** (1 min) — may we record, may we publish a sanitized transcript, may we share it privately if publication is refused.
2. **Show the working software** (8 min) — the finished MUP stories, one `AC-nn` at a time; ask for the customer's verdict on each.
3. **Show the VS Code extension** (3 min) — choose a kind, generate an exercise, verify the fix, all inside the editor; ask for the customer's verdict on the extension direction.
4. **Show the requirements and the architecture against the drivers** (6 min) — the quality requirements, the container view, and the ADRs; ask questions 1–4.
5. **Read-back** (2 min) — read the decisions and action points back to the customer.

Total: ~20 minutes.

## Questions

1. Do the quality requirements capture what "good" means for the Debugging Gym, and are the priorities right? (open)
2. Does the container view match how you expect the product to run on the VM? (open)
3. The VS Code extension now covers choose, generate, and verify. Is that the right surface for the extension, or should it also start and attach the debug runtime automatically? (open)
4. Which of the finished stories should we not finish, or should change, by the deadline? (closed)
5. What should come next after the requirements, architecture, and extension are in place? (open)

## Roles

- **Moderator:** Magel0n
- **Note taker:** Doosuur14
- **Observer:** Tedor49

## Key improvements

1. **Question 2, before:** "Is the architecture right?" — **after:** "Does the container view match how you expect the product to run on the VM?" — *principle:* name the concrete artifact (the container view) and the constraint it must fit (the VM) instead of asking for a general opinion on the architecture.
2. **Agenda, before:** three separate show parts — **after:** one working-software part and one requirements-and-architecture part — *principle:* the customer's verdict on each story needs the software shown once, and the review covers requirements and design in one pass, not two.
