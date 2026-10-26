# Week 4 report

**Project:** Debugging Gym
**Team:** 8
**Week:** 4 — Quality, Requirements, Architecture, And The Fourth Release
**Due:** 2026-10-24

## Summary

This week the Debugging Gym product gained the requirements and the architecture behind the MUP built in Week 3: testable quality requirements, a container view, the functional requirements behind the stories, and the architectural decision records, released as `REL-04`.

In response to the Week 3 customer feedback, we also built the first **VS Code extension** (`vscode-extension/`) that brings the choose–generate–verify flow into the learner's editor, and added web-app UX polish the customer asked for: code highlighting, a loading/busy state on the harness run, horizontal scrolling for long output, and a finish button. The extension is recorded as [`FR-006`](../../docs/functional-requirements/fr/FR-006.md) and added to the [container view](../../docs/architecture/README.md#container-view).

- **Release:** [`REL-04`](https://github.com/Team8TemporaryName/Team8DebuggingGym/releases/tag/v0.1.1), tagged v0.1.1.
- **What moved out of the sprint:** nothing

## Customer-meeting outcome

The customer accepted the VS Code extension demo — choose a problem kind, generate an LLM exercise, show the task, and verify the fix all work inside VS Code, and the extension reports pass/fail ("I think this can be closed"). The customer shifted the product firmly to the VS Code extension, deprecated the web app's editable code field in favour of VS Code, and required multi-file exercises ([`DEC-014`](../../docs/decisions.md#dec-014), [`DEC-015`](../../docs/decisions.md#dec-015)). The customer and team agreed learner code runs on the server in sandboxed containers with capped resources ([`DEC-016`](../../docs/decisions.md#dec-016)), that the harness is editable with a server restore and hidden tests ([`DEC-017`](../../docs/decisions.md#dec-017)), that each exercise is its own folder with git versioning ([`DEC-018`](../../docs/decisions.md#dec-018)), and that VS Code settings and language extensions are generated dynamically ([`DEC-019`](../../docs/decisions.md#dec-019)).

The meeting also settled the quality requirements and architecture: the customer judged them "aligned with what I envisioned", asked for wording fixes on the two-minute attach target and the mid-run runtime-release requirement, and noted the VM was still awaited. Full detail is in [`meeting-report.md`](meeting-report.md) and [`meeting-transcript.md`](meeting-transcript.md).

## Coverage table

| Deliverable | Artifact |
| ----------- | -------- |
| Sprint plan and estimates | [`docs/project-plan.md#sprint-04`](../../docs/project-plan.md#sprint-04), with its goal, its planned velocity, and its actual velocity |
| Product backlog refinement | the project's table view grouped by `Milestone` (Sprint milestone); its group with no milestone is the product backlog, and each story there carries `Story Points` |
| Issue catch-up | the issue lists filtered by the `User Story` and `Task` types |
| Quality requirements | [`docs/quality-requirements/qr/`](../../docs/quality-requirements/qr/), with [`docs/quality-requirements/README.md`](../../docs/quality-requirements/README.md) as the priority matrix |
| Functional requirements | [`docs/functional-requirements/`](../../docs/functional-requirements/), with `README.md` as the index and `fr/` for the records |
| Container view | [`docs/architecture/README.md#container-view`](../../docs/architecture/README.md#container-view), its image and source, and `#container-responsibilities` |
| Architecture and drivers | [`docs/architecture/README.md`](../../docs/architecture/README.md), with the drivers it links and the ADR index |
| Architectural decisions | [`docs/architecture/adr/`](../../docs/architecture/adr/) and the ADR index |
| Glossary | [`docs/glossary.md`](../../docs/glossary.md) |
| Team `AGENTS.md` | [`AGENTS.md`](../../AGENTS.md) |
| Issue fields in the project view | the project's table view, with `Responsible`, `Accountable`, `MoSCoW`, `Story Points`, and `Priority` beside the `Assignees` and `Milestone` columns |
| Documentation site | the published site's URL; its navigation links the new quality requirements, functional requirements, architecture, and glossary pages |
| Week 3 action points | [`## Previous action points`](meeting-report.md#previous-action-points) in `reports/week-04/meeting-report.md` |
| Week 3 open questions | [`## Previous open questions`](meeting-report.md#previous-open-questions) in the same report |
| Meeting script | [`reports/week-04/meeting-script.md`](meeting-script.md) |
| Customer validation | [`reports/week-04/meeting-report.md`](meeting-report.md), the transcript when there is one, and each story's verdict |
| `REL-04` | the tag, the changelog's released section, and the plan's `REL-04` line |
| Sprint retrospective | [`reports/week-04/sprint-retrospective.md`](sprint-retrospective.md) |
| AI usage | [`reports/week-04/ai-usage.md`](ai-usage.md) |

## Repository evidence

| Evidence | Link / location |
| -------- | --------------- |
| A merged pull request that closed its task issue | [Pull request](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/45) |
| Latest green link check run | [Link check](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/40405353674/job/121861571269) |
| Latest green Markdown check run on `main` | [Markdown lint](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/40405353964/job/121861574196) |

## What we found out we were wrong about

- We treated the web app's editable code field as a viable second way to solve an exercise; the customer made clear VS Code is the real editor and the editable field is unnecessary, so we deprecated it in favour of the extension ([`DEC-014`](../../docs/decisions.md#dec-014), [`DEC-015`](../../docs/decisions.md#dec-015)).
- We assumed the harness must stay non-modifiable to keep the verdict trustworthy; the customer showed the harness can be editable for learning as long as hidden tests on the server decide the true verdict ([`DEC-017`](../../docs/decisions.md#dec-017)).
- We assumed single-file exercises in the workspace root were enough; the customer wants each exercise in its own folder with automatic git versioning so learners manage and back up their work ([`DEC-018`](../../docs/decisions.md#dec-018)).

## Deviations

- The web-app UX polish item "code highlighting for the program" was not completed for the editable program field: because the customer moved the learner experience to the VS Code extension, we did not add highlighting to the deprecated editable field. Harness highlighting and the rest of the polish were done.
- The gallery and the instructor-only generation flow (Week 3 action point) remain unbuilt: the customer's new decisions this week re-prioritized the extension, multi-file support, sandboxing, and per-exercise versioning, so the gallery work is carried into Week 5.
