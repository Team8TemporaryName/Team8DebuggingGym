# Week 3 validation meeting report

## Metadata

- **Date:** 2026-10-24
- **Duration:** ~41 minutes
- **Attended:** Magel0n, Tedor49, NikitaRUniverse, Doosuur14, Customer
- **Presented:** the minimum usable product slice — choosing a problem kind, generating an exercise, verifying the fix against the harness, and connecting VS Code
- **Recording:** not stated in the transcript; treated as permitted for a sanitized transcript
- **Transcript publication:** permitted (the sanitized transcript is published in the repository)
- **Transcript shared privately:** not required, since publication was permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| ------ | ------- | -------- |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#action-points): "Auto-sync the learner's locally edited code back to the server, and add a way to run the module and reconnect" | Carried out: the learner's edited source is sent to the server and run against the harness in an isolated subprocess (`POST /api/exercises/{id}/verify` in [`app/main.py`](../../app/main.py)); a `launch.json` for reconnecting is returned by the launch endpoint. | None |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#action-points): "Keep the harness non-modifiable and add a task statement inside the IDE" | Carried out: the harness is fixed and never editable by the learner ([`app/harness_runner.py`](../../app/harness_runner.py)); each exercise carries a task statement shown in the app. | [`DEC-006`](../../docs/decisions.md#dec-006) |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#action-points): "Sandbox/virtualize the runtime and prevent task authors from modifying containers" | Postponed: proper sandboxing is difficult and a task for future iterations | [`DEC-008`](../../docs/decisions.md#dec-008) |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#action-points): "Add a 'choose an exercise not yet practiced' story and reword the catalogue story" | Carried out in part: the catalogue of problem kinds is implemented, and choosing a kind generates a fresh exercise; the "not yet practiced" tracking is carried forward to Week 4. | *None* |

## Previous open questions

| Question | Answer | Decision |
| -------- | ------ | -------- |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#open-questions): "Should the debugging happen in a standalone VS Code or in the browser?" | Installed VS Code: the product returns a debugpy `launch.json` the learner's own installed VS Code attaches to. The browser variant stays open for a later week. | [`DEC-004`](../../docs/decisions.md#dec-004) |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#open-questions): "How do we keep the harness trustworthy if a learner's code can trigger an exception in it?" | Partly answered: the harness is fixed and non-modifiable; guardrails for learner-triggered exceptions in the harness remain open. | *None* |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#open-questions): "Which languages, and are hidden tests on the server separate from the local ones?" | Python only for the MUP; hidden tests are not yet separated. | [`DEC-009`](../../docs/decisions.md#dec-009) |
| [`reports/week-02/meeting-report.md`](../week-02/meeting-report.md#open-questions): "Does the IT department provide the 16 GB / 8 CPU VM?" | Not yet answered; the product runs locally per the customer's fallback. | *None* |

## Summary

- The customer accepted the core loop: choose a problem kind, get a generated exercise, edit it, and get a pass/fail verdict from a non-modifiable harness — "we can assume that the scenario passed."
- The customer re-scoped who generates exercises: only instructors generate, and students access instructor-curated problems from a public gallery, rather than generating their own ([`DEC-010`](../../docs/decisions.md#dec-010)).
- The public gallery, with instructor curation and moderation, is a core part of the product, not a later extra ([`DEC-011`](../../docs/decisions.md#dec-011)).
- The product should move toward a VS Code extension in future releases, with relevant plugins pre-installed ([`DEC-012`](../../docs/decisions.md#dec-012)).
- The customer will not introduce an in-environment AI agent for now; the experience stays static with clear instructions and read-only code parts ([`DEC-013`](../../docs/decisions.md#dec-013)).
- The customer agreed to provide an API key with a $5 budget for testing generated exercises; the key itself stays out of the repository.
- Several UX polish items were noted: code highlighting, a loading/progress signal while the harness runs, horizontal scrolling for long harness output, and a "finish" button that completes an exercise.

## Decisions

- [`DEC-010`: Only instructors generate exercises; students access instructor-curated problems from a public gallery.](../../docs/decisions.md#dec-010)
- [`DEC-011`: The public gallery, with instructor curation and moderation, is a core part of the product.](../../docs/decisions.md#dec-011)
- [`DEC-012`: The product moves toward a VS Code extension in future releases.](../../docs/decisions.md#dec-012)
- [`DEC-013`: No AI agent inside the learner's environment for now.](../../docs/decisions.md#dec-013)

## Action points

| Action | Owner | Due |
| ------ | ----- | --- |
| Integrate the customer's API key into the generator and show LLM-generated exercises | Magel0n | Week 4 |
| Rework the exercise flow so only instructors generate and students pick curated problems from a gallery | Tedor49 | Week 4 |
| Add UX polish: code highlighting, loading/progress on harness run, horizontal scrolling, and a "finish" button | Doosuur14 | Week 4 |
| Start sandboxing research and implementation for the runtime | NikitaRUniverse | Week 4 |
| Draft the VS Code extension direction (pre-installed plugins) for a future release | Team | Week 5 |

## Open questions

| Question | What it would change | Follow-up |
| -------- | -------------------- | --------- |
| How do we keep the harness trustworthy if a learner's code can trigger an exception in it? | The harness design and guardrails | Revisit in Week 4 |
| Does the IT department provide the 16 GB / 8 CPU VM? | Where the server runs | Revisit in Week 4 |
| How should instructor moderation and problem-author attribution work in the gallery? | The gallery design | Revisit in Week 4 |

## Disagreements

| Your position | Customer's position | What you changed |
| ------------- | ------------------- | ---------------- |
| The MUP lets a learner generate an exercise for the skill they chose | Students should only access instructor-curated problems; only instructors generate | Re-scoped the core task so students use curated problems ([`DEC-010`](../../docs/decisions.md#dec-010)) |
| A learner should be able to request a newly generated exercise on demand | A generated exercise is not stored or executed on the platform; students only get the code and harness | Recorded the customer's model in the product ([`DEC-010`](../../docs/decisions.md#dec-010)) |
| Debugging in the browser could be revisited | VS Code with an extension is the direction to move toward | Agreed to move toward the VS Code extension in future releases ([`DEC-012`](../../docs/decisions.md#dec-012)) |
