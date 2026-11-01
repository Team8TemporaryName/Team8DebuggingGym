# Product Features

This page describes what learners and instructors can do with Debugging Gym. The detailed terms used below are defined in the [project glossary](glossary.md).

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
- [US-01: Choose a problem kind and receive a generated exercise](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/19)

**Behavior:**
- [FR-002: Exercise Generation](functional-requirements/fr/FR-002.md)

**Decisions:**
- [DEC-010: Exercise Generation and Access](decisions.md)
- [DEC-011: Public Gallery of Instructor-Curated Problems](decisions.md)
- [ADR-001: Architecture](architecture/adr/ADR-001.md)
## Debug exercises in VS Code

Learners can work on an exercise in their own [VS Code extension](glossary.md#vs-code-extension) and connect to its [debug runtime](glossary.md#debug-runtime).

**Stories:**
- [US-03: Connect VS Code to an exercise environment](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/22)

**Behavior:**
- [FR-004: Debugging Environment](functional-requirements/fr/FR-004.md)
- [FR-006: Exercise Workspace](functional-requirements/fr/FR-006.md)
- [FR-007: VS Code Integration](functional-requirements/fr/FR-007.md)

**Decisions:**
- [DEC-004: Debug in the Learner's Own IDE](decisions.md)
- [DEC-012: VS Code Extension](decisions.md)
- [DEC-015: VS Code Extension Priority](decisions.md)
- [ADR-001: Architecture](architecture/adr/ADR-001.md)
## Run the harness and verify a fix

Learners can inspect and run the local [harness](glossary.md#harness), then receive an official verification result from the server.

**Stories:**
- [US-04: Verify a fix against the harness](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/23)
- [US-11: Run Harness Locally and Trust Official Verdict](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/64)
- [US-10: Understand Verification Results at a Glance](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/63)

**Behavior:**
- [FR-003: Exercise Verification](functional-requirements/fr/FR-003.md)
- [FR-008: Local Harness Execution](functional-requirements/fr/FR-008.md)
- [FR-009: Verification Results](functional-requirements/fr/FR-009.md)

**Decisions:**
- [DEC-016: Server-Side Sandboxing](decisions.md)
- [DEC-017: Local Harness Editing and Official Verification](decisions.md)
- [ADR-001: Architecture](architecture/adr/ADR-001.md)
## Work on multi-file exercises

Learners can work on an [exercise](glossary.md#exercise) containing multiple related files in one workspace.

**Stories:**
- [US-12: Work on Multi-File Debugging Exercises](https://github.com/Team8TemporaryName/Team8DebuggingGym/issues/65)

**Behavior:**
- [FR-010: Multi-File Exercises](functional-requirements/fr/FR-010.md)

**Decisions:**
- [DEC-014: Multi-File Exercises](decisions.md)
- [DEC-018: Exercise Workspace and Versioning](decisions.md)
- [ADR-001: Architecture](architecture/adr/ADR-001.md)
