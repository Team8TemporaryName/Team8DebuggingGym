# Week 5 validation meeting script

## Context

**Problem space.** Software developers and programming-language learners want targeted, hands-on practice that trains a specific debugging skill, but existing platforms offer general exercises rather than exercises for a particular kind of debugging problem.

**What we already believe.** The MUP core loop works, the customer confirmed the VS Code extension is the primary learner surface, and the product must run learner code in sandboxed containers. This week we made the product deployable: an expanded automated test suite, quality requirement tests, and a self-hosted production stack that the university VM will replace.

**Target.** This meeting settles whether the deployed product and its tests answer the drivers, and what comes next.

## Agenda

1. **Permission questions** (1 min) — may we record, may we publish a sanitized transcript, may we share it privately if publication is refused.
2. **Show the deployed product** (8 min) — the running stack, the tests, and the CI; ask for the customer's verdict on the deployable state.
3. **Show the quality requirement tests** (5 min) — the `QRT-nn` sections and the testing plan; ask questions 1–2.
4. **Read-back** (2 min) — read the decisions and action points back to the customer.

Total: ~16 minutes.

## Questions

1. Does the deployed product give the learner the practice loop the customer expects, and is a self-hosted instance (until the VM) acceptable? (open)
2. Are the quality requirement tests the right checks for "good", and are the priorities right? (open)
3. What should come next after the product is deployable? (open)

## Roles

- **Moderator:** Magel0n
- **Note taker:** Doosuur14
- **Observer:** Tedor49

## Key improvements

1. **Agenda, before:** show the tests and the deployment as two parts — **after:** one deployed-product part and one tests part — *principle:* the customer's verdict on the product comes first from seeing it running, then from the checks that keep it correct.
2. **Question 1, before:** "Is the deployment done?" — **after:** "Does the deployed product give the learner the practice loop, and is a self-hosted instance acceptable?" — *principle:* ask about the outcome the deployment serves, and the fallback the team is actually using, rather than asking for a status report.
