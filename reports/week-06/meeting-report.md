# Week 6 customer Sprint Review report

## Metadata

- **Date:** 2026-11-09
- **Duration:** ~1 h 48 min
- **Attended:** Magel0n, Tedor49, NikitaRUniverse, Doosuur14, Customer
- **Presented:** server-stored exercises; the teacher access-key interface and exercise generation; learner browsing, downloading, reopening, and solving exercises; and per-user completion markers. The analytics and observability dashboards and the observability QRT were not demonstrated because the university VM was unavailable for the review.
- **Recording:** permitted before recording began.
- **Sanitized transcript publication:** permitted.
- **Private sharing with instructors if publication is refused:** permitted; not needed because the sanitized transcript is published in this repository.
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| ------ | ------- | -------- |
| [Week 5 action points](../week-05/meeting-report.md#action-points): fix server verification so the full harness runs, matching the local run. | Done. The review demonstrated local and server verification of a stored exercise; a successful server verification produced the per-user completion marker. | *None* |
| [Week 5 action points](../week-05/meeting-report.md#action-points): implement pinning of the current exercise's open files in the extension. | Done for the current open/reopen flow. The extension opens an exercise from the server and restores its files after the local directory is removed. A visible update indicator for teacher-published changes is a separate follow-up from this review. | *None* |
| [Week 5 action points](../week-05/meeting-report.md#action-points): warn when an expected folder is missing or renamed, with an option to refetch it. | Done. The review demonstrated deleting the local exercise directory and downloading the stored exercise again from the server. | *None* |
| [Week 5 action points](../week-05/meeting-report.md#action-points): decide the package layout and top-level Git repository with per-exercise commit naming. | Done at the previous review: one top-level repository and visually grouped packages were recorded in DEC-020 and DEC-021. This review clarified that assignment groupings should be exercise sets and that one exercise may be linked from several sets. | [DEC-020](../../docs/decisions.md#dec-020), [DEC-021](../../docs/decisions.md#dec-021), [DEC-030](../../docs/decisions.md#dec-030) |
| [Week 5 action points](../week-05/meeting-report.md#action-points): protect hidden tests with server-side permissions and keep them out of the local harness. | Partly carried forward. Server-side hidden-test protection remains the recorded direction in DEC-022. At this review the customer removed the requirement to make every runtime workaround impossible and agreed that submissions should be retained for post-deadline review instead. | [DEC-022](../../docs/decisions.md#dec-022), [DEC-036](../../docs/decisions.md#dec-036) |
| [Week 5 action points](../week-05/meeting-report.md#action-points): design the exercise library and teacher-assignment flow. | Partly done. Server-stored exercises, teacher access by key, teacher-side generation, learner browsing, extension download, and completion tracking were demonstrated (FR-011–FR-015). Assignment of exercise sets and operator-created accounts remain future work. | [DEC-023](../../docs/decisions.md#dec-023), [DEC-028](../../docs/decisions.md#dec-028), [DEC-030](../../docs/decisions.md#dec-030) |
| [Week 5 action points](../week-05/meeting-report.md#action-points): add at least one language beyond Python. | Not done; multi-language support remains deferred. Exercise-specific dependency environments and teacher-facing scaffolding were discussed, but they do not constitute implementation of a second language. | [DEC-024](../../docs/decisions.md#dec-024), [DEC-034](../../docs/decisions.md#dec-034) |

## Previous open questions

| Question | Answer | Decision |
| -------- | ------ | -------- |
| [Week 5 open questions](../week-05/meeting-report.md#open-questions): what should a package contain? | The customer agreed on an exercise-set concept for grouping exercises for a lab or student group. The same exercise may be linked into multiple sets rather than copied. The detailed assignment interface remains to be worked out. | [DEC-030](../../docs/decisions.md#dec-030) |
| [Week 5 open questions](../week-05/meeting-report.md#open-questions): how do students and teachers authenticate and receive separate interfaces? | The demonstrated implementation uses a teacher access key and a learner browse-and-solve interface. Full teacher/student accounts are a later step; the customer described an operator creating accounts before teachers and students sign in. | [DEC-023](../../docs/decisions.md#dec-023), [DEC-028](../../docs/decisions.md#dec-028) |
| [Week 5 open questions](../week-05/meeting-report.md#open-questions): will the IT department provide the university VM? | The VM was unavailable for this review, so the planned dashboards and observability QRT could not be shown. A later staging execution of QR-05 QRT-01 passed on 2026-11-19; that later evidence does not change what was demonstrated at this meeting. | *None* |

## Summary

- The team demonstrated server-stored exercises, teacher access and generation, learner browsing and downloading, local and server verification, and a completion marker stored per learner.
- The customer asked to restate the learner core-task threshold around the current VS Code extension flow, accepted the verification threshold as achieved under a retained-submission audit model, accepted the initial candidate threshold as achieved, and confirmed documentation reachability.
- The customer added a broader operator–teacher–learner end-to-end threshold and changed the focus metric to satisfaction across learners and teachers, measured through surveys after usability testing.
- The review settled product direction for exercise sets, edit scope, manual update reconciliation, sandbox research, exercise-specific dependencies, a private ground-truth solution, and post-deadline submission review. Deletion permissions and the exact delete interaction were not settled.

## Decisions

- [DEC-027](../../docs/decisions.md#dec-027): Re-scope the learner core task around the current VS Code extension workflow.
- [DEC-028](../../docs/decisions.md#dec-028): Add the operator–teacher–learner end-to-end scenario as TOS-05.
- [DEC-029](../../docs/decisions.md#dec-029): Use user satisfaction across learners and teachers as the focus metric, measured through surveys.
- [DEC-030](../../docs/decisions.md#dec-030): Model assignment groupings as exercise sets with shared exercise references.
- [DEC-031](../../docs/decisions.md#dec-031): Let teachers choose local versus global edit scope; non-authors create a new exercise when editing a public-gallery item.
- [DEC-032](../../docs/decisions.md#dec-032): Show students when an exercise is updated and use a manual update/reconciliation flow that preserves local work.
- [DEC-033](../../docs/decisions.md#dec-033): Research and prototype container-based exercise isolation with a refresh/restart action.
- [DEC-034](../../docs/decisions.md#dec-034): Provide per-exercise dependency environments and teacher-editable exercise scaffolding, including the Dockerfile.
- [DEC-035](../../docs/decisions.md#dec-035): Generate a private ground-truth solution and build the harness against it.
- [DEC-036](../../docs/decisions.md#dec-036): Retain submissions for post-deadline audit rather than require complete run-time anti-tampering.
- [DEC-037](../../docs/decisions.md#dec-037): Use neutral “product user” wording for the documentation-access threshold.

## Action points

| Action | Owner | Due |
| ------ | ----- | --- |
| Re-scope TOS-01, add TOS-05, and update the threshold and analytics documentation to reflect the review decisions. | @Magel0n | Week 7 |
| Research container-based exercise isolation and prototype a run that can be refreshed/restarted; report feasibility and limitations. | @Doosuur14 | Week 7 |

## Open questions

| Question | What it would change | Follow-up |
| -------- | -------------------- | -------- |
| How should a student reconcile local work when a teacher's update is too large for an automatic Git-stash application or produces conflicts? | The manual update/reconciliation flow in DEC-032. | Validate the proposed stash-based flow and document conflict recovery. |
| What is the exact submission flow and what CSV structure or validation contract must teacher exports satisfy? | The submission and export portion of TOS-05. | Refine the flow with the customer before implementation. |
| Should teachers be able to delete server-stored exercises, and if so, who may delete which exercises and how prominent should the action be? | The exercise-library management and deletion interaction. | Confirm the permissions and interaction during exercise-library refinement. |
| How does the operator create, invite, and manage teacher and student accounts? | The authentication and role lifecycle in TOS-05. | Refine the account-creation flow. |
| Which survey questions, scale, sample, and satisfaction threshold will be used for the focus metric? | The measurement definition in DEC-029. | Finalize after the usability test. |
| Which container approach and per-exercise environment model are practical for the supported languages? | The sandbox and dependency decisions in DEC-033 and DEC-034. | Report findings from the Week 7 prototype. |

## Disagreements

| Your position | Customer's position | What you changed |
| ------------- | ------------------- | ---------------- |
| The team considered local sandboxing a lower priority because of implementation complexity and the expectation that teachers would review exercise code. | The customer wanted isolation for reproducibility and to prevent exercise code from modifying files outside its workspace, and asked the team to research or try containers sooner. | The team agreed to research and prototype container-based isolation with a refresh/restart action; a complete production solution was not promised. |
| The team proposed completed exercises per active learner per week as the focus metric. | The customer considered that usage-dependent and unstable after a course ends, and preferred satisfaction across both learners and teachers, measured through surveys. | The focus metric was changed to satisfaction; exact questions and the target will be set after usability testing. |
| The team asked whether updates should propagate automatically or be downloaded manually. | The customer preferred a manual update because automatic propagation could cause merge conflicts and risk students' local work. | The team adopted a visible update indicator and manual reconciliation, with Git stash as the proposed first approach to preserving changes. |
