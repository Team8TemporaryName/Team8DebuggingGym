# Debugging Gym

**Team:** 8 · **Project:** Debugging Gym

> **Problem space.** Software developers and programming-language learners want
> targeted, hands-on practice that trains a specific debugging skill, but the
> existing platforms offer general exercises rather than exercises for a
> particular kind of debugging problem.

**Debugging Gym** is a site that generates debugging exercises for a chosen
problem category using an LLM and lets users connect from VS Code and debug
them as they would debug real code. A public gallery collects community
exercises.

This is the course repository for the Debugging Gym project. Week 1 was a
research week (no product); Week 2 turned that direction into requirements and
a prototype; Week 3 built the minimum usable product. This README describes the
project and points at the weekly artifacts.

## Getting started

- **Documentation site:** <https://team8temporaryname.github.io/Team8DebuggingGym/>
- **Setup and run:** [docs/setup.md](docs/setup.md)
- **Maintained documentation:** under [`docs/`](docs/)
- **Current week's report:** [`reports/week-03/README.md`](reports/week-03/README.md)

To run the product, follow [docs/setup.md](docs/setup.md). A clean checkout,
then the setup page, completes the core task end to end.

## Repository layout

```text
.
├── README.md                 # this file
├── LICENSE                   # MIT
├── .gitignore
├── .lycheeignore
├── .markdownlint-cli2.jsonc
├── .github/
│   ├── dependabot.yml
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── user-story.yml
│   │   ├── task.yml
│   │   └── config.yml
│   └── workflows/
│       ├── lychee.yml
│       └── markdown.yml
├── docs/
│   ├── decisions.md
│   ├── assumptions.md
│   ├── product-vision.md
│   ├── architecture/
│   └── research/
│       ├── alternatives.md
│       ├── comparison.md
│       ├── gap-analysis.md
│       └── value-proposition.md
├── app/                         # the product (FastAPI + static front end)
│   ├── main.py
│   ├── generator.py
│   ├── harness_runner.py
│   └── static/
├── requirements.txt
├── .env.example
├── CHANGELOG.md
├── CONTRIBUTING.md
└── reports/
    ├── week-01/
    ├── week-02/
    └── week-03/
```

## Research index

| Deliverable | Artifact |
| ----------- | -------- |
| Project definition | [README](./README.md) |
| Candidate list | [`reports/week-01/candidate-list.md`](reports/week-01/candidate-list.md) |
| Alternatives research | [`docs/research/alternatives.md`](docs/research/alternatives.md) |
| Comparison | [`docs/research/comparison.md`](docs/research/comparison.md) |
| Gap analysis | [`docs/research/gap-analysis.md`](docs/research/gap-analysis.md) |
| Value proposition | [`docs/research/value-proposition.md`](docs/research/value-proposition.md) |
| Decisions | [`docs/decisions.md`](docs/decisions.md) |
| Assumptions | [`docs/assumptions.md`](docs/assumptions.md) |
| Product vision | [`docs/product-vision.md`](docs/product-vision.md) |
| Quality requirements | [`docs/quality-requirements/README.md`](docs/quality-requirements/README.md) |
| Functional requirements | [`docs/functional-requirements/README.md`](docs/functional-requirements/README.md) |
| Architecture | [`docs/architecture/README.md`](docs/architecture/README.md) |
| Glossary | [`docs/glossary.md`](docs/glossary.md) |
| Week 1 report | [`reports/week-01/README.md`](reports/week-01/README.md) |
| Week 2 report | [`reports/week-02/README.md`](reports/week-02/README.md) |
| Week 3 report | [`reports/week-03/README.md`](reports/week-03/README.md) |
| Week 4 report | [`reports/week-04/README.md`](reports/week-04/README.md) |
| Threshold of success | [`docs/threshold-of-success.md`](docs/threshold-of-success.md) |
| Project plan | [`docs/project-plan.md`](docs/project-plan.md) |
| Risk register | [`docs/risks.md`](docs/risks.md) |
| Definition of done | [`docs/definition-of-done.md`](docs/definition-of-done.md) |
| Contributing guide | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Agent instructions | [`AGENTS.md`](AGENTS.md) |
| Setup and run | [`docs/setup.md`](docs/setup.md) |

## License

MIT — see [LICENSE](LICENSE).
