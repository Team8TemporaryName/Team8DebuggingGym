# Observability

The signals this product reports about its own operation, the service level indicators they define, and the pipeline that stores them.
The product's diagnosability requirement is read through the staging organization's log query, and the dashboard is the evidence that the pipeline stored and rendered it.

## The Signals

The product emits a metric for every `SLI`, and it emits a structured log line for every HTTP request because `SLI-01`'s per-request point is read from it.
The trace span is optional, and the team emits none this week.
An alert is a rule over a signal rather than a signal of its own, and the team defines none this week.
The observability capability covers each runtime quality requirement: request response time and diagnosis (`SLI-01`), verification latency (`SLI-02`), availability (`SLI-03`), and debug-runtime release (`SLI-04`).

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
- **Definition:** The fraction of successful minute-level availability probes of the `webapp` in a seven-day window, where a probe is successful when the root and the catalogue both respond successfully. This is the measure of the availability requirement [`QR-04`](quality-requirements/qr/QR-04.md). The single counter-metric is a `request_outcome` counter labelled `outcome`; a rising failure count over the window reads the availability directly.
- **Unit:** Percentage.
- **Window:** Seven days, evaluated every minute.
- **Source:** An OpenTelemetry counter of request outcomes (`request_outcome`) the `webapp` increments for every request with an `outcome` label (`ok`, `client_error`, `server_error`), exported over OTLP/HTTP to OpenObserve.
- **Query:** `100 * sum(rate(request_outcome_total{outcome="ok"}[7d])) / (sum(rate(request_outcome_total{outcome="ok"}[7d])) + sum(rate(request_outcome_total{outcome=~"client_error|server_error"}[7d])))`

### SLI-04

Debug-runtime release.

- **Status:** Active
- **Definition:** The fraction of ended debug sessions whose runtime is stopped and source removed within one minute of the session ending. This is the measure of the security/resistance requirement [`QR-03`](quality-requirements/qr/QR-03.md): a session ends by exception, resource exhaustion, or disconnect, and a fresh session starts from a clean runtime.
- **Unit:** Percentage.
- **Window:** One minute per session end, evaluated on each session end.
- **Source:** An OpenTelemetry histogram of the time to release a runtime (`debug_runtime_release_ms`) the `webapp` records when a debug session ends, labelled by `reason` (`exception`, `resource_exhaustion`, `disconnect`) and `within_budget` (`yes`/`no`), exported over OTLP/HTTP to OpenObserve.
- **Query:** `100 * sum by (reason) (rate(debug_runtime_release_within_budget_total{within_budget="yes"}[1m])) / sum by (reason) (rate(debug_runtime_release_total[1m]))`

## The Pipeline

The `webapp` container emits each signal: a structured log line per request, an OpenTelemetry histogram per request, a request-outcome counter per request, and a debug-runtime release metric per ended session, all exported over OTLP/HTTP to OpenObserve.
The observability backend is OpenObserve, self-hosted on the university VM, with one environment scope per environment: a `staging` organization and a `production` organization, each with its own dashboard.
The export interval is one minute for the metric and the log exporter's batch interval is five seconds, so the per-request log point appears within five seconds and the aggregate within one minute, meeting `SLI-01`'s `**Window:**`.
The debug-runtime release metric is emitted when a session ends and is queryable within the same one-minute metric export interval, meeting `SLI-04`'s `**Window:**`.
The page records the retention as 30 days, which covers the longest `SLI` window (the seven-day availability window of `SLI-03`).
Collection is enabled by the environment variable `OBSERVABILITY_ENABLED` (default `false`); when disabled, the `webapp` emits no signal.
The deployment's steps and configuration live in [`docs/deployment.md`](deployment.md#telemetry-pipelines), which this page links and does not repeat.
The backend, its dashboards, and their credentials are reachable by the team and the customer from the university network, and their addresses and credentials are private-only.

## The Dashboard

Each environment scope's dashboard carries at least one chart for each `Active` `SLI` (`SLI-01`, `SLI-03`, and `SLI-04`), named after the `SLI`, which runs the `**Query:**` recorded in its section.
The `staging` scope's dashboard shows the test traffic; the `production` scope's dashboard carries the same charts and queries and is not exercised with test traffic.
The dashboard's address and credentials are private-only and are never tracked.
Evidence is two sanitized screenshots, one per scope, in `reports/week-06/images/`, linked from the weekly report.

## Collected Data

The signals collect a `request_id`, `route`, `outcome`, `duration_ms`, the histogram bucket labels, the request-outcome counts, and the debug-runtime release time and reason; the data lives in the OpenObserve instance on the university VM.
The product never collects a personal name, an email address, a phone number, a postal address, free text, or payment data; the `request_id` is an opaque random identifier, not derived from personal data.
Collection is disabled by setting `OBSERVABILITY_ENABLED=false`.