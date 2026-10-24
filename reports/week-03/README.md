# Week 3 report — Debugging Gym

**Project:** Debugging Gym · **Team number:** 8

> **Problem space.** Software developers and programming-language learners want
> targeted, hands-on practice that trains a specific debugging skill, but the
> existing platforms offer general exercises rather than exercises for a
> particular kind of debugging problem.

## Summary

Week 3 turned the Week 2 candidate into a plan and a working slice. We wrote
the threshold of success, the project plan with its seven sprints and releases,
and the risk register; decided the stack (Python, FastAPI, debugpy-based debug
environments, [DEC-009](../../docs/decisions.md#dec-009)); and defined what done
means in the Definition of Done and the contributing guide. We then built the
minimum usable product on `main`: a learner chooses a problem kind, gets a
generated exercise, connects their own VS Code, and verifies the fix against a
harness. We published the documentation site and the setup page, and cut the
first release, `REL-03`, tagged `v0.1.0`.

The candidate's stories were shown to the customer at the Week 3 meeting and
each received a verdict; the outcome and the customer-meeting details are in
[`meeting-report.md`](meeting-report.md) and [`meeting-transcript.md`](meeting-transcript.md).

## Minimum Usable Product Candidate

Core task: a learner chooses a curated debugging problem from a public gallery,
opens it, and verifies a fix against a non-modifiable harness.

- Candidate stories shown at the meeting: choose a problem kind and get a
  generated exercise; see a catalogue of problem kinds; connect VS Code to the
  exercise environment; verify the fix against the harness.
- The first release is `REL-03`, tagged `v0.1.0`.
- **Re-scoped after the meeting:** the core task moved from "a learner
  generates an exercise for a chosen kind" to "a learner chooses a curated
  problem from a public gallery", because the customer decided only instructors
  generate exercises and students access curated problems
  ([`DEC-010`](../../docs/decisions.md#dec-010),
  [`DEC-011`](../../docs/decisions.md#dec-011)). This re-scopes the first
  sentence of `MLS-03` in [`docs/project-plan.md`](../../docs/project-plan.md).

## Customer-meeting outcome

- The core loop — choose a problem kind, get a generated exercise, edit it, and
  get a pass/fail verdict from a non-modifiable harness — was accepted by the
  customer ("we can assume that the scenario passed").
- The story "a learner generates their own exercise on demand" moved out of the
  candidate: the customer decided only instructors generate, and students use
  curated problems from a public gallery ([`DEC-010`](../../docs/decisions.md#dec-010)).
- The gallery moved from a later extra into a core part of the product
  ([`DEC-011`](../../docs/decisions.md#dec-011)).
- Full detail is in [`meeting-report.md`](meeting-report.md) and
  [`meeting-transcript.md`](meeting-transcript.md).

## Coverage table

| Deliverable | Artifact |
| ----------- | -------- |
| Threshold of success | [`docs/threshold-of-success.md`](../../docs/threshold-of-success.md) |
| Project plan | [`docs/project-plan.md`](../../docs/project-plan.md) |
| Risk register | [`docs/risks.md`](../../docs/risks.md) |
| Stack decision | [`DEC-009`](../../docs/decisions.md#dec-009) in [`docs/decisions.md`](../../docs/decisions.md) |
| Definition of Done | [`docs/definition-of-done.md`](../../docs/definition-of-done.md) |
| Contributing guide | [`CONTRIBUTING.md`](../../CONTRIBUTING.md) |
| Sprint milestones and issue fields | the `SPRINT-03` GitHub milestone, with the `Responsible` and `Accountable` values and the assignees on its issues |
| GitHub project | [the project's table view](https://github.com/orgs/Team8TemporaryName/projects/1) |
| Minimum usable product | the candidate's `US-nn`, merged into `main` and shown at the meeting |
| Changelog and first release | [`CHANGELOG.md`](../../CHANGELOG.md), and the first release `REL-03` (`v0.1.0`) |
| Documentation site | [the site's URL](https://Team8TemporaryName.github.io/Team8DebuggingGym/) |
| Setup and run instructions | [`docs/setup.md`](../../docs/setup.md) |
| Week 2 action points | `## Previous action points` in [`meeting-report.md`](meeting-report.md) |
| Week 2 open questions | `## Previous open questions` in [`meeting-report.md`](meeting-report.md) |
| Meeting script | [`reports/week-03/meeting-script.md`](meeting-script.md) |
| Customer validation | [`reports/week-03/meeting-report.md`](meeting-report.md), and [`meeting-transcript.md`](meeting-transcript.md) when there is one |
| AI usage | [`reports/week-03/ai-usage.md`](ai-usage.md) |

## Repository evidence

| Evidence | Link / location |
| -------- | --------------- |
| A merged pull request that closed its task issue | [Request](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/36) |
| Latest green link check run | [Link check](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/40131702821/job/120984583794) |
| Latest green Markdown check run on `main` | [Markdown check](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/40131702757/job/120984583526) |

## Deviations

None

## Privacy confirmation

No private-only material was committed to this repository.
