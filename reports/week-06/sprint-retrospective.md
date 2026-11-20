# Week 6 sprint retrospective

## What Went Well

| What went well |
| --- |
| The team delivered a server-backed exercise flow: teachers can create named exercises, learners can browse and reopen them, verification runs against stored exercises, and completion is recorded per learner. |
| The VS Code extension delivery and the web application were brought closer together, including downloading the extension from the web app and restoring exercise files from the server. |
| Analytics and observability foundations were implemented, with separate staging and production dashboard views captured as repository evidence. |
| The team corrected the scope of the operational signals and produced a passing deployed staging diagnosability check for QR-05 QRT-01, in addition to passing CI checks for QR-02 and local workspace cleanup for QR-03. |
| The customer review produced explicit decisions on the next product direction, including exercise sets, update reconciliation, sandbox research, a survey-based focus metric, and the broader operator–teacher–learner threshold. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| The analytics and observability dashboards could not be demonstrated during the November 9 customer review. | The university VM was not available at the time of the review; the dashboard screenshots and deployed diagnosability test were completed later. |
| The first observability implementation did not consistently measure the quality properties its names suggested: request outcomes were initially treated as availability, and local temporary-workspace cleanup was not remote runtime teardown. | The team checked whether telemetry panels existed before tracing every metric back to the exact quality requirement and its response measure. The follow-up clarified the SLI-03 limitation and kept SLI-04 Planned. |
| Sprint closeout and evidence consolidation drifted beyond the planned deadline. | The team continued implementation and same-sprint rework without a firm closeout checkpoint for the release record, actual velocity, retrospective, AI report, and public report. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Complete the exercise-set assignment flow, teacher edit scope, and student update/reconciliation workflow. | Tedor49 | High | The customer accepted the exercise-set model but the assignment, shared-reference, and update-reconciliation workflows remain follow-up work. | Yes |
| Keep hidden evaluation server-side, plan the second language, and prototype container isolation with per-exercise dependency environments. | Doosuur14 | High | The Week 5 action is not complete; the customer reaffirmed the need for isolation and asked for a container prototype and dependency scaffolding. | Yes |
| Specify the operator/teacher account lifecycle, exercise deletion permissions, learner submission flow, and the teacher CSV export validation contract for TOS-05. | NikitaRUniverse | High | The customer described these as parts of the remaining end-to-end classroom workflow, but the detailed interaction and validation contract are still open. | No |
| Finalize the usability study's satisfaction survey instrument and use its results to settle the focus metric and the remaining TOS-01 measure. | Magel0n | High | The customer selected satisfaction across learners and teachers as the focus metric but deferred its questions, scale, sample, and threshold until usability testing. | No |

## Carried Actions

The Week 5 retrospective predates the explicit `Carried: Yes/No` field, so it did not record carry flags. The actions below reconcile its recorded action list against the Week 6 review outcomes; unresolved actions are re-listed in `## Actions`.

| Action | Outcome |
| --- | --- |
| [`reports/week-05/sprint-retrospective.md#actions`](../week-05/sprint-retrospective.md#actions): “Fix the server-side verify so it runs the full harness and matches the local `pytest` run.” | Done — the review demonstrated local and server verification of the stored exercise, including the completion marker after a successful server verdict. |
| [`reports/week-05/sprint-retrospective.md#actions`](../week-05/sprint-retrospective.md#actions): “Implement pinning of the current exercise's open files, and warn when a folder the server expects is missing or renamed.” | Done — the extension can reopen an exercise from server-stored files after the local directory is removed. |
| [`reports/week-05/sprint-retrospective.md#actions`](../week-05/sprint-retrospective.md#actions): “Move to the top-level git repository decided in `DEC-020`, with per-exercise commit naming.” | Done — the product uses the top-level repository and per-exercise workspace layout recorded in the Week 5 decisions. |
| [`reports/week-05/sprint-retrospective.md#actions`](../week-05/sprint-retrospective.md#actions): “Protect hidden tests on the server (`DEC-022`) and add a second language (`DEC-024`).” | Not done — server-side evaluation remains the direction, while the customer changed the run-time anti-tampering expectation to retained submissions and post-deadline audit; a second language remains deferred. |
| [`reports/week-05/sprint-retrospective.md#actions`](../week-05/sprint-retrospective.md#actions): “Design the packages and the student/teacher separation (`DEC-021`, `DEC-023`).” | Not done — teacher/student access and generation are implemented, but the exercise-set assignment and shared-reference workflow remain outstanding. |
