# Week 5 report

**Project:** Debugging Gym
**Team:** 8
**Week:** 5 — Testing, Automation, Production Deployment & Next Product Release
**Due:** 2026-10-29

## Summary

This week the Debugging Gym product was made deployable and verifiable, and the customer's Week 4 feature requests were carried out in the VS Code extension. We expanded the automated test suite from a single module to focused generator, harness-runner, and web-app-API suites (26 tests), added quality requirement tests (`QRT-nn`) to all four quality requirements with their required fields (level, where they run, and the manual justification), and recorded them in the plan's quality requirement testing plan. We set up a self-hosted production stack (`docker-compose.yml`, `deploy/webapp.Dockerfile`, `docs/deployment.md`).

Per the course deployment rules, the deployment is **manual** from the university network: the product CI cannot reach the VM, so we removed the CI deploy job rather than plan a deployment in CI. The `python.yml` workflow runs the product tests in CI; the runbook in `docs/deployment.md` describes the manual deploy to staging and production.

We also carried out the Week 4 action points that belong to the extension: a **sidebar GUI** for the VS Code extension (the primary learner surface), **per-exercise folders** with git versioning, an **editable pytest harness**, and **dynamic per-exercise VS Code settings**. Exercise verification now runs under pytest, giving the learner the coloured expected-vs-got output the customer asked for. Sandboxed execution and hidden server-side tests are deferred to a later week (server-side work).

The production instance runs locally for now — the university VM is still awaited. The tests that need a live host (attach timing, runtime release, availability) are planned but stay `Not verified` until the host is reachable. Whether the debug-runtime attach stays part of the web app is a **pending decision** the team has not yet settled; the code is left as-is until then.

- **Release:** `REL-05`, tagged [v0.5.0](https://github.com/Team8TemporaryName/Team8DebuggingGym/releases/tag/v0.5.0).
- **What moved out of the sprint:** Nothing

## Findings

The clean-checkout test requirement is met and verified: `python -m pytest tests/ -q` runs the full suite and passes from a clean checkout, and a change that breaks the generator or harness fails it. The tests that need a live debug runtime or a production host are planned for this sprint but stay `Not verified` until the host is reachable. [The testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) carries every row that is not `Passes`.

## Customer-meeting outcome

The customer accepted the sidebar demo: choose a kind, generate an exercise, see the task statement, run the harness locally with coloured terminal output, verify the fix on the server, and reopen saved per-exercise folders. The customer said the core implementation is "correct and to your satisfaction", and asked us to finish the open bugs we acknowledged. One bug was found live: verifying a fix ran only two tests while the harness had four. Decisions recorded: top-level git repository rather than per-folder (`DEC-020`), packages with `uv` and deferring sandboxing (`DEC-021`), protecting hidden tests on the server (`DEC-022`), confirming the library/teacher-interface scope (`DEC-023`), at least two languages (`DEC-024`), and user-acceptance tests before hand-over (`DEC-025`).

Full detail is in [`meeting-report.md`](meeting-report.md) and, when the meeting was recorded, [`meeting-transcript.md`](meeting-transcript.md).

## Coverage table

| Deliverable | Artifact |
| ----------- | -------- |
| Sprint plan and estimates | [`docs/project-plan.md#sprint-05`](../../docs/project-plan.md#sprint-05), with its goal, its planned velocity, and its actual velocity |
| Test suite | [`tests/`](../../tests/), with the generator, harness-runner, and web-app-API suites |
| Quality requirement tests | [`docs/quality-requirements/qr/QR-01.md#qrt-01`](../../docs/quality-requirements/qr/QR-01.md#qrt-01) and the `QRT-nn` sections in `QR-02`..`QR-04` |
| Quality requirement testing plan | [`docs/project-plan.md#quality-requirement-testing-plan`](../../docs/project-plan.md#quality-requirement-testing-plan) |
| CI/CD | [`.github/workflows/product-ci.yml`](../../.github/workflows/product-ci.yml) (product tests in CI); deployment is manual per [the runbook](../../docs/deployment.md) |
| Week 4 action points | [`## Previous action points`](meeting-report.md#previous-action-points) in `reports/week-05/meeting-report.md` |
| Week 4 open questions | [`## Previous open questions`](meeting-report.md#previous-open-questions) in the same report |
| Meeting script | [`reports/week-05/meeting-script.md`](meeting-script.md) |
| Customer validation | [`reports/week-05/meeting-report.md`](meeting-report.md), the transcript when there is one, and each story's verdict |
| `REL-05` | [the plan's `REL-05` block](../../docs/project-plan.md#rel-05), the tag, and the changelog's released section |
| Sprint retrospective | [`reports/week-05/sprint-retrospective.md`](sprint-retrospective.md) |
| AI usage | [`reports/week-05/ai-usage.md`](ai-usage.md) |

## Repository evidence

| Evidence | Link / location |
| -------- | --------------- |
| A merged pull request that closed its task issue | [Pull request](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/69) |
| Latest green link check run | [Link check](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/41348938383/job/124974697456) |
| Latest green Markdown check run on `main` | [Markdown lint](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/41348938394/job/124974697723) |
| Latest green product code check run on `main` | [Code check](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/41348938449/job/124975375267) |

## Deviations

None
