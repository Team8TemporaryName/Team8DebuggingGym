# Architecture

This document records the architecture of the Debugging Gym product, and [the product vision](../product-vision.md) is the scope it serves.

## Drivers

- **Business goals:** [the threshold of success](../threshold-of-success.md) holds the goals the architecture serves.
- **Constraints:** the product vision's [constraints section](../product-vision.md#constraints) holds the conditions the architecture lives inside.
- **Functional requirements:** the [functional requirements index](../functional-requirements/README.md) holds the behavior the architecture must deliver.
- **Quality requirements:** the [quality requirements index](../quality-requirements/README.md) holds the quality the architecture must meet, and it is also the priority matrix.

## Container View

The product runs as the containers below, and [`ADR-001`](adr/ADR-001.md) decides that split and the stack it runs on.

![Container view](container.svg)

### Container Responsibilities

| Container | Responsibilities |
| --------- | ---------------- |
| `webapp` | Serves the catalogue of problem kinds and the exercise generation; returns the attach configuration; verifies a fix against the harness; owns the gallery requests and the session lifecycle |
| `debug-runtime` | Runs a learner's exercise and the harness in isolation; exposes a Debug Adapter Protocol server the learner's VS Code attaches to; owns the learner's uploaded source for the lifetime of the session |
| `database` | Stores the instructor-curated gallery and the results each learner records; owns the problem metadata, the authors, and the result history |
| `vscode-extension` | Brings the choose, generate, verify, and task flow into the learner's own VS Code; calls the webapp API over HTTP; owns the learner's active exercise reference in the editor |

## Diagrams And Legends

Solid boxes are the product's containers and dashed boxes are external actors or systems; an arrow is one exchange, labelled with the protocol or event that crosses it.
The image is [`container.svg`](./container.svg), and its Mermaid source is [`container.mmd`](./container.mmd), generated to match the diagram's containers and arrows.

## Architectural Decisions

| ADR | Status | Addresses | Decision |
| --- | ------ | --------- | -------- |
| [ADR-001](adr/ADR-001.md) | Accepted | [FR-001](../functional-requirements/fr/FR-001.md), [FR-002](../functional-requirements/fr/FR-002.md), [FR-003](../functional-requirements/fr/FR-003.md), [FR-004](../functional-requirements/fr/FR-004.md), [FR-005](../functional-requirements/fr/FR-005.md), [FR-006](../functional-requirements/fr/FR-006.md), [QR-02](../quality-requirements/qr/QR-02.md), [QR-03](../quality-requirements/qr/QR-03.md) | One webapp, a debug runtime, a database, and a VS Code extension |
| [ADR-002](adr/ADR-002.md) | Accepted | [FR-004](../functional-requirements/fr/FR-004.md), [QR-01](../quality-requirements/qr/QR-01.md) | Attach the learner's VS Code over the Debug Adapter Protocol |
| [ADR-003](adr/ADR-003.md) | Accepted | [FR-002](../functional-requirements/fr/FR-002.md), [QR-02](../quality-requirements/qr/QR-02.md) | Generate exercises with an LLM and a deterministic fallback |
