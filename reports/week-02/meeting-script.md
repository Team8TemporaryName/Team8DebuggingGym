# Week 2 validation meeting script

## Context

Our problem-space sentence: software developers and programming-language
learners want targeted, hands-on practice that trains a specific debugging
skill, but the existing platforms offer general exercises rather than
exercises for a particular kind of debugging problem.

We believe the prototype, the boundary, and the minimum usable product
candidate are right, and that debugging in the learner's own VS Code is the
riskiest part to get working (DEC-001).

Target: settle whether the prototype, the boundary, and the minimum usable
product candidate are right.

## Agenda

1. Permission questions (2 min).
   Show: nothing.
2. The prototype (12 min).
   Show: [the prototype record](prototypes.md).
   Questions 1–3.
3. The boundary (8 min).
   Show: [the product vision](../../docs/product-vision.md).
   Questions 4–5.
4. The minimum usable product candidate (8 min).
   Show: the candidate in [the week report](README.md#minimum-usable-product-candidate)
   and the [user-story issue list](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues?q=label%3Auser-story).
   Questions 6–8.
5. Read back the decisions and action points (2 min).
   Show: the note taker's list.

## Questions

1. _(open)_ When you attach VS Code and hit that breakpoint, is this the setup
   a learner would accept? What is the sticking point?
2. _(open)_ What would make you trust the harness's pass/fail signal?
3. _(closed)_ Is debugging in the user's own VS Code still the right first
   priority given what the prototype shows?
4. _(open)_ Which boundary item is wrong, and who should actually do that job?
5. _(closed)_ Is "we do not teach complete beginners" (BND-05) right, or should
   beginners be a target after all?
6. _(open)_ If we can only build the candidate's stories, can a learner
   complete the core task? What is missing?
7. _(open)_ Which story would you pull out of the candidate, and which would
   you add?
8. _(closed)_ Is this your verdict on the candidate?

## Roles

Interviewer — Magel0n; note taker — Doosuur14; observer — Tedor49.

## Key improvements

### "Do you think learners would like debugging in their own IDE?" -> "When you attach VS Code and hit that breakpoint, is this the setup a learner would accept? What is the sticking point?"

The original tested a belief, not the thing we built, and invited agreement.
The rewrite anchors the question to the actual prototype in front of the
customer, so the answer is a reaction to the real thing and surfaces an
objection we did not predict.

### "Which of our boundary items do you agree with?" -> "Which boundary item is wrong, and who should actually do that job?"

The original invited agreement and cost the customer nothing.
The rewrite forces them to name a specific item to drop and an owner, so they
have to give something up; a boundary nobody contests is one we wrote for
ourselves, and the value of the question is a disagreement.
