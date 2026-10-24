# Product vision

Debugging Gym

## Goal

A learner can choose a named debugging problem kind, receive a generated
exercise (an existing program with a planted defect) for that kind, and debug
it in their own VS Code, proving the fix against a harness.

**Supports:** [VP-01](research/value-proposition.md#vp-01),
[VP-02](research/value-proposition.md#vp-02),
[VP-03](research/value-proposition.md#vp-03).

**Success is:** [the threshold of success](threshold-of-success.md).

## Stakeholders

- **Learner**: the primary user, who debugs an exercise to train a skill, in
  their own environment.
- **Instructor / Customer**: runs the course, decides the scope, and wants to
  see that learners actually improved, ideally with a controlled assessment.
- **Exercise author**: later contributes exercises to the gallery and wants
  their work reused and credited.
- **System operator / team**: owns the VM, the API-key budget, and the
  reliability of generated environments.
- **LLM provider**: supplies generation and the in-environment guide; its cost
  and rate limits constrain us.

## Constraints

### CON-01

The exercise environments run on a university VM with 16 GB RAM and 8 CPUs.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** each exercise environment must be small and bounded, and
  we cannot host many large or long-lived environments for learners at once.
- **Decision:** [DEC-003](decisions.md#dec-003)

### CON-02

The API-key budget is $5–$10.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** we must use cheaper models for prototyping and track spend
  so a learner cannot exhaust a shared key.
- **Decision:** None

### CON-03

The in-environment agent must coach the learner, not solve the exercise.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** we must design the agent's prompt and context so it guides
  without completing the task, which constrains how much it can do.

### CON-04

Every exercise ships as a self-contained, reproducible unit.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** each exercise must carry its program and harness, run in a
  Docker container or NixOS VM, and ideally run locally outside our
  environment too.
- **Decision:** [DEC-003](decisions.md#dec-003)

## Boundary

### BND-01

Host a fixed catalogue of hand-curated problems.

- **Status:** Active
- **Handled by:** LeetCode, CodinGame, HackerRank
- **Why:** we generate exercises on demand instead, so a hand-curated
  catalogue is the alternative model we did not follow.

### BND-02

Run code in a browser editor.

- **Status:** Active
- **Handled by:** LeetCode, CodinGame
- **Why:** the learner debugs in their own IDE, so a browser editor is the
  alternative model we did not follow.

### BND-03

Run mock interviews or human-reviewed debugging sessions.

- **Status:** Active
- **Handled by:** Pramp, Interviewing.io
- **Why:** interview-prep is a different audience from the learners we target,
  per [DEC-002](decisions.md#dec-002).

### BND-04

Host debugging Q&A.

- **Status:** Active
- **Handled by:** Stack Overflow
- **Why:** a learner's answer is the fixed exercise, not a forum post, so
  Q&A is outside.

### BND-05

Teach programming from scratch.

- **Status:** Active
- **Handled by:** MOOC courses and tutorial platforms (Codecademy,
  freeCodeCamp)
- **Why:** we assume the learner already knows the language they practise, per
  [DEC-002](decisions.md#dec-002).

### BND-06

Provide lessons, modules, or certificates.

- **Status:** Active
- **Handled by:** course platforms and universities
- **Why:** we provide practice, not a curriculum.

## System context

> **TODO (team):** add the system context diagram here and its source under
> `docs/architecture/context.<ext>` (e.g. `context.svg`, or a Mermaid/PlantUML
> `.puml` source). The diagram must be embedded in this file as an image that
> GitHub renders, and must agree with the boundary list. A text description
> follows so the diagram and its source stay consistent.

The product sits among the actors and systems it exchanges data with. The
external actors and systems are described in prose here; the diagram draws
them.

- **Learner** interacts with the Debugging Gym web app to choose a problem
  kind and receive an exercise.
- **Debugging Gym web app** hosts the generated exercises, the gallery, and
  the session flow, and talks to the **LLM provider** to generate exercises.
- **Learner's VS Code** connects to the **Exercise runtime** (a container/VM
  on the team's server) over the Debug Adapter Protocol; the runtime runs the
  buggy program and the harness.
- **LLM provider** also powers the **in-environment guide** that coaches the
  learner (CON-03).
- **Instructor / Customer** views learner results (statistics/metrics) from
  the web app.

The boundary holds: the learner's IDE and the LLM provider are external actors,
and the runtime is ours to control. The boundary items hand jobs to LeetCode,
CodinGame, HackerRank, Pramp, Interviewing.io, Stack Overflow, MOOC platforms,
course platforms, and universities; each appears as an external actor or system
on the diagram.

## Where The Detail Lives

- [User stories](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues?q=label%3Auser-story)
- [Week 2 report](../reports/week-02/README.md)
