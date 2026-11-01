# Week 5 validation meeting report

## Metadata

- **Date:** 2026-10-30
- **Duration:** ~1 h 07 min
- **Attended:** Magel0n, Tedor49, NikitaRUniverse, Doosuur14, Customer
- **Presented:** the deployed product, the automated test suite, the quality requirement tests, and the production stack
- **Recording:** permitted
- **Transcript publication:** permitted
- **Transcript shared privately:** not applicable — the transcript is public in this repository
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| ------ | ------- | -------- |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Move toward multi-file exercise support and deprecate the web app's editable code field" | Partly carried out: each exercise is now a folder with `exercise.py`, `harness.py`, and `task.md`; the sidebar is the primary surface. The web app's editable code field is still present but no longer the focus. | [`DEC-015`](../../docs/decisions.md#dec-015) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Prioritize the VS Code extension as the primary learner surface" | Carried out: the sidebar is the primary learner surface (choose kind, generate, see the task, run the harness, verify, open saved exercises). | [`DEC-015`](../../docs/decisions.md#dec-015) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Implement sandboxed execution" | Not carried out: the customer agreed for now to run exercises with `uv` and not to sandbox immediately; local container running is a "should have" for later. | [`DEC-021`](../../docs/decisions.md#dec-021) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Make the harness editable with a server restore and hidden tests" | Partly carried out: the harness is editable and a learner can run it locally; server restore and hidden tests are not implemented. The customer flagged that printing the harness reveals the hidden tests and asked to protect file permissions. | [`DEC-022`](../../docs/decisions.md#dec-022) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Implement per-exercise folders with git versioning" | Partly carried out: per-exercise folders exist; git versioning is not finished and does not commit automatically. The customer decided one repository at the top level, not per folder. | [`DEC-020`](../../docs/decisions.md#dec-020) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Generate recommended VS Code settings and language extensions dynamically" | Not carried out this meeting; discussed as future work tied to the packages and per-language support. | [`DEC-024`](../../docs/decisions.md#dec-024) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#action-points): "Clarify quality-requirement wording" | Carried out: `QR-01` and `QR-03` were reworded per the customer's feedback. | [`DEC-014`](../../docs/decisions.md#dec-014) |

## Previous open questions

| Question | Answer | Decision |
| -------- | ------ | -------- |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#open-questions): "How do we differentiate between students and teachers?" | Answered: the customer wants separate access for students and teachers, a teacher interface in the extension and on the site, and assignment of exercises to students. This is now planned, not built. | [`DEC-023`](../../docs/decisions.md#dec-023) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#open-questions): "How are hidden tests produced and kept separate from the local harness?" | Answered: the customer asked to protect file permissions so the learner cannot read the hidden tests, and to run `uv` for dependencies. Hidden tests are not implemented yet. | [`DEC-022`](../../docs/decisions.md#dec-022) |
| [`reports/week-04/meeting-report.md`](../week-04/meeting-report.md#open-questions): "Does the IT department provide the 16 GB / 8 CPU VM?" | Carried forward: still not provided; the product runs self-hosted locally. | *None* |

## Summary

- The sidebar demo was accepted: choose a kind, generate, see the task, run the harness locally (coloured terminal output), verify on the server, and reopen saved per-exercise folders. The customer confirmed the core implementation is "correct and to your satisfaction".
- The customer found a bug: "verify fix against the harness" ran only two tests while the harness had four; fixing the code so it passes was confirmed to work.
- The customer decided the git repository lives at the top level (one repo for all exercises) rather than per exercise folder, so history survives deleting a folder and is easy to back up; per-file history covers the clutter.
- The customer agreed to a **packages** concept for grouping exercises visually without changing the physical layout, to warn when a folder the server expects is missing, and to run dependencies with `uv` for now; local container running is a "should have".
- New scope for later sprints was confirmed: a public (instructor-curated) exercise library, separate student/teacher access and teacher interface, assignment of exercises, and at least two languages (Python and one more).

## Decisions

- Each exercise shows its task statement and harness in its own folder, and exercises are named `exercise-<kind>-<id>` by the backend; reopening a saved exercise restores its files. (shown, accepted)
- One top-level git repository for all exercises, not per-folder, so deleting an exercise folder does not lose history and the student can back up to GitHub. [`DEC-020`](../../docs/decisions.md#dec-020)
- Packages group exercises visually by name without changing the physical layout; dependencies can be provided per package. [`DEC-021`](../../docs/decisions.md#dec-021)
- Protect hidden tests on the server so the learner cannot read them; use `uv` for dependencies for now. [`DEC-022`](../../docs/decisions.md#dec-022)
- Support at least two languages (Python and one more); one exercise and one package use one language. [`DEC-024`](../../docs/decisions.md#dec-024)
- A public exercise library, separate student/teacher access, and a teacher interface are confirmed scope for later sprints. [`DEC-023`](../../docs/decisions.md#dec-023)
- After the MUP, run user-acceptance tests with real students, then hand the project over to the customer at the course's end. [`DEC-025`](../../docs/decisions.md#dec-025)

## Action points

| Action | Owner | Due |
| ------ | ----- | --- |
| Fix the verify-bug so the full harness (all tests) runs on the server, matching the local run. | @Tedor49 | Week 6 |
| Implement pinning of the current exercise's open files in the extension. | @Magel0n | Week 6 |
| Warn the learner when a folder the server expects is missing or renamed, with an option to refetch. | @NikitaRUniverse | Week 6 |
| Decide the package layout and the top-level git repository with per-exercise commit naming. | @Doosuur14 | Week 6 |
| Protect hidden tests via server file permissions; keep them out of the local harness. | @Magel0n | Week 6 |
| Design the exercise-library and teacher-assignment flow (students vs. teachers). | @Tedor49 | Week 6 |
| Add at least a second language (e.g. Python + one more) to the exercise format. | @Doosuur14 | Week 6 |

## Open questions

| Question | What it would change | Follow-up |
| -------- | -------------------- | --------- |
| What exactly should a "package" contain — one lab, one course, nested packages? | The grouping, dependency, and language layout of exercises. | Resolve with the customer in Week 6. |
| How do students and teachers authenticate and get separate interfaces? | The library, assignment, and teacher-interface scope. | Design in Week 6. |
| Does the IT department provide the 16 GB / 8 CPU VM? | Where the deployment and the `deployed` quality requirement tests run. | Still awaited; carried forward. |

## Disagreements

| Your position | Customer's position | What you changed |
| ------------- | ------------------- | ---------------- |
| A git repository per exercise folder makes progress and review easier. | One repository at the top level so history survives deleting a folder and is easy to back up. | Adopted the top-level repository; keep per-file history and name commits per exercise. |
| Problem kinds should be a predetermined catalogue. | They should be an open prompt so any subject is supported. | Adopted an open prompt for generation. |
| Sandboxing exercises is needed from the start. | It is not needed now; `uv` is enough, container running is a "should have". | Use `uv` now; defer local container running. |
