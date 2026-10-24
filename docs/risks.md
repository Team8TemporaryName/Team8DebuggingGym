# Risks

| ID                  | Status | Impact | Likelihood | Risk |
| ------------------- | ------ | ------ | ---------- | ---- |
| [RISK-01](#risk-01) | Open   | High   | Medium     | The team has not built a VS Code attach-to-server flow end to end in the product, so the connect story may take longer than the sprint allows, which would leave the core task incomplete. |
| [RISK-02](#risk-02) | Open   | High   | Medium     | The LLM provider's API key and budget are constrained, so generated exercises may be slow or unavailable during the Week 3 meeting, which would leave the generation story unproven. |
| [RISK-03](#risk-03) | Open   | Medium | Medium     | The documentation site and the setup page may be left to too few members near the deadline, which would push them past the sprint. |
| [RISK-04](#risk-04) | Open   | Medium | Low       | The university VM may not be provisioned in time, so the debug environments may have nowhere to run, which would block the connect story. |

## RISK-01

The team has not built a VS Code attach-to-server flow end to end in the product, so the connect story may take longer than the sprint allows, which would leave the core task incomplete.

- **Status:** Open
- **Impact:** High
  - The core task cannot complete without the connect story, so the sprint would end without the MUP.
- **Likelihood:** Medium
  - The Week 2 prototype proved VS Code can attach over DAP, but wiring it into the product with generated exercises is new.
- **Trigger:** the connect story's first task is not merged by the sprint's third day.
- **Window:** [SPRINT-03](project-plan.md#sprint-03).
- **Mitigation:** build the connect story first, on the proven prototype, before adding generation and the front end.
- **Contingency:** fall back to serving one hand-written exercise through the debug environment, and move generation to the first task of the next sprint, with the customer's agreement.

## RISK-02

The LLM provider's API key and budget are constrained, so generated exercises may be slow or unavailable during the Week 3 meeting, which would leave the generation story unproven.

- **Status:** Open
- **Impact:** High
  - A generation failure in front of the customer would leave the MUP's central story unaccepted.
- **Likelihood:** Medium
  - The budget is $5–$10 and the provider may rate-limit, and the rehearsal and the meeting fall close together.
- **Trigger:** a generation request comes back rate-limited or over budget.
- **Window:** [SPRINT-03](project-plan.md#sprint-03), up to the Week 3 meeting.
- **Mitigation:** keep a small, deterministic local generator as a fallback, and rehearse generation the day before the meeting.
- **Contingency:** fall back to the recorded, deterministic exercises and show generation once more for the customer after the meeting.

## RISK-03

The documentation site and the setup page may be left to too few members near the deadline, which would push them past the sprint.

- **Status:** Open
- **Impact:** Medium
  - The docs site and setup are required in Week 3; missing them fails the submission even with a working slice.
- **Likelihood:** Medium
  - The team's effort concentrates on product code, and the docs site is a distinct unfamiliar task.
- **Trigger:** the docs-site task is not started by the sprint's fourth day.
- **Window:** [SPRINT-03](project-plan.md#sprint-03).
- **Mitigation:** schedule the docs-site task with an owner early, and keep the setup page in the Definition of Done for every pull request.
- **Contingency:** publish a minimal GitHub Pages site from the existing `docs/` with a landing page, and extend it in the next sprint.

## RISK-04

The university VM may not be provisioned in time, so the debug environments may have nowhere to run, which would block the connect story.

- **Status:** Open
- **Impact:** Medium
  - The connect story needs a hosted debug runtime; without it the learner cannot attach.
- **Likelihood:** Low
  - The customer has asked the IT department but is still waiting; a local fallback exists.
- **Trigger:** no VM is available by the sprint's third day.
- **Window:** [SPRINT-03](project-plan.md#sprint-03).
- **Mitigation:** run the debug environments in a local Docker container for the demonstration, per the prototype.
- **Contingency:** keep the server runnable locally, per the customer's note that the server should be runnable locally if no VM is provided.