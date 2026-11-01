# Week 5 sprint retrospective

## Went well

- The extension sidebar became a real, accepted learner surface: the customer confirmed the core flow "is correct and to your satisfaction" and asked only that we finish the acknowledged bugs.
- The coloured pytest output in a terminal and the per-exercise folders were demonstrable and well received.
- We aligned the deployment and the quality requirement tests to the course rules (manual deployment; `Level`/`Runs at`/`Why Manual` fields), catching the discrepancy before release.

## What did not go well

- A live demo exposed a real bug: verifying a fix ran only two of the four harness tests, so the server-side verify path did not match the local run.
- Git versioning per exercise was not finished (does not commit automatically), and the customer redirected it to a single top-level repository, so some work was toward the wrong design.
- Some Week 4 action points (sandboxing, hidden tests, dynamic settings) were only partly addressed or deferred; a few were clarified as future scope rather than done.

## Actions

- Fix the server-side verify so it runs the full harness and matches the local `pytest` run.
- Implement pinning of the current exercise's open files, and warn when a folder the server expects is missing or renamed.
- Move to the top-level git repository decided in `DEC-020`, with per-exercise commit naming.
- Protect hidden tests on the server (`DEC-022`) and add a second language (`DEC-024`).
- Design the packages and the student/teacher separation (`DEC-021`, `DEC-023`).
