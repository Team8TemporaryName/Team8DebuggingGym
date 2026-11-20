# Week 6 report — Product Review, Analytics, And Thresholds

**Project:** Debugging Gym · **Team:** 8 · **Week:** 6 · **Sprint:** SPRINT-06

## Summary

The customer review took place on **2026-11-09**. The team demonstrated the server-backed exercise workflow: teacher access and generation, learner browsing and retrieval, local/server verification, and per-learner completion markers.

The university VM was unavailable for this review, so the analytics dashboards, observability dashboards, and the observability QRT were **not shown**. A separate staging execution of [QR-05 QRT-01](qr-05-qrt-01-evidence.md) passed on **2026-11-19**; it is later evidence, not part of the November 9 demonstration.

The customer changed the focus metric to **user satisfaction across learners and teachers**, measured by surveys. The exact survey instrument and threshold are to be finalized after usability testing; there is no satisfaction value yet. Weekly active learners completing an exercise remains a supporting usage metric in the [analytics plan](../../docs/analytics.md#supporting-usage-metric).

## Threshold review

The table covers the four goals that were open when the review began. TOS-05 was added during the meeting and is recorded separately below.

| Goal | Current measure | Can analytics/observability settle it? | Proposal | Customer response |
| ---- | --------------- | -------------------------------------- | -------- | ----------------- |
| [TOS-01](../../docs/threshold-of-success.md#tos-01) | Clean checkout and setup guide allow a learner to choose/generate an exercise, connect VS Code, debug it, and receive a harness verdict by the end of Week 3. | No. Events can show server-side exercise activity and completion, but not whether the extension-based learner workflow is usable end to end or whether setup instructions are needed. | Re-state the normal learner flow around the current VS Code extension: retrieve/open an exercise, debug it, submit it for server verification, and receive a verdict without following setup instructions during ordinary use. | Agreed. TOS-01 is re-scoped and remains Open; see [DEC-027](../../docs/decisions.md#dec-027). |
| [TOS-02](../../docs/threshold-of-success.md#tos-02) | The generated exercise contains the intended defect and the learner's fix is accepted by a harness the learner cannot tamper with. | No. This is verified by exercise/harness correctness and the retained-submission audit, not by usage or operating telemetry. | Remove the run-time “cannot tamper with” condition; retain the correctness check and keep submitted work for a post-deadline audit. | Achieved under the revised audit model; see [DEC-036](../../docs/decisions.md#dec-036) and [DEC-037](../../docs/decisions.md#dec-037). |
| [TOS-03](../../docs/threshold-of-success.md#tos-03) | Every story in the Week 2 candidate receives a customer verdict by the Week 3 meeting. | No. Telemetry cannot establish customer acceptance. | None. | Achieved; the customer accepted the candidate and the team continued from it, as recorded in [DEC-005](../../docs/decisions.md#dec-005). No new decision was needed. |
| [TOS-04](../../docs/threshold-of-success.md#tos-04) | The documentation site is published, linked from the root README, and reachable without cloning by the end of Week 3. | Partly. A reachability check can verify availability, but not whether the intended audience can find and use the documentation. | Use “product user” rather than “learner” for the audience of the documentation-access goal. | The customer confirmed the site was reachable and requested neutral “product user” wording; see [DEC-038](../../docs/decisions.md#dec-038). Achieved. |

- **TOS-01 — Open:** the customer asked to reword the criterion around the current extension-based learner flow. The revised measure targets the remaining project release window, **Week 9 (2026-11-28)**; that date comes from the project plan, not from a date specified by the customer.
- **TOS-02 — Achieved:** the customer accepted the criterion after removing the runtime anti-tampering requirement. A private oracle/harness and retained submissions for later review are recorded in [DEC-036](../../docs/decisions.md#dec-036) and [DEC-037](../../docs/decisions.md#dec-037).
- **TOS-03 — Achieved:** the Week 2 candidate had already been accepted under [DEC-005](../../docs/decisions.md#dec-005); the customer confirmed that the team should continue from the agreed direction.
- **TOS-04 — Achieved:** the customer checked the published site during the review and suggested a neutral audience term; the wording is recorded in [DEC-038](../../docs/decisions.md#dec-038).
- **TOS-05 — Open (new):** the customer asked for an end-to-end scenario in which an operator deploys the product and creates accounts; a teacher creates and assigns exercise sets; learners solve and submit exercises, receive server verdicts, and reconcile teacher updates; and the teacher exports results in a CSV accepted by Moodle or an agreed validation check. The project plan's remaining release window is **Week 9 (2026-11-28)**; the customer did not specify this date in the meeting. See [DEC-028](../../docs/decisions.md#dec-028).

## Focus metric

The focus metric is user satisfaction across learners and teachers, measured by surveys. The customer suggested that the team define the instrument and success threshold after the usability test; “four out of five satisfied” was an example, not an agreed target. The former weekly-active-learner measure is retained as a supporting usage metric, not the focus metric.

## Evidence and artifact index

| Deliverable | Artifact |
| ----------- | -------- |
| Meeting report | [meeting-report.md](meeting-report.md) |
| Meeting script | [meeting-script.md](meeting-script.md) |
| Sanitized transcript | [meeting-transcript.md](meeting-transcript.md) |
| Thresholds and decisions | [threshold of success](../../docs/threshold-of-success.md), [decision log](../../docs/decisions.md) |
| Analytics plan | [analytics plan](../../docs/analytics.md) |
| Architecture and ADR index | [architectural decisions](../../docs/architecture/README.md#architectural-decisions) |
| Automated QR-02 / QR-03 evidence | [CI QRT evidence](qr-02-qr-03-automated-qrt-evidence.md) |
| Later QR-05 QRT-01 staging evidence | [staging QRT-01 evidence](qr-05-qrt-01-evidence.md) |

## Deviations and timing

- The November 9 review could not show the university-VM deployment, analytics dashboards, observability dashboards, or observability QRT because the VM was unavailable. The product workflow was demonstrated instead.
- QR-05 QRT-01 was run later, on November 19, and passed in staging. It is recorded separately and must not be described as having been shown at the November 9 meeting.
- The satisfaction focus metric has no value yet. The customer deferred the exact survey instrument and threshold until the usability test.
