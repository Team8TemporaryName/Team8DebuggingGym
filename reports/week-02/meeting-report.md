# Week 2 validation meeting report

## Metadata

- **Date:** 2026-10-14
- **Duration:** ~65 minutes
- **Attended:** Tedor49, Magel0n, NikitaRUniverse, Doosuur14, Customer
- **Presented:** the product vision, the boundary, the minimum usable product
  candidate, and the debugging-in-VS-Code prototype
- **Recording:** permitted (per the customer, prior to the meeting)
- **Transcript publication:** permitted (the transcript is committed)
- **Transcript shared privately:** permitted
- **Transcript:** [meeting-transcript.md](meeting-transcript.md)
- **Script:** [meeting-script.md](meeting-script.md)

## Previous action points

| Action | Outcome | Decision |
| ------ | ------- | -------- |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#action-points): "Build a single-language (Python) prototype focused on debugging in the user's own IDE" | Carried out: the prototype attached the learner's own VS Code to a hosted container over DAP and debugged a buggy program with breakpoints and a harness verdict. | Confirms [DEC-004](../../docs/decisions.md#dec-004) |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#action-points): "Design the system so it is extensible to multiple languages" | Kept as future work; the customer pulled multi-language out of the minimal product but the system is designed to be extensible later. | [DEC-005](../../docs/decisions.md#dec-005) |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#action-points): "Define the exercise layout and the reproducible container/VM setup within 16 GB / 8 CPU" | The Docker container runs the exercise and harness and fits the constraint; the VM itself is still pending IT provision. | [DEC-003](../../docs/decisions.md#dec-003) |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#action-points): "Draft a statistics/metrics plan and a budget/spend-tracking approach" | Not addressed in Week 2; carried forward. | *TODO / None* |

## Previous open questions

| Question | Answer | Decision |
| -------- | ------ | -------- |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Which exact languages should the MVP support?" | Open; customer pulled multi-language out of the minimal product for now. | [DEC-005](../../docs/decisions.md#dec-005) |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Who provides the API key and how are spend limits tracked?" | Carried forward; budget is $5–$10 ([CON-002](../../docs/product-vision.md)). | *TODO / None* |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Will debugging sessions be supervised by an instructor at all?" | Open; not discussed in Week 2. | *None* |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Browser VS Code vs. installed extensions vs. a third editor: which UX should v1 target?" | Partially answered: installed VS Code with a local debugging experience is confirmed; the standalone-vs-browser question stays open. | [DEC-004](../../docs/decisions.md#dec-004) |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "What is a reliable metric for 'the learner learned to debug' for a general audience?" | Open; carried forward. | *None* |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Can the IT department provide more than 16 GB RAM / 8 CPUs?" | The customer is still waiting on the IT department; if no VM is provided, the server must run locally. | *None* |
| [`reports/week-01/meeting-report.md`](../week-01/meeting-report.md#open-questions): "Should we reach out to Codeforces/LeetCode admins or contest creators?" | Open; not a priority for the minimal product. | *None* |

## Summary

- The prototype demonstrated that debugging a generated exercise in the user's
  own installed VS Code works: VS Code attached to the hosted container over
  DAP, hit breakpoints, and the harness reported the bug and then a pass once
  the fix was pushed.
- The customer confirmed the local debugging experience with files available
  locally is the right direction ([DEC-004](../../docs/decisions.md#dec-004)),
  while leaving the standalone-vs-browser question open.
- The customer advised making the story set less ambitious and accepted the
  candidate, pulling the multi-language and gallery stories out of the minimal
  product ([DEC-005](../../docs/decisions.md#dec-005)).
- The customer agreed the harness must not be modifiable so the success state
  is fixed ([DEC-006](../../docs/decisions.md#dec-006)), and that task authors
  must not be able to modify the containers ([DEC-008](../../docs/decisions.md#dec-008)).
- The catalogue story was reworded into choosing an exercise not yet practiced,
  and the gallery was justified as a public pool students can choose from and
  teachers can reuse ([DEC-007](../../docs/decisions.md#dec-007)).

## Decisions

- **The customer's verdict on the minimum usable product candidate:** accepted,
  with the multi-language and gallery stories pulled out
  ([DEC-005](../../docs/decisions.md#dec-005)).
- **Keep local debugging in the user's own installed IDE** as the debugging
  environment ([DEC-004](../../docs/decisions.md#dec-004)).
- **The harness is non-modifiable** so the success state is fixed
  ([DEC-006](../../docs/decisions.md#dec-006)).
- **Add a "choose an exercise not yet practiced" story**, and justify the
  gallery as a public pool for students and teachers
  ([DEC-007](../../docs/decisions.md#dec-007)).
- **Task authors may not modify the containers** ([DEC-008](../../docs/decisions.md#dec-008)).

## Action points

| Action | Owner | Due |
| ------ | ----- | --- |
| Auto-sync the learner's locally edited code back to the server, and add a way to run the module and reconnect | Team | Week 3 |
| Keep the harness non-modifiable and add a task statement inside the IDE | Team | Week 3 |
| Sandbox/virtualize the runtime and prevent task authors from modifying containers | Team | Week 3 |
| Add a "choose an exercise not yet practiced" story and reword the catalogue story | Team | Week 3 |

## Open questions

| Question | What it would change | Follow-up |
| -------- | -------------------- | --------- |
| Should the debugging happen in a standalone VS Code or in the browser? | The distribution model (extension vs. web app) | Revisit in Week 3 |
| How do we keep the harness trustworthy if a learner's code can trigger an exception in it? | The harness design and guardrails | Revisit in Week 3 |
| Which languages, and are hidden tests on the server separate from the local ones? | The exercise layout and harness | Revisit in Week 3 |
| Does the IT department provide the 16 GB / 8 CPU VM? | Where the server runs | Revisit in Week 3 |

## Disagreements

| Your position | Customer's position | What you changed |
| ------------- | ------------------- | ---------------- |
| The catalogue story was about browsing a technical list of problem kinds | The intent is choosing an exercise not yet practiced, so the learner improves in a new environment | Reworded the catalogue story ([DEC-007](../../docs/decisions.md#dec-007)) |
| Multi-language and the gallery belonged in the minimal product | The story set was too ambitious; both should come out of the candidate | Pulled both out of the minimal product ([DEC-005](../../docs/decisions.md#dec-005)) |
| Target only university non-beginners | Complete beginners should be accommodated if instructions are clear | Softened the audience assumption ([DEC-002](../../docs/decisions.md#dec-002)) |
