# Threshold of success

## TOS-01

A learner can complete the core task end to end in the product by the end of Week 3.

- **Status:** Open
- **Measure:** a clean checkout, following `docs/setup.md`, lets a learner choose a problem kind, get a generated exercise, connect their own VS Code, debug it, and get a pass/fail verdict from the harness, by the end of Week 3.
- **Changed:**
  - Added as the threshold's leading goal: the core task is the product's reason to exist, per the customer's verdict on the candidate, [`DEC-005`](decisions.md#dec-005).

## TOS-02

The generated exercise contains the intended defect, and the learner's fix is judged by a harness the learner cannot tamper with.

- **Status:** Open
- **Measure:** the harness reports the planted defect present on the buggy exercise and absent once the learner fixes it, on every exercise the slice generates in the Week 3 demonstration.
- **Changed:**
  - Added as a goal: the customer required a fixed, non-modifiable success state, per [`DEC-006`](decisions.md#dec-006).

## TOS-03

Every story in the Week 2 candidate is built, shown, and either accepted by the customer or moved out of the candidate by the customer's decision at the Week 3 meeting.

- **Status:** Open
- **Measure:** each candidate story has a customer verdict at the Week 3 meeting, each recorded as a `DEC-nnn`.
- **Changed:**
  - Added as a goal: the Week 3 build scope is exactly the candidate's stories, per [`DEC-005`](decisions.md#dec-005).

## TOS-04

A learner can reach the product and its documentation without cloning the repository.

- **Status:** Open
- **Measure:** `docs/` is published as a GitHub Pages site, linked from the root `README.md`, and reachable by the end of Week 3.
- **Changed:**
  - Added as a goal: the repository requirements call for a published documentation site in Week 3.

## Failure And Success Statements

| Goal | Success statement | Failure statement |
| ---- | ----------------- | ----------------- |
| [TOS-01](#tos-01) | A learner completes the core task end to end. | We never put a runnable core task in front of anyone. |
| [TOS-01](#tos-01) | A clean checkout runs the slice by following the setup. | Nobody outside the team could run the product code. |
| [TOS-02](#tos-02) | The harness reports the planted defect and its fix. | The learner could not tell whether the bug was actually gone. |
| [TOS-03](#tos-03) | The customer accepts the Week 2 candidate stories. | The customer never accepted the candidate. |
| [TOS-04](#tos-04) | A reader reaches the docs site without cloning. | Only the team could see the documentation. |
