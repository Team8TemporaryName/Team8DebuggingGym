# Observability

This page is the product observability plan for Debugging Gym. It records the signals the application currently emits, the service level indicator (SLI) planned for request health, and the remaining work required to collect and display that SLI.

The related runtime requirement is [QR-05](quality-requirements/qr/QR-05.md). Deployment configuration and release procedures belong in the [Deployment Runbook](deployment.md), not duplicated here.

## The Signals

The product has three possible signal types:

- **Metrics:** numerical measurements aggregated over time. The request-duration histogram needed by SLI-01 is planned but is not currently exported.
- **Logs:** per-request Python logging records emitted by `app/telemetry.py` when `OBSERVABILITY_ENABLED=true`. Each record is created with `request_id`, `route`, `outcome`, and `duration_ms` fields.
- **Traces:** distributed traces are not currently emitted.

The request middleware in `app/main.py` measures each request with a monotonic clock and classifies its outcome as `ok`, `client_error`, or `server_error`. The telemetry function currently writes the per-request logging record only; it does not create an OpenTelemetry histogram or export telemetry to OpenObserve.

No alert rules are currently configured.

## The SLIs

### SLI-01

Request response time and outcome.

**Status:** Planned

**Definition:** The 95th percentile of HTTP request duration, grouped by route and outcome, over a rolling five-minute window. Each request also has an individual diagnostic log record carrying its request identifier, route, outcome, and duration.

**Unit:** Milliseconds (ms).

**Window:** Rolling five minutes, evaluated once per minute. These are the intended aggregation settings; end-to-end collection and query latency have not yet been verified.

**Source:** The request middleware in `app/main.py` measures duration and calls `telemetry.emit_request_signal` in `app/telemetry.py`. The per-request log record is implemented behind `OBSERVABILITY_ENABLED`. The OpenTelemetry histogram and export to OpenObserve remain to be implemented.

**Query:** Planned PromQL-style query for the histogram once its exporter and metric backend are implemented:

```promql
histogram_quantile(
  0.95,
  sum by (le, route, outcome) (
    rate(request_duration_ms_bucket[5m])
  )
)
```

The query is a target definition, not a claim that the metric is currently available. The dashboard must use this same query when the histogram pipeline is operational.

## The Pipeline

The intended backend is OpenObserve, with separate staging and production environment scopes. The deployment runbook describes the university VM deployment boundary and private configuration handling: [Deployment Runbook](deployment.md).

Current implementation status:

- The application can emit per-request Python log records when `OBSERVABILITY_ENABLED=true`.
- `OBSERVABILITY_ENABLED` defaults to `false`; collection is therefore disabled unless explicitly enabled in the runtime environment.
- The application does not currently configure an OpenTelemetry histogram exporter or send the request metric to OpenObserve.
- OpenObserve deployment, staging/production scopes, retention settings, and export intervals have not been verified in this repository.

Do not treat the pipeline as operational until the exporter and backend are configured and a staging request has been found in the backend.

## The Dashboard

The intended dashboard is one dashboard per environment scope:

- **Request health (staging):** contains the SLI-01 chart and staging request traffic.
- **Request health (production):** contains the same SLI-01 query and production request traffic.

The dashboards and charts are not yet evidenced as deployed. Once available, add sanitized screenshots for both scopes under the relevant `reports/week-NN/images/` directory and link them from that week's report. Do not commit credentials, private backend addresses, or sensitive query results.

## Collected Data

When observability is enabled, the request logging record contains:

- `request_id`: opaque request identifier, supplied by the caller or generated randomly by the application.
- `route`: request URL path.
- `outcome`: `ok`, `client_error`, or `server_error`.
- `duration_ms`: request duration measured in milliseconds.

The current request signal does not intentionally include learner names, email addresses, phone numbers, postal addresses, passwords, access keys, authentication tokens, or request bodies. Do not add those fields to request telemetry.

Collection is disabled by default and can be disabled by setting `OBSERVABILITY_ENABLED=false`. The application currently logs locally through Python's logging system; centralized storage and retention are not yet configured or verified.
