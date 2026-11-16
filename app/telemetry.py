"""Telemetry for Debugging Gym.

Two pipelines, both optional:

- Analytics events (Part 3): an HTTP POST per action to the analytics backend
  (OpenPanel). Event delivery is attempted when the OpenPanel credentials are
  configured; missing credentials disable delivery.
- Observability signals (Part 5): a structured log line per request plus an
  OpenTelemetry histogram, exported over OTLP/HTTP to OpenObserve. Turned on by
  ``OBSERVABILITY_ENABLED``.

Every event carries a ``source`` field with a closed set of values: ``web``,
``usability-test``, or ``smoke``. ``smoke`` marks the team's own pipeline check
and a metric excludes it. Events carry an opaque ``learner_id``, never personal
data.

The observability pipeline uses the OpenTelemetry SDK with the OTLP/HTTP
exporter. The histogram ``request_duration_ms`` (labelled ``route`` and
``outcome``) and the per-request structured log line are exported to the
OpenObserve backend, which accepts OTLP. This is disabled unless
``OBSERVABILITY_ENABLED`` is set, and an unavailable exporter never breaks the
product (FR-017, issue #80 AC-08..AC-11).
"""

from __future__ import annotations

import logging
import os
import re
import secrets
from typing import Any
from uuid import uuid4

import httpx

logger = logging.getLogger(__name__)
EVENT_SCHEMAS = {
    "app_opened": {"first_visit"},
    "exercise_started": {"exercise_id"},
    "exercise_generated": {"exercise_id", "generator"},
    "verification_run": {"exercise_id", "passed"},
    "exercise_completed": {"exercise_id"},
}

# OpenObserve OTLP/HTTP endpoint. The base is the OpenObserve HTTP address, for
# example http://<university-vm-ipv4>:5080; the OTLP/HTTP exporter appends the
# signal path and the organization. The token is an OpenObserve stream token,
# private-only and installed on the VM.
OPENOBSERVE_URL = os.environ.get("OPENOBSERVE_URL", "http://localhost:5080")
OPENOBSERVE_TOKEN = os.environ.get("OPENOBSERVE_TOKEN", "")
OBSERVABILITY_ORGANIZATION = os.environ.get("OBSERVABILITY_ORGANIZATION", "default")

# SLI-01's export windows, per docs/observability.md: the log exporter's batch
# interval is five seconds and the metric exporter's is one minute.
LOG_EXPORT_INTERVAL_SECONDS = 5
METRIC_EXPORT_INTERVAL_SECONDS = 60

_STRUCTURED_LOGGER = logging.getLogger("debugging_gym.requests")

# Lazily-built OpenTelemetry meter/logger so an import never fails when the SDK
# is absent or observability is off.
_METER = None
_HISTOGRAM = None
_OUTCOME_COUNTER = None
_RELEASE_HISTOGRAM = None
_VERIFICATION_HISTOGRAM = None
_LOGGER_PROVIDER = None

VALID_SOURCES = {"web", "usability-test", "smoke"}

OBSERVABILITY_ENABLED = os.environ.get("OBSERVABILITY_ENABLED", "false").lower() == "true"


def new_learner_id() -> str:
    """Generate a random opaque learner identifier."""
    return f"learner_{uuid4().hex}"


def _opaque_id() -> str:
    """A random opaque identifier, not derived from personal data."""
    return secrets.token_hex(8)


def validate_event(
    event_name: str,
    properties: dict[str, Any],
) -> None:
    """Reject unknown events and events missing required properties."""
    if event_name not in EVENT_SCHEMAS:
        raise ValueError(f"Unknown analytics event: {event_name}")
    missing = EVENT_SCHEMAS[event_name] - properties.keys()
    if missing:
        raise ValueError(f"{event_name} is missing required properties: {sorted(missing)}")

    source = properties.get("source")
    if source not in VALID_SOURCES:
        raise ValueError(f"Invalid analytics source: {source}")


async def track_event(
    event_name: str,
    learner_id: str,
    properties: dict[str, Any],
) -> bool:
    """Validate and send an event to OpenPanel when configured."""
    validate_event(event_name, properties)

    endpoint = os.getenv(
        "OPENPANEL_API_URL",
        "https://api.openpanel.dev/track",
    )
    client_id = os.getenv("OPENPANEL_CLIENT_ID", "")
    client_secret = os.getenv("OPENPANEL_CLIENT_SECRET", "")

    if not all((endpoint, client_id, client_secret)):
        return False

    payload = {
        "type": "track",
        "payload": {
            "name": event_name,
            "profileId": learner_id,
            "properties": properties,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                endpoint,
                json=payload,
                headers={
                    "openpanel-client-id": client_id,
                    "openpanel-client-secret": client_secret,
                },
            )
            response.raise_for_status()
        return True
    except httpx.HTTPError:
        logger.exception("Analytics delivery failed: %s", event_name)
        return False


def _ensure_observability() -> bool:
    """Build the OpenTelemetry meter and logger once, if observability is on."""
    global \
        _METER, \
        _HISTOGRAM, \
        _OUTCOME_COUNTER, \
        _RELEASE_HISTOGRAM, \
        _LOGGER_PROVIDER, \
        _VERIFICATION_HISTOGRAM
    if not OBSERVABILITY_ENABLED:
        return False
    if _METER is not None:
        return True
    try:
        from opentelemetry import metrics
        from opentelemetry.exporter.otlp.proto.http._log_exporter import (
            OTLPLogExporter,
        )
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
            OTLPMetricExporter,
        )
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({"service.name": "debugging-gym"})

        metric_headers = {}
        if OPENOBSERVE_TOKEN:
            metric_headers["Authorization"] = f"Basic {OPENOBSERVE_TOKEN}"
        metric_exporter = OTLPMetricExporter(
            endpoint=f"{OPENOBSERVE_URL}/api/{OBSERVABILITY_ORGANIZATION}/v1/metrics",
            headers=metric_headers,
        )
        metric_reader = PeriodicExportingMetricReader(
            metric_exporter,
            export_interval_millis=METRIC_EXPORT_INTERVAL_SECONDS * 1000,
        )
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
        _METER = metrics.get_meter("debugging-gym")
        _HISTOGRAM = _METER.create_histogram(
            "request_duration_ms",
            description="HTTP request response time in milliseconds",
            unit="ms",
        )
        _OUTCOME_COUNTER = _METER.create_counter(
            "request_outcome",
            description="HTTP request outcomes, labelled by outcome (SLI-03 availability)",
            unit="1",
        )
        _RELEASE_HISTOGRAM = _METER.create_histogram(
            "debug_runtime_release_ms",
            description="Time to release a debug runtime after a session ends (SLI-04)",
            unit="ms",
        )
        _VERIFICATION_HISTOGRAM = _METER.create_histogram(
            "verification_duration_ms",
            description="Time to verify a user's solution (SLI-02)",
            unit="ms",
        )

        log_headers = {}
        if OPENOBSERVE_TOKEN:
            log_headers["Authorization"] = f"Basic {OPENOBSERVE_TOKEN}"
        log_exporter = OTLPLogExporter(
            endpoint=f"{OPENOBSERVE_URL}/api/{OBSERVABILITY_ORGANIZATION}/v1/logs",
            headers=log_headers,
        )
        _LOGGER_PROVIDER = LoggerProvider(resource=resource)
        _LOGGER_PROVIDER.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        logging.getLogger().addHandler(
            LoggingHandler(level=logging.INFO, logger_provider=_LOGGER_PROVIDER)
        )
        return True
    except Exception:
        # If the SDK is missing or misconfigured, telemetry must not break the
        # product; fall back to the no-op path.
        return False


def emit_request_signal(request_id: str, route: str, outcome: str, duration_ms: float) -> None:
    """Emit the per-request structured log line and the histogram point.

    The log line is ``SLI-01``'s per-request point; the histogram feeds its
    aggregate query. Both are no-ops unless observability is enabled (AC-11).
    The histogram is ``request_duration_ms`` labelled ``route`` and ``outcome``
    and exported over OTLP/HTTP to OpenObserve (AC-08). The structured log
    carries ``request_id``, ``route``, ``outcome``, and ``duration_ms`` (AC-09).
    """
    if not _ensure_observability():
        return

    # Sanitize so that histograms are counted per route, not per route-excersize
    sanitized_route = re.sub(r"/ex-.{6}", r"/ex-XXXXXX", route)

    _STRUCTURED_LOGGER.info(
        "request",
        extra={
            "request_id": request_id,
            "route": route,
            "outcome": outcome,
            "duration_ms": duration_ms,
        },
    )
    _HISTOGRAM.record(duration_ms, {"route": sanitized_route, "outcome": outcome})
    _OUTCOME_COUNTER.add(1, {"outcome": outcome})


def emit_runtime_release(release_ms: float, reason: str, within_budget: bool) -> None:
    """Emit the debug-runtime release signal (SLI-04).

    ``release_ms`` is the time from the session ending to the runtime being
    stopped and its source removed; ``reason`` is ``exception``,
    ``resource_exhaustion``, or ``disconnect``; ``within_budget`` is whether the
    release finished within the one-minute budget of QR-03. A no-op unless
    observability is enabled.
    """
    if not _ensure_observability():
        return
    _RELEASE_HISTOGRAM.record(
        release_ms,
        {"reason": reason, "within_budget": "yes" if within_budget else "no"},
    )


def emit_verification_duration(verification_ms: float) -> None:
    """Emit the exercise verification latency signal (SLI-04).

    ``verification_ms`` is the time the harness runner verifies the task for
    """
    if not _ensure_observability():
        return
    _VERIFICATION_HISTOGRAM.record(verification_ms)
