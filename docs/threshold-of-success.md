# Threshold of success

## TOS-01

A learner can complete the current core practice flow end to end using the VS Code extension, without following setup instructions during ordinary exercise use.

- **Status:** Open
- **Measure:** By the end of Week 9 (2026-11-28), a learner can use the VS Code extension to retrieve and open a server-stored exercise, debug and fix the intended defect in VS Code, submit the work for server verification, and receive a verdict. The setup guide remains available for installation and operators, but is not a required step in the ordinary learner flow.
- **Changed:**
  - Re-scoped from the earlier choose/generate/connect flow to the current extension-based learner workflow, per [DEC-027](decisions.md#dec-027). The Week 9 target follows the remaining project release window in [SPRINT-09](project-plan.md#sprint-09); the customer did not set a new date during the review.

## TOS-02

A generated exercise contains the intended defect, and the learner's fix is evaluated by a harness built against a private ground-truth solution.

- **Status:** Achieved
- **Measure:** The generated exercise has an intended buggy state and a corresponding private ground-truth solution; the harness distinguishes the buggy state from the corrected state. Submitted work is retained for post-deadline review.
- **Outcome:** At the Week 6 review, the customer accepted this threshold as achieved after removing the requirement that every run-time workaround be impossible. Submissions are retained on the server and in Git history for post-deadline audit; server-side hidden-test protection remains in place ([DEC-022](decisions.md#dec-022), [DEC-036](decisions.md#dec-036), [DEC-037](decisions.md#dec-037)).

- **Changed:**
  - Added as a goal after the customer required a non-modifiable success state, per [DEC-006](decisions.md#dec-006).
  - Replaced the run-time “learner cannot tamper with” condition with retained submissions and post-deadline audit, per [DEC-037](decisions.md#dec-037).

## TOS-03

Every story in the Week 2 candidate is built, shown, and either accepted by the customer or moved out of the candidate by the customer's decision at the Week 3 meeting.

- **Status:** Achieved
- **Measure:** Each candidate story has a customer verdict at the Week 3 meeting, each recorded as a `DEC-nnn`.
- **Outcome:** The customer had accepted the minimum usable product candidate and agreed that the team should continue from the settled direction ([DEC-005](decisions.md#dec-005); [Week 6 review](../reports/week-06/meeting-report.md)).

- **Changed:**
  - Added as a goal: the Week 3 build scope is exactly the candidate's stories, per [DEC-005](decisions.md#dec-005).

## TOS-04

A product user can reach the product and its documentation without cloning the repository.

- **Status:** Achieved
- **Measure:** `docs/` is published as a GitHub Pages site, linked from the root `README.md`, and reachable by the end of Week 3.
- **Outcome:** The customer opened the published documentation site during the Week 6 review and confirmed it was reachable without cloning. The audience wording was made neutral because the setup instructions may serve an operator as well as a learner ([DEC-038](decisions.md#dec-038); [Week 6 review](../reports/week-06/meeting-report.md)).

- **Changed:**
  - Added as a goal: the repository requirements call for a published documentation site in Week 3.
  - Replaced “learner” with “product user” to cover operators and other people who may use the setup documentation, per [DEC-038](decisions.md#dec-038).

## TOS-05

The operator, teacher, and learner can each complete their part of the product's end-to-end classroom workflow.

- **Status:** Open
- **Measure:** By the end of Week 9 (2026-11-28), an operator can deploy from a clean checkout and create teacher/student accounts; a teacher can create an exercise, group it into an exercise set, and assign it; learners can retrieve, solve, and submit the exercise, receive a server verdict, and reconcile a later teacher update; and the teacher can export results in a CSV accepted by Moodle or by an agreed validation check. The Week 9 target follows the remaining project release window in [SPRINT-09](project-plan.md#sprint-09); the customer did not set a date during the review.
- **Changed:**
  - Added after the customer described the extended operator–teacher–learner scenario and agreed to split it by role, per [DEC-028](decisions.md#dec-028).

## Failure And Success Statements

| Goal | Success statement | Failure statement |
| ---- | ----------------- | ----------------- |
| [TOS-01](#tos-01) | A learner completes the core task end to end. | We never put a runnable core task in front of anyone. |
| [TOS-01](#tos-01) | A clean checkout runs the slice by following the setup. | Nobody outside the team could run the product code. |
| [TOS-02](#tos-02) | The harness reports the planted defect and its fix. | The learner could not tell whether the bug was actually gone. |
| [TOS-03](#tos-03) | The customer accepts the Week 2 candidate stories. | The customer never accepted the candidate. |
| [TOS-04](#tos-04) | A reader reaches the docs site without cloning. | Only the team could see the documentation. |
| [TOS-05](#tos-05) | An operator, teacher, and learner complete their parts of the end-to-end workflow, including assignment, submission, update reconciliation, and results export. | The product cannot support a complete classroom workflow from deployment through validated results. |
