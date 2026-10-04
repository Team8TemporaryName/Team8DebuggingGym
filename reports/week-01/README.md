# Week 1 report — Debugging Gym

**Project:** Debugging Gym · **Team number:** 8

> **Problem space.** Software developers and programming-language learners want
> targeted, hands-on practice that trains a specific debugging skill, but the
> existing platforms offer general exercises rather than exercises for a
> particular kind of debugging problem.

## Summary

Week 1 is a research week: no code, no prototype, nothing to deploy. We
defined the problem space, searched widely for alternatives
([`candidate-list.md`](./candidate-list.md)), researched three of them
([`alternatives.md`](../docs/research/alternatives.md)), compared them on six
properties fixed in advance ([`comparison.md`](../docs/research/comparison.md)),
and derived three gaps ([`gap-analysis.md`](../docs/research/gap-analysis.md))
and four value propositions
([`value-proposition.md`](../docs/research/value-proposition.md)).

**What we found.** No mainstream product combines debugging *specificity*, on
-demand exercise *generation*, and debugging in the *user's own IDE*. CodinGame
and LeetCode have the audience and feedback loop but train writing correct
code, not debugging, and run in a browser; Rustlings has the "fix the broken
file" model in the user's own environment but is Rust-only, fixed-content, and
has no gallery. That absence is the seed of the project.

**What we propose.** **Debugging Gym** — a site that generates an exercise for
a chosen *named debugging problem kind* with an LLM, lets the user connect from
VS Code and debug it with their own tooling, and collects exercises in a public
gallery. The gaps are targeted practice (GAP-01), fresh exercises on demand
(GAP-02), and the user's own IDE (GAP-03). The assumptions behind this are
listed in the value proposition and are exactly what we test in the customer
kickoff.

## Coverage table

| Deliverable | Artifact |
| ----------- | -------- |
| Project definition / problem space | [README](../README.md) |
| Candidate list | [`candidate-list.md`](./candidate-list.md) |
| Alternatives search | [`docs/research/alternatives.md`](../docs/research/alternatives.md) |
| Compare the alternatives | [`docs/research/comparison.md`](../docs/research/comparison.md) |
| Gap analysis | [`docs/research/gap-analysis.md`](../docs/research/gap-analysis.md) |
| Value proposition | [`docs/research/value-proposition.md`](../docs/research/value-proposition.md) |
| Research board | [Link to research board](https://www.figma.com/design/7bwb24mxusLGMo43t5VsVH/Untitled) |
| Meeting script | [`meeting-script.md`](./meeting-script.md) |
| Customer kickoff | [`meeting-report.md`](./meeting-report.md), and [`meeting-transcript.md`](./meeting-transcript.md) |
| AI usage | [`ai-usage.md`](./ai-usage.md) |
| License | [`LICENSE`](../../LICENSE) |

## Repository evidence

These three items prove things only the platform's own interface can prove;
none is visible in the repository files.

| Evidence | Link / location |
|----------|-----------------|
| `main` branch protection screenshot | [`reports/week-01/images/branch-protection.png`](./reports/week-01/images/branch-protection.png) |
| Merged PR approved by another member | [Link](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/3) |
| Latest green link check run | [Link](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/37218041214) |

- **Excluded links:**
```
# Returns 403 to the checker.
# Verified manually in a browser on 2026-10-04.
  - '^https://leetcode\.com/'
# Returns 403 to the checker.
# Verified manually in a browser on 2026-10-04.
  - '^https://www\.hackerearth\.com/'
```

## Contribution table

| GitHub username | Commits | Issues  | Pull requests | Reviews |
|-----------------|---------|---------|---------------|---------|
| Tedor49         | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/393fc7a7630c8f97a9a38d4a3326ba74600a3d6b) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/e25143fdbaa675e31c330425abfcaca0b90cfa67) [3](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/3051048e52430f443428438bba1a8650c31cc835) [4](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/dc7b6774c3c61d69f5f77d209b982e560a532ac8) [5](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/32fc0b25731019a796119f4379c36353882ce5be) [6](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/57590cd30a2d7655f75d99bf21f27ede071c1cf4)     | None    | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/1) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/2) [3](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/3) [4](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/4)       | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/6) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/7) [3](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/8) [4](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/9)     |
| Magel0n         | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/6d1d9e776fd8af6fe52dcc4fb16194b306ec32cb) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/606aaed1cde834a0a89ea4ff27b12acbe73dda0c)     | None    | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/8) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/9)           | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/1) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/4)     |
| NikitaRUniverse | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/870a67ec9ae5596b4f9638f2d78efadb746aaf62) [2](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/239cc9b4572475d03b93d31ff952f0c7b1cacb2e) [3](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/8cacf5465fb094d987f8ed4b07a40c646f35b95d)     | None    | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/6)           | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/3)    |
| Doosuur14       | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/commit/aa6bd314e78f043c9c3138f68bcc4506a6b5b346)     | None    | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/7)           | [1](https://github.com/Team8TemporaryName/Team8DebuggingGym/pull/2 )     |

## Deviations

None

## Privacy confirmation

No private-only material was committed to this repository. The meeting
recording and any private identity mapping live only in the Moodle submission,
not here.