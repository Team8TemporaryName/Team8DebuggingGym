# Week 2 report — Debugging Gym

**Project:** Debugging Gym · **Team number:** 8

> **Problem space.** Software developers and programming-language learners want
> targeted, hands-on practice that trains a specific debugging skill, but the
> existing platforms offer general exercises rather than exercises for a
> particular kind of debugging problem.

## Summary

Week 2 turns the Week 1 direction into requirements, then tests how much of it
was wrong. We moved the Week 1 decisions and assumptions into their logs
([`docs/decisions.md`](../../docs/decisions.md),
[`docs/assumptions.md`](../../docs/assumptions.md)), wrote the product vision with
a boundary and system context diagram
([`docs/product-vision.md`](../../docs/product-vision.md)), added the user-story
and task issue forms and the Markdown check to CI, and prepared a prototype of
the riskiest part (debugging a generated exercise in the user's own VS Code).
User stories are opened as GitHub issues from the `user-story` form.

**What we found out we were wrong about:** we had assumed the gallery and
multi-language support belonged in the minimal product and that the "choose a
problem kind" story was about a technical catalogue. The customer told us the
story set was too ambitious: both the multi-language and the gallery stories
should come out of the candidate, and the real intent of the catalogue story
was to choose an exercise the learner had not yet practiced, not to browse a
list ([DEC-005](../../docs/decisions.md#dec-005),
[DEC-007](../../docs/decisions.md#dec-007)). They also pushed back that we
target only non-beginners, saying complete beginners should be accommodated as
long as instructions are clear ([DEC-002](../../docs/decisions.md#dec-002)).

## Coverage table

| Deliverable | Artifact |
| ----------- | -------- |
| Kickoff action points | `## Previous action points` in [`meeting-report.md`](./meeting-report.md) |
| Kickoff open questions | `## Previous open questions` in [`meeting-report.md`](./meeting-report.md) |
| Product vision | [`docs/product-vision.md`](../../docs/product-vision.md) |
| System context diagram | `docs/architecture/context.<ext>` and its source, embedded in [`docs/product-vision.md`](../../docs/product-vision.md) (TODO — team supplies) |
| Assumptions | [`docs/assumptions.md`](../../docs/assumptions.md) |
| Decisions | [`docs/decisions.md`](../../docs/decisions.md) |
| Story issues | the `US-nn` issues, filtered by the `user-story` label ([list](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues?q=is%3Aissue+label%3Auser-story)) |
| Issue forms | `.github/ISSUE_TEMPLATE/user-story.yml`, `.github/ISSUE_TEMPLATE/task.yml`, `.github/ISSUE_TEMPLATE/config.yml` |
| Labels | the repository's labels page, with `user-story`, `task`, and the `moscow:*` labels |
| Pull request template | `.github/pull_request_template.md` |
| Prototypes | [`prototypes.md`](./prototypes.md) |
| Meeting script | [`meeting-script.md`](./meeting-script.md) |
| Customer validation | [`meeting-report.md`](./meeting-report.md), and [`meeting-transcript.md`](./meeting-transcript.md) when there is one |
| AI usage | [`ai-usage.md`](./ai-usage.md) |

## Minimum Usable Product Candidate

Core task: a learner chooses a problem kind, gets a generated exercise for it,
debugs it in their own VS Code, and verifies the fix against the harness.

- [US-01: Choose a problem kind and receive a generated exercise](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/19)
- [US-02: See a catalogue of problem kinds](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/21)
- [US-03: Connect VS Code to the exercise environment](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/22)
- [US-04: Verify the fix against the harness](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/23)

Customer's verdict: the customer accepted the candidate but advised making the
story set less ambitious, pulling out the multi-language and gallery stories
([DEC-005](../../docs/decisions.md#dec-005)). The core task they confirmed is:
go to the site, get an exercise, connect to the server, solve the bug, get the
harness verdict, and finish.

## What changed because of the customer's feedback

The prototype confirmed that debugging in the user's own installed IDE stays
the priority, so [`DEC-004`](../../docs/decisions.md#dec-004) records the local
debugging experience with files available locally as the confirmed direction.
The customer's insistence that the success state must not be changeable
([DEC-006](../../docs/decisions.md#dec-006)) makes the harness non-modifiable,
and that a learner must be able to run the module and push edits back to the
server becomes a follow-up for the next iteration.

## Repository evidence

| Evidence | Link / location |
| -------- | --------------- |
| A merged pull request that closed its task issue | *TODO — PR link* |
| Latest green link check run | *TODO — Actions run link* |
| Latest green Markdown check run on `main` | *TODO — Actions run link* |

## Deviations

None

## Privacy confirmation

No private-only material was committed to this repository. The meeting
recording and any private identity mapping live only in the Moodle submission,
not here.
