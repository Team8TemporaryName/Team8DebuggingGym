# Product Features

This page describes what learners and instructors can do with Debugging Gym. It provides an overview of the product's main features and links to the related user stories, functional requirements, and architectural decisions. The detailed terms used below are defined in the [project glossary](glossary.md).

## Browse debugging exercises

Learners can explore supported [problem kinds](glossary.md#problem-kind) and browse instructor-curated problems in the [gallery](glossary.md#gallery).

**Stories:**

- [US-02: See a catalogue of problem kinds](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/21)
- [US-07: Browse a public gallery of community exercises](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/26)

**Behavior:**

- [FR-001: Catalogue of Problem Kinds](functional-requirements/fr/FR-001.md)
- [FR-005: Curated Gallery of Problems](functional-requirements/fr/FR-005.md)

## Prepare exercises

Instructors can prepare self-contained [exercises](glossary.md#exercise) for learners to practise.

**Stories:**

- [US-01: Generate a debugging exercise](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/19)

**Behavior:**

- [FR-002: Exercise Generation](functional-requirements/fr/FR-002.md)

**Decisions:**

- [DEC-010: Exercise Generation and Access](decisions.md#dec-010)
- [DEC-011: Public Gallery](decisions.md#dec-011)
- [ADR-001: Architecture Decision Record](architecture/adr/ADR-001.md)

## Debug exercises in VS Code

Learners can work on an exercise in their own [VS Code extension](glossary.md#vs-code-extension) and connect to its [debug runtime](glossary.md#debug-runtime).

**Stories:**

- [US-03: Debug an exercise in VS Code](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/22)

**Behavior:**

- [FR-004: VS Code Integration](functional-requirements/fr/FR-004.md)
- [FR-006: Exercise Workspace](functional-requirements/fr/FR-006.md)
- [FR-007: Debugging Environment](functional-requirements/fr/FR-007.md)

**Decisions:**

- [DEC-004: Learner Uses Own IDE](decisions.md#dec-004)
- [DEC-012: VS Code Extension](decisions.md#dec-012)
- [DEC-015: VS Code as Priority IDE](decisions.md#dec-015)
- [ADR-001: Architecture Decision Record](architecture/adr/ADR-001.md)

## Run the harness and verify a fix

Learners can inspect and run the local [harness](glossary.md#harness), then receive an official verification result from the server.

**Stories:**

- [US-04: Run the exercise harness](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/23)
- [US-10: Verify an exercise solution](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/63)
- [US-11: Receive verification results](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/64)

**Behavior:**

- [FR-003: Exercise Verification](functional-requirements/fr/FR-003.md)
- [FR-008: Local Harness](functional-requirements/fr/FR-008.md)
- [FR-009: Verification Results](functional-requirements/fr/FR-009.md)

**Decisions:**

- [DEC-016: Server-Side Sandboxing](decisions.md#dec-016)
- [DEC-017: Local Harness and Official Verification](decisions.md#dec-017)
- [ADR-001: Architecture Decision Record](architecture/adr/ADR-001.md)

## Work on multi-file exercises

Learners can work on an [exercise](glossary.md#exercise) containing multiple related files in one workspace.

**Stories:**

- [US-12: Work with multi-file exercises](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/65)

**Behavior:**

- [FR-010: Multi-file Exercises](functional-requirements/fr/FR-010.md)

**Decisions:**

- [DEC-014: Multi-file Exercises](decisions.md#dec-014)
- [DEC-018: Exercise Workspace and Versioning](decisions.md#dec-018)
- [ADR-001: Architecture Decision Record](architecture/adr/ADR-001.md)

## Store exercises and browse the server library

Teachers' generated exercises are stored on the server, and learners can browse and reopen the available exercises.

**Stories:**

- [US-13: Store exercises on the server](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/84)
- [US-16: Browse and solve exercises](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/87)

**Behavior:** [FR-011](functional-requirements/fr/FR-011.md)

## Teacher and student access

Teachers can enter the teacher interface with an access key and create named exercises. Student accounts are a later Should Have capability.

**Stories:**

- [US-14: Teacher/student interfaces](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/85)
- [US-15: Teacher exercise generation](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/86)
- [US-18: Student and teacher accounts](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/89)

**Behavior:** [FR-012](functional-requirements/fr/FR-012.md), [FR-013](functional-requirements/fr/FR-013.md), [FR-018](functional-requirements/fr/FR-018.md)

## Extension download and learner progress

Learners can download the VS Code extension from the web app and see which server exercises they have completed.

**Stories:**

- [US-17: Download the VS Code extension](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/88)
- [US-19: Track completed exercises](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/90)

**Behavior:** [FR-014](functional-requirements/fr/FR-014.md), [FR-015](functional-requirements/fr/FR-015.md)

## Product analytics and operational observability

The product records core-task events and exposes operating signals so the team can understand usage and diagnose failures.

**Stories:**

- [US-20: Product analytics](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/91)
- [US-21: Operational observability](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/92)

**Behavior:** [FR-016](functional-requirements/fr/FR-016.md), [FR-017](functional-requirements/fr/FR-017.md), [QR-05](quality-requirements/qr/QR-05.md)

**Architecture:** [ADR-005](architecture/adr/ADR-005.md), [ADR-006](architecture/adr/ADR-006.md)
