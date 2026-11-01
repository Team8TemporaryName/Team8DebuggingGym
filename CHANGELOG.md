# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.0](https://github.com/Team8TemporaryName/Team8DebuggingGym/releases/tag/v0.5.0) - 2026-11-1

### Added

- A Debugging Gym sidebar in VS Code that lists the problem kinds, generates exercises, and verifies a fix against the harness.
- Each exercise now opens in its own folder (with the program, an editable harness, and the task), versioned in a local git repository.

### Changed

- Exercise verification now runs under pytest, so the learner sees the standard expected-vs-got output and stack traces.
- The exercise harness is now an editable pytest file.

## [0.1.1](https://github.com/Team8TemporaryName/Team8DebuggingGym/releases/tag/v0.1.1) - 2026-10-25

### Added

- A VS Code extension that brings the choose, generate, and verify flow into the learner's editor (`vscode-extension/`).
- Syntax highlighting for the exercise program and harness in the web app.

### Changed

- The web app harness run now shows a busy/loading state, and passes horizontally for long output.
- A finish button completes an exercise and returns the learner to the problem kinds.

## [0.1.0](https://github.com/Team8TemporaryName/Team8DebuggingGym/releases/tag/v0.1.0) - 2026-10-24

### Added

- Choose a debugging problem kind from a catalogue.
- Get a generated exercise for the chosen kind.
- Edit the exercise program and verify the fix against a harness.
- A launch configuration to connect the learner's own VS Code to the debug environment over the Debug Adapter Protocol.
- A documentation site and setup page.
- A test suite asserting every generated exercise starts with a planted defect.
