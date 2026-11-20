# Observability

The signals this product reports about its own operation, the service level indicators they define, and the pipeline that stores them.
The product's diagnosability requirement is read through the staging organization's log query, and the dashboard is the evidence that the pipeline stored and rendered it.

## The Signals

The product emits metrics for active `SLI`s, and it emits a structured log line for every HTTP request because `SLI-01`'s per-request point is read from it.
The trace span is optional, and the team emits none this week.
An alert is a rule over a signal rather than a signal of its own, and the team defines none this week.
The active telemetry records request response time and HTTP request outcomes (`SLI-01` and the application-side request-success indicator shown as `SLI-03`). `SLI-03` is not an independent external availability monitor and does not satisfy `QR-04`; its deployed QRT remains Not verified. Verification latency (`SLI-02`) and actual debug-runtime release (`SLI-04`) remain planned.

## The SLIs

An `SLI` is a quality signal the product emits and the pipeline records.
Its target is the `Response Measure` of the requirement whose test reads it.

### SLI-01

Request response time.

- **Status:** Active
- **Definition:** The five-minute P95 of the `webapp`'s HTTP request response time, in milliseconds, computed from an OpenTelemetry histogram labelled `route` and `outcome`, where `outcome` is `ok`, `client_error`, or `server_error`.
  The per-request point is a structured log line carrying `request_id`, `route`, `outcome`, and `duration_ms`, which the environment's organization stores and a query finds by `request_id`.
  `duration_ms` is the elapsed time from the `webapp` receiving the request to its response completing, measured on a monotonic clock, and it is the same observation the histogram records.
- **Unit:** Milliseconds.
- **Window:** Five minutes, evaluated every minute; the per-request log line is queryable in the environment's organization within five seconds of the response, and the aggregate point follows within one minute.
- **Source:** An OpenTelemetry histogram the `webapp` exports over OTLP/HTTP to OpenObserve, and a structured log line the `webapp` emits for every request, exported over OTLP logs to the same instance.
- **Query:** `histogram_quantile(0.95, sum by (le, route, outcome) (rate(request_duration_ms_bucket[5m])))`

### SLI-02

Exercise verification latency.

- **Status:** Planned
- **Definition:** The five-minute P95 of the `webapp`'s exercise verification response time, in milliseconds, labelled `exercise_id` and `outcome`. This supports the runtime verification requirement's signal.
- **Unit:** Milliseconds.
- **Window:** Five minutes, evaluated every minute.
- **Source:** An OpenTelemetry histogram the `webapp` exports over OTLP/HTTP to OpenObserve for the `verify` route.
- **Query:** `histogram_quantile(0.95, sum by (le, outcome) (rate(verification_duration_ms_bucket[5m])))`

### SLI-03

Availability.

- **Status:** Active
- **Definition:** The fraction of HTTP requests handled by the `webapp` that complete successfully (`outcome="ok"`) out of all recorded HTTP request outcomes, measured over a seven-day window. This is an application-side request-success indicator, not the independent one-minute external probe required by [`QR-04`](quality-requirements/qr/QR-04.md), and must not be used as evidence that QR-04 passes.
- **Unit:** Percentage.
- **Window:** Seven days, evaluated every minute.
- **Source:** An OpenTelemetry counter of request outcomes (`request_outcome`) the `webapp` increments for every request with an `outcome` label (`ok`, `client_error`, `server_error`), exported over OTLP/HTTP to OpenObserve.
- **Query:** `100 * sum(rate(request_outcome{outcome="ok"}[7d])) / sum(rate(request_outcome[7d]))`

### SLI-04

Debug-runtime release.

- **Status:** Planned
- **Definition:** The fraction of ended debug sessions whose runtime is stopped and source removed within one minute of the session ending. This is the measure of the security/resistance requirement [`QR-03`](quality-requirements/qr/QR-03.md): a session ends by exception, resource exhaustion, or disconnect, and a fresh session starts from a clean runtime.
- **Unit:** Percentage.
- **Window:** One minute per session end, evaluated on each session end.
- **Source:** An OpenTelemetry histogram of the time to release a runtime (`debug_runtime_release_ms`) the `webapp` records when a debug session ends, labelled by `reason` (`exception`, `resource_exhaustion`, `disconnect`) and `within_budget` (`yes`/`no`), exported over OTLP/HTTP to OpenObserve.
- **Query:** `100 * sum by (reason) (rate(debug_runtime_release_ms_count{within_budget="yes"}[1m])) / sum by (reason) (rate(debug_runtime_release_ms_count[1m]))`

## The Pipeline

The `webapp` container emits the active signals: a structured log line per request, an OpenTelemetry request-duration histogram, and a request-outcome counter for each handled HTTP request, all exported over OTLP/HTTP to OpenObserve. No independent external availability-probe counter is currently implemented.
The observability backend is OpenObserve, self-hosted on the university VM, with one environment scope per environment: a `staging` organization and a `production` organization, each with its own dashboard.
The metric export interval is ten seconds and the log exporter's batch interval is one second, so the per-request log point appears within five seconds and the aggregate within one minute, meeting `SLI-01`'s `**Window:**`.
The temporary workspace used by local verification is cleaned up after the subprocess exits. This is not the complete runtime teardown measured by QR-03, so it does not produce an SLI-04 measurement.
The page records the retention as 30 days, which covers the longest `SLI` window (the seven-day availability window of `SLI-03`).
Collection is enabled by the environment variable `OBSERVABILITY_ENABLED` (default `false`); when disabled, the `webapp` emits no signal.
The deployment's steps and configuration live in [`docs/deployment.md`](deployment.md#observability-deployment), which this page links and does not repeat.
The backend, its dashboards, and their credentials are reachable by the team and the customer from the university network, and their addresses and credentials are private-only.

## The Dashboard

Each environment scope's dashboard carries at least one chart for each `Active` `SLI` (`SLI-01` and `SLI-03`), named after the `SLI`, which runs the `**Query:**` recorded in its section.
The `staging` scope's dashboard shows the test traffic; the `production` scope's dashboard carries the same charts and queries and is not exercised with test traffic.
The dashboard's address and credentials are private-only and are never tracked.
Evidence is two sanitized screenshots, one per scope, in `reports/week-06/images/`, linked from the weekly report.

## Collected Data

The signals collect a `request_id`, `route`, `outcome`, `duration_ms`, histogram bucket labels, and HTTP request-outcome counts; the data lives in the OpenObserve instance on the university VM.
The product never collects a personal name, an email address, a phone number, a postal address, free text, or payment data; the `request_id` is an opaque random identifier, not derived from personal data.
Collection is disabled by setting `OBSERVABILITY_ENABLED=false`.
