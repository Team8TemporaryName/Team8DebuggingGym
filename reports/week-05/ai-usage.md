# Week 5 AI usage report

This report names the AI tools used in Week 5, what each was used for, and what was done with its output.

## GitHub Copilot

- **Used for:** expanding the automated test suite — the generator tests (`tests/test_generator.py`), the harness-runner tests (`tests/test_harness_runner.py`), and the web-app API tests (`tests/test_webapp_api.py`) — from the single existing `test_mup.py`.
- **Used for:** writing the quality requirement tests (`QRT-nn` sections in `QR-01`..`QR-04`) and the quality requirement testing plan in `docs/project-plan.md`.
- **Used for:** building the self-hosted production stack — `deploy/webapp.Dockerfile`, `docker-compose.yml`, and `docs/deployment.md`.
- **Used for:** filling the Week 5 meeting report, sprint retrospective, and decisions (`DEC-020`..`DEC-025`) and settling assumptions from the uploaded meeting transcript.
- **What was done with the output:** the tests were run and verified against the repository (`pytest` passes, 28 tests), the documentation was linked into `docs/index.md`, the deployment was aligned to the course rule that it is manual from the university network rather than a CI job, and the meeting outcomes were derived from the transcript and checked against the course requirements. No private-only material was included.

## Other tools

- **Used for:** retrieving the Week 5 assignment scope and the course requirement files (releases, planning, weekly report, quality requirements, sprint ceremonies) from the course repository.
- **What was done with the output:** the requirement shapes were read and followed when writing the artifacts above.
