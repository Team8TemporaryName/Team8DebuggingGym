# Week 6 AI usage report

## Tools

- **GitHub Copilot** for inline code and documentation completion.
- **Nessy / GitHub Copilot coding agent** for implementation and first drafts of technical and course artifacts.
- **ChatGPT** for repository and course-requirement review, reconciliation of the sprint closeout evidence, and drafting the remaining report and retrospective material.

## How we used them

GitHub Copilot suggested code and text while the team edited the analytics and observability plans and the web-app instrumentation. The team kept completions that matched the intended behavior and surrounding code, and changed or rejected suggestions that did not.

The coding agent was used for the server-stored exercise flow, teacher/student access, teacher generation, extension delivery, progress tracking, analytics instrumentation, observability instrumentation, quality-requirement tests, and first drafts of the associated documentation. It was also used to derive the customer-meeting report, decision records, and threshold changes from the meeting transcript.

ChatGPT was used during the closeout to compare the live repository, GitHub issues and pull requests, CI evidence, the course assignment, and the team's shadow drafts. It helped identify stale documentation and draft the sprint retrospective, AI usage report, and public report updates. The team must review these drafts against the implementation and the source records before merging.

## What worked

The coding agent accelerated repetitive implementation and cross-file documentation work. Its output was useful when the team checked the generated behavior against the relevant issue criteria, tests, pull-request diffs, and customer transcript.

Inline completion was useful for small edits where the surrounding code and expected shape were already clear. The repository and course-source review helped distinguish implemented features from quality properties that still lack the required level of evidence.

## What did not work

Some generated documentation retained assumptions that had become stale, especially the VM and dashboard deployment status and the distinction between an active telemetry panel and a quality requirement actually passing. The shadow report also contained outdated screenshot paths and release/threshold references. These were not copied as authoritative facts; the team reconciled them against the current product repository, GitHub release and tag, dashboard images, test evidence, and decision log.

Generated code and prose were not treated as proof. The team used automated CI for code checks, the staging QRT output for deployed diagnosability, and the customer transcript for meeting decisions. Any remaining uncertainty is recorded as a limitation rather than converted into a success claim.
