# Week 4 AI usage report

This report names the AI tools used in Week 4, what each was used for, and what was done with its output.

## GitHub Copilot

- **Used for:** drafting the Week 4 maintained artifacts — the quality requirements, the functional requirements, the architecture document, the architectural decision records, the glossary, and the `AGENTS.md` — from the course assignment and requirements.
- **Used for:** building the first VS Code extension (`vscode-extension/`) that brings the choose–generate–verify flow into the learner's editor, and the web-app UX polish the customer asked for in Week 3 (code highlighting, a loading/busy state on the harness run, horizontal scrolling, and a finish button).
- **Used for:** updating the container view, `ADR-001`, `ADR-002`, `FR-006`, the glossary, and `QR-01` so the documentation matches the new extension and reflects the customer feedback from Week 3.
- **Used for:** completing the Week 4 meeting report, the decisions (`DEC-014`..`DEC-019`), and the settled assumptions and quality-requirement wording from the customer meeting transcript.
- **What was done with the output:** the draft files were reviewed against the course requirements, corrected to the required field order and identifier rules, and committed to the repository. The extension was reviewed for correctness (exercise persistence, HTTP API calls, error paths) and the web app was verified end to end with `pytest` and a `TestClient` smoke test (6 tests passing). Meeting outcomes were derived strictly from the transcript. No private-only material was included.

## Other tools

- **Used for:** retrieving the Week 4 assignment and the course requirement files from the course repository.
- **What was done with the output:** the requirement shapes were read and followed when writing the artifacts above.
