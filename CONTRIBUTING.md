# Contributing

Debugging Gym is developed by team 8 in the ITPD course. This file says how we work; the [Definition of done](docs/definition-of-done.md) says what done means for a story, a task, and a pull request.

## How a change gets in

Every change to `main` goes through a pull request. `main` is protected: it requires a pull request, at least one approval from a member other than the author, and the author cannot approve their own pull request.

The one exception is the very first commit, which went directly to `main` in Week 1.

### Branches

Name a branch after the task issue it closes: `#<task-number>-<short-slug>`, for example `#12-connect-vs-code`.

### Pull requests

A pull request:

- closes exactly one task issue, and its description starts with `Closes #<task-number>`;
- links the story (`US-nn`) it works on, when it works on one;
- ticks the pull request acceptance criteria in the template;
- records, in its description, the decisions made and how the change was checked;
- adds a changelog line to `CHANGELOG.md` under `[Unreleased]` when the change is user-visible.

### Review

The reviewer is a member other than the author. Before approving, the reviewer ticks every acceptance criterion on the task issue and checks the repository checks are green: the [link check](.github/workflows/lychee.yml) and the [Markdown check](.github/workflows/markdown.yml).

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/): a type, an optional scope, and a short description.

```text
feat: generate an exercise for a chosen problem kind
fix(harness): report the planted defect as present
docs: write the threshold of success
ci: pin the docs-site workflow action
```

A commit message is lowercase, imperative, and one line where possible.

## Views in the GitHub project

We use the project's table view to run the week. It shows the `Responsible` and `Accountable` fields, the built-in `Assignees` and `Milestone`, and is sorted by `Milestone` so each sprint's issues read together.

- [The project](https://github.com/orgs/Team8TemporaryName/projects/1)

The schedule lives on the issues and in their sprint milestones; the project is a view over them, not a second backlog. An issue is scheduled by assigning it to its sprint's GitHub milestone and setting the two field values and the matching assignees in the same act.

## Definition of done

The [Definition of done](docs/definition-of-done.md) is the single source for what done means. This file does not restate it; read it before you open a pull request.
