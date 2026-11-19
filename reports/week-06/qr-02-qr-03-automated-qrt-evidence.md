# Week 06 — Automated QRT evidence

This record captures the automated quality-requirement checks executed by Product code CI on the Issue #81 branch.

- **Workflow:** [Product code CI — run 44610074054](https://github.com/Team8TemporaryName/Team8DebuggingGym/actions/runs/44610074054)
- **Commit checked:** `98354a509fd1c41dba85411aadc47369ef6aab35`
- **Execution environment:** GitHub Actions, `ubuntu-latest`, fresh checkout
- **Toolchains:** Python 3.11 and Node.js 22
- **Test command:** `python -m pytest tests/ -q`
- **Result:** `64 passed, 2 warnings in 6.36s`

The workflow also passed Ruff lint/format, the VS Code extension TypeScript type-check, and the extension build.

## QR-02 QRT-02 — CI testability

**Result: Passes.**

The Product code CI workflow starts from a fresh checkout, installs the documented Python and Node.js dependencies, and executes the complete pytest suite.

Relevant automated coverage includes:

- `tests/test_generator.py` exercises the generator catalogue, generated exercise structure, deterministic fallback, and unknown-kind rejection.
- `tests/test_frontend.py` launches `tests/test_frontend.cjs` with Node.js. The Node tests load `app/static/app.js` and exercise catalogue selection, exercise display, and passing/failing verification-result flows.
- The workflow step runs the full `python -m pytest tests/ -q` command, not a subset.

This satisfies QR-02 QRT-02's clean-checkout CI pass criterion. The CI run linked above is the evidence.

## QR-03 QRT-03 — Local verification workspace cleanup

**Result: Passes.**

The same full pytest run includes `tests/test_runtime_cleanup.py`. Its two tests verify that:

1. A normally completed local verification removes its temporary workspace.
2. A timed-out local verification removes its temporary workspace and reports the timeout as not passed.

Both tests passed in the CI run linked above.

**Scope boundary:** QRT-03 verifies the local subprocess workspace used by the harness runner. It does not establish that a deployed Docker runtime is stopped or that remote session source is removed; that is the separate manual QR-03 QRT-04.

## Review of the OpenObserve dashboard

The [staging dashboard screenshot](images/qr-05-qrt-01-staging-openobserve-dashboard.png) is a point-in-time view (Past 15 Minutes) and displays:

- **SLI-01:** the `client_error` verification route with a 4.75 ms five-minute P95. This is the QR-05 QRT-01 result recorded in [its staging evidence](qr-05-qrt-01-evidence.md).
- **SLI-02:** an exercise-verification-latency series (the screenshot displays 242.50 ms).
- **SLI-03:** an availability value of 94.06% in that dashboard view. This is not the full seven-day observation required by QR-04 QRT-05, which remains ongoing.
- **SLI-04:** a 100% release value for the `disconnect` reason. This alone does not establish all three QR-03 QRT-04 termination cases. In addition, the current `SLI-04` emission is called by the local harness runner when its temporary workspace is released; the dashboard therefore must not be treated as proof of remote deployed Docker-runtime cleanup.

The dashboard does not record the end-to-end VS Code attach attempts and timings required by QR-01 QRT-01. That test remains unverified until its ten fresh attempts are recorded.

Accordingly, only QR-02 QRT-02 and QR-03 QRT-03 are marked `Passes` from this CI run. The incomplete/manual and seven-day tests retain their existing `Not verified` status.
