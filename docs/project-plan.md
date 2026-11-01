# Project plan

## Milestones

### MLS-03

- **Due:** 2026-10-17
- **Sprints:** [SPRINT-03](#sprint-03)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01), [TOS-02](threshold-of-success.md#tos-02), [TOS-03](threshold-of-success.md#tos-03)

A learner chooses a curated debugging problem from a public gallery, opens it, and verifies a fix against a non-modifiable harness — the candidate's core task, built as one working slice and released as `REL-03`.
This increment also publishes the documentation site and the setup page so the slice is reachable without cloning.

### MLS-05

- **Due:** 2026-10-31
- **Sprints:** [SPRINT-04](#sprint-04), [SPRINT-05](#sprint-05)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01)

A learner completes the core debugging exercise in VS Code: the task is visible in the extension sidebar, the learner can run the local editable harness, and the official verdict is determined by server-side verification tests. The verification service is deployed to staging and production on the university VM and is reachable from the university network.

This increment shifts the learner experience from the web application's editable code field to the VS Code extension while keeping official verification under server control.

### MLS-07

- **Due:** 2026-11-14
- **Sprints:** [SPRINT-06](#sprint-06), [SPRINT-07](#sprint-07)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01)

The in-environment guide helps a stuck learner without solving the exercise: a coached debug session that respects the "coach, do not solve" constraint, and a usability-tested onboarding that a complete beginner can follow.
The increment turns the core task into a guided, measurable learning loop.

## Sprints

### SPRINT-03

A learner can choose a problem kind, get a generated exercise, connect their own VS Code, and verify the fix against the harness.

- **Due:** 2026-10-17
- **Sprint Backlog:** [the issues scheduled into SPRINT-03](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/1)

#### REL-03

### SPRINT-04

The product carries the requirements and the architecture behind the MUP: quality requirements that can be failed, a container view of what the product runs as, functional requirements behind the stories, architectural decision records, and the sprint records behind them, released as `REL-04`.

- **Due:** 2026-10-24
- **Sprint Backlog:** [the issues scheduled into SPRINT-04](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/2)
- **Planned Velocity:** 13
- **Actual Velocity:** 16

#### REL-04

### SPRINT-05

A learner reaches the product through a browser and the product is deployed to a production host, so a learner can return to their practice.

- **Due:** 2026-10-31
- **Sprint Backlog:** [the issues scheduled into SPRINT-05](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/3)
- **Planned Velocity:** 10
- **Actual Velocity:** 10

#### REL-05

### SPRINT-06

The product records a learner's progress after each exercise, so a learner and an instructor can see improvement over time. *(Provisional.)*

- **Due:** 2026-11-07
- **Sprint Backlog:** [the issues scheduled into SPRINT-06](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/4)

#### REL-06

### SPRINT-07

The in-environment guide coaches a stuck learner without solving the exercise, per the "coach, do not solve" constraint. *(Provisional.)*

- **Due:** 2026-11-14
- **Sprint Backlog:** [the issues scheduled into SPRINT-07](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/5)

#### REL-07

### SPRINT-08

The onboarding and first-session flow are usability-tested, so a complete beginner can follow them without frustration. *(Provisional.)*

- **Due:** 2026-11-21
- **Sprint Backlog:** [the issues scheduled into SPRINT-08](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/6)

#### REL-08

### SPRINT-09

The repository is finalised, the pitch is ready, and every supported story is released and documented. *(Provisional.)*

- **Due:** 2026-11-28
- **Sprint Backlog:** [the issues scheduled into SPRINT-09](https://github.com/Team8TemporaryName/Team8DebuggingGym/milestone/7)

#### REL-09

## Progress Monitoring

- **Review:** the team's weekly review, Thursdays at 17:00 before the customer meeting; it reviews [threshold-of-success.md](threshold-of-success.md) and [risks.md](risks.md).
- **Checked by:** the accountable member of each scheduled issue reports its state, and the team walks the sprint backlog against the sprint's goal and the open risks.
- **Visible at:** the [project's table view](https://github.com/orgs/Team8TemporaryName/projects/1) and the sprints' GitHub milestones.
