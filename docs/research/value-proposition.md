# Value proposition

**Problem space.** Software developers and programming-language learners want
targeted, hands-on practice that trains a specific debugging skill, but the
existing platforms offer general exercises rather than exercises for a
particular kind of debugging problem.

Each `VP-nn` below is a positioning statement that closes at least one `GAP-nn`
(from [`gap-analysis.md`](./gap-analysis.md)), names what it costs, and says
how a competitor would respond. Assumptions are listed at the end.

## VP-01 — "Practice the debugging skill, not the puzzle"

**Statement.** For developers and learners who are weak at a particular kind
of debugging, Debugging Gym is a site that generates an exercise *for that
named problem kind* (null pointer, off-by-one, race, …) and lets them debug it,
so they get targeted reps of the exact skill — unlike CodinGame and LeetCode,
which only train writing correct code.

- **Closes:** GAP-01.
- **What it costs:** we must generate exercises that genuinely contain the
  intended defect and a fair pass condition; a wrong bug or an unsolvable
  exercise is worse than none, so we invest in a validation step.
- **How a competitor responds:** LeetCode adds a "debugging" tag and a few
  curated buggy problems. They can do this — but their catalogue is hand-
  curated and not generated, so the *volume and specificity* (VP-02) is where
  we stay ahead.

## VP-02 — "Fresh exercises on demand, not a fixed set"

**Statement.** For learners who run out of relevant practice, Debugging Gym
generates a *new* exercise for the category they choose, so there is always
another targeted rep — unlike every alternative, whose exercises are fixed and
hand-curated.

- **Closes:** GAP-02.
- **What it costs:** generation quality control. We need a guardrail that
  verifies the generated exercise is solvable and contains the intended bug,
  or the product fails. This is our hardest engineering risk and our core
  differentiator.
- **How a competitor responds:** a platform already using an LLM adds a
  "generate more" button. They can — but only we make the generated exercise
  the *unit of debugging practice in your own IDE* (VP-03), which raises the
  bar for a copied feature.

## VP-03 — "Debug in your own VS Code, not a browser"

**Statement.** For developers who debug with real tools, Debugging Gym lets
them connect from VS Code and debug the generated exercise with their own
breakpoints and stack traces, so the skill transfers to work — unlike the
browser editors of CodinGame and LeetCode, and unlike Rustlings's single
language/toolchain.

- **Closes:** GAP-03.
- **What it costs:** we must run arbitrary user-attached code safely. That
  means container isolation, resource limits, and a Debug Adapter Protocol
  bridge — real security and infra work that a browser-editor competitor does
  not pay.
- **How a competitor responds:** LeetCode's IDE plugin already exists; it
  could host debug sessions. They can — but "host a remote debugging session
  on a generated exercise with grading of the debugging *process*" is a deeper
  integration they have not shipped, and the gallery (below) compounds it.

## VP-04 — "A public gallery of exercises"

**Statement.** For learners who want to browse, Debugging Gym includes a public
gallery of community-generated exercises, so good exercises are discoverable
and reused — which Rustlings and closed platforms lack.

- **Closes:** partly GAP-02 (volume via community) and strengthens VP-01/VP-02
  by making generation cumulative.
- **What it costs:** moderation and quality control of user-contributed
  content; a broken or unsafe gallery entry damages trust and needs curation.
- **How a competitor responds:** anyone can host a gallery. The moat is that
  ours is fed by a working generator with verification, not manual curation.

---

## Assumptions

We are assuming these are true; the kickoff meeting with the customer is where
we test them. Everything below is falsifiable.

| # | Assumption | Why it matters | How we will test it |
|---|-----------|----------------|---------------------|
| A1 | A real audience wants *skill-category* debugging practice, not just general coding practice. | If false, GAP-01 collapses. | Customer kickoff + existing "fix-the-bug" demand signals (candidate list). |
| A2 | Learners will accept connecting their IDE for practice (the setup cost is worth it). | If false, GAP-03 collapses. | Customer kickoff; ask about willingness to set up VS Code. |
| A3 | An LLM can reliably generate exercises that (a) contain the intended bug and (b) are solvable, within our quality budget. | If false, VP-02 and the whole generation premise fail. | Small generation experiment in Week 2; measure defect-presence and solvability rates. |
| A4 | Running user-attached debug sessions safely on a VPS is achievable within our time/security budget. | If false, VP-03 collapses. | Spike on container + DAP bridge in Week 2. |
| A5 | The public gallery is a differentiator worth moderating, not a commodity feature. | If false, drop or de-scope VP-04. | Customer kickoff; compare value of gallery vs. solo generation. |
| A6 | Developers and learners are our single reachable audience; interview-prep candidates are not the focus. | Keeps scope bounded; if the customer disagrees, revisit. | Customer kickoff (explicit disagreement on audience). |

*These assumptions are the risk register for the project. Any the customer
contradicts move to the meeting report's Disagreements table and back here as
changed assumptions.*