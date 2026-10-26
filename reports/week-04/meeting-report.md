# Week 4 validation meeting report

## Metadata

- **Date:** 2026-10-26
- **Duration:** ~1h 03m
- **Attended:** Magel0n, Tedor49, NikitaRUniverse, Doosuur14, Customer
- **Presented:** the LLM-generated exercises, the VS Code extension, the web-app UX polish, and the quality requirements and architecture against the drivers
- **Recording:** not stated in the transcript; treated as permitted for a sanitized transcript
- **Transcript publication:** permitted (the sanitized transcript is published in the repository)
- **Transcript shared privately:** not required, since publication was permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| ------ | ------- | -------- |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#action-points): "Integrate the customer's API key into the generator and show LLM-generated exercises" | Carried out: the generator now uses the customer's LLM API key and produces LLM-generated exercises, with the deterministic generator as a fallback. | [`DEC-003`](../../docs/decisions.md#dec-003) |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#action-points): "Rework the exercise flow so only instructors generate and students pick curated problems from a gallery" | Carried forward: the gallery and the instructor-only generation flow are not yet implemented; the customer confirmed the extension should prioritize the learner experience and the teacher's view comes next. | [`DEC-014`](../../docs/decisions.md#dec-014), [`DEC-015`](../../docs/decisions.md#dec-015) |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#action-points): "Add UX polish: code highlighting, loading/progress on harness run, horizontal scrolling, and a 'finish' button" | Carried out in part: code highlighting was added to the harness, a loading/busy state on the harness run, and a finish button. Program highlighting in the editable field is deferred because the learner edits in VS Code. | [`DEC-014`](../../docs/decisions.md#dec-014) |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#action-points): "Start sandboxing research and implementation for the runtime" | Ongoing: the customer and team agreed to run learner code in sandboxed containers with capped resources and limited networking. | [`DEC-016`](../../docs/decisions.md#dec-016) |

## Previous open questions

| Question | Answer | Decision |
| -------- | ------ | -------- |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#open-questions): "How do we keep the harness trustworthy if a learner's code can trigger an exception in it?" | Answered: the harness becomes an ordinary, editable file on the learner's side, but the true verdict comes from hidden tests on the server so a learner cannot tamper with the result. | [`DEC-017`](../../docs/decisions.md#dec-017) |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#open-questions): "Does the IT department provide the 16 GB / 8 CPU VM?" | Carried forward: still not confirmed; the product runs locally and the VM decision is awaited. | *None* |
| [`reports/week-03/meeting-report.md`](../week-03/meeting-report.md#open-questions): "How should instructor moderation and problem-author attribution work in the gallery?" | Answered in part: the gallery needs metadata (author name, tags); the teacher's view (submit, edit, run, add to gallery) is next. Student-vs-teacher differentiation is deferred. | [`DEC-014`](../../docs/decisions.md#dec-014) |

## Summary

- The customer accepted the VS Code extension demo and confirmed it "can be closed": choose a problem kind, generate (LLM) an exercise, show the task, and verify the fix all work inside VS Code, and the extension reports pass/fail.
- The customer shifted the product's focus firmly to the VS Code extension: the web-app's editable code field is deprecated in favour of VS Code, and multi-file exercises are required ([`DEC-014`](../../docs/decisions.md#dec-014), [`DEC-015`](../../docs/decisions.md#dec-015)).
- The customer and team agreed learner-submitted code runs on the server in sandboxed containers with capped resources and limited networking, so a learner cannot crash the server ([`DEC-016`](../../docs/decisions.md#dec-016)).
- The customer agreed the harness should be editable by the learner, with an option to restore the server version, and that hidden tests on the server decide the true verdict ([`DEC-017`](../../docs/decisions.md#dec-017)).
- The customer asked for per-exercise folders with automatic git versioning and backup, so learners manage their work and teachers can review it ([`DEC-018`](../../docs/decisions.md#dec-018)).
- The customer asked that recommended VS Code settings and language extensions be generated dynamically per exercise ([`DEC-019`](../../docs/decisions.md#dec-019)).
- Several quality-requirement wording fixes were agreed: rephrase the two-minute attach target to be about the extension sending information, and clarify the mid-run runtime-release requirement to cover both non-dangerous (exception) and dangerous (resource exhaustion) cases.

## Decisions

- [`DEC-014`: Multi-file exercises are required; the web-app's editable code field is deprecated in favour of the VS Code extension.](../../docs/decisions.md#dec-014)
- [`DEC-015`: Prioritize the VS Code extension over the web application for the learner experience.](../../docs/decisions.md#dec-015)
- [`DEC-016`: Learner-submitted code runs on the server inside sandboxed containers with capped resources.](../../docs/decisions.md#dec-016)
- [`DEC-017`: The harness is editable by the learner, with an option to restore the server version.](../../docs/decisions.md#dec-017)
- [`DEC-018`: Each exercise opens as its own folder/workspace with automatic versioning.](../../docs/decisions.md#dec-018)
- [`DEC-019`: The recommended VS Code settings and language extensions are generated dynamically per exercise.](../../docs/decisions.md#dec-019)

## Action points

| Action | Owner | Due |
| ------ | ----- | --- |
| Move toward multi-file exercise support and deprecate the web-app's editable code field in favour of the VS Code extension | Tedor49 | Week 5 |
| Prioritize the VS Code extension as the primary learner surface | Team | Week 5 |
| Implement sandboxed execution: separate containers, capped resources, limited networking | NikitaRUniverse | Week 5 |
| Make the harness an editable file with an option to restore the server version, and separate hidden tests on the server | Doosuur14 | Week 5 |
| Implement per-exercise folders with automatic git versioning and backup | Magel0n | Week 5 |
| Generate recommended VS Code settings and language extensions dynamically per exercise | Team | Week 5 |
| Clarify the quality-requirement wording for the two-minute attach target and the mid-run runtime-release cases | Magel0n | Week 5 |

## Open questions

| Question | What it would change | Follow-up |
| -------- | -------------------- | --------- |
| How do we differentiate between students and teachers? | The roles and permissions model (who may generate and moderate) | Week 5 |
| How are hidden tests produced and kept separate from the local harness? | The harness and evaluation design | Week 5 |
| Does the IT department provide the 16 GB / 8 CPU VM? | Where the server runs | Week 5 |

## Disagreements

| Your position | Customer's position | What you changed |
| ------------- | ------------------- | ---------------- |
| The web app's editable code field is the fallback for using the system without an editor | VS Code is the real editor; the web app's editable field is unnecessary and cannot handle large or multi-file exercises | Agreed to deprecate the editable field and prioritize the VS Code extension ([`DEC-014`](../../docs/decisions.md#dec-014), [`DEC-015`](../../docs/decisions.md#dec-015)) |
| The harness should be non-modifiable so the verdict stays trustworthy | The harness is a learning tool and should be editable, with an option to restore it; hidden tests on the server keep the verdict trustworthy | Made the harness an editable file backed by hidden server tests ([`DEC-017`](../../docs/decisions.md#dec-017)) |
| Exercises are single files written into the workspace root | Each exercise should be its own folder with automatic versioning so learners manage and back up their work | Planned per-exercise folders with git versioning ([`DEC-018`](../../docs/decisions.md#dec-018)) |
