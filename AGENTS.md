# Agent Instructions

The course requirements are routed from [`SKILL.md`](https://github.com/inno-itpd/itpd/blob/main/SKILL.md); read the rule before you change anything it checks.

## Layout

- `app/` is the product: the FastAPI web app (`app/main.py`), the exercise generator (`app/generator.py`), the harness runner (`app/harness_runner.py`), and the static front end (`app/static/`).
- `deploy/` holds the debug runtime image and its example exercise; `tests/` holds the product tests.
- `vscode-extension/` is the VS Code extension that brings the choose, generate, and verify flow into the learner's editor; its TypeScript source lives in `vscode-extension/src/`.
- `docs/` holds the maintained artifacts: the vision, the plan, the requirements, the architecture, the decisions, the assumptions, and the glossary.
- `docs/quality-requirements/qr/` and `docs/functional-requirements/fr/` hold one requirement per file, and `docs/architecture/adr/` holds one ADR per file.
- `reports/week-NN/` holds each week's evidence, and is not rewritten after its week.

## Checks

- The Markdown check ([`markdown.yml`](.github/workflows/markdown.yml)) runs `markdownlint-cli2`; the link check ([`lychee.yml`](.github/workflows/lychee.yml)) runs `lychee .` and needs the network.
- The docs site is built by the [`docs-site.yml`](.github/workflows/docs-site.yml) workflow when `docs/` changes.

## Conventions

- Commit messages follow Conventional Commits: `type(scope): summary`, in the imperative, one line where possible.
- Branch names are `<issue-number>-<slug>`, such as `12-connect-vs-code`.
- `main` is protected: every change goes through a pull request that closes exactly one task issue, and the author cannot approve their own pull request.
- Python is formatted with Black and linted with `ruff`; keep the front end consistent with the existing `app/static/` style.
- The VS Code extension is TypeScript: run `npm run compile` in `vscode-extension/` to type-check, and keep its `package.json` and `tsconfig.json` in sync.

## Do Not Edit

- `CHANGELOG.md` is edited only when a release is cut; during a sprint a change adds its line to `[Unreleased]` and touches nothing else.
- `docs/decisions.md` and the records in `docs/architecture/adr/` are edited only by the member accountable for the decision.
- `reports/week-NN/` is not rewritten after its week; carry a change forward in the next week's report instead.
- `.github/workflows/` is edited in its own pull request, so a broken gate cannot hide inside a feature change.
- The prototype under a `prototypes/` folder, when it exists, stays off `main`; keep it on its feature branch.
