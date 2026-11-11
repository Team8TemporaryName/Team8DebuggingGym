"""Telemetry for Debugging Gym.

Two pipelines, both optional and off by default:

- Analytics events (Part 3): an HTTP POST per action to the analytics backend
  (OpenPanel). Turned on by ``ANALYTICS_ENABLED``.
- Observability signals (Part 5): a structured log line per request plus an
  OpenTelemetry histogram, exported over OTLP/HTTP to OpenObserve. Turned on by
  ``OBSERVABILITY_ENABLED``.

Every event carries a ``source`` field with a closed set of values: ``web``,
``usability-test``, or ``smoke``. ``smoke`` marks the team's own pipeline check
and a metric excludes it. Events carry an opaque ``learner_id``, never personal
data.
"""

from __future__ import annotations

import logging
import os
import secrets
from typing import Any

import httpx

ANALYTICS_ENABLED = os.environ.get("ANALYTICS_ENABLED", "false").lower() == "true"
OBSERVABILITY_ENABLED = os.environ.get("OBSERVABILITY_ENABLED", "false").lower() == "true"

ANALYTICS_URL = os.environ.get("ANALYTICS_URL", "http://localhost:5081/api")
ANALYTICS_TOKEN = os.environ.get("ANALYTICS_TOKEN", "")

_STRUCTURED_LOGGER = logging.getLogger("debugging_gym.requests")


def _opaque_id() -> str:
    """A random opaque identifier, not derived from personal data."""
    return secrets.token_hex(8)


def track(event: str, fields: dict[str, Any], *, source: str = "web") -> None:
    """Send one analytics event to the analytics backend.

    ``source`` is ``web``, ``usability-test``, or ``smoke``; ``smoke`` marks a
    pipeline check. Collection is a no-op unless analytics is enabled.
    """
    if not ANALYTICS_ENABLED:
        return
    payload = {"event": event, "source": source, **fields}
    try:
        headers = {"Authorization": f"Bearer {ANALYTICS_TOKEN}"} if ANALYTICS_TOKEN else {}
        httpx.post(
            f"{ANALYTICS_URL}/events",
            json=payload,
            headers=headers,
            timeout=2.0,
        )
    except httpx.HTTPError:
        # Telemetry must never break the product.
        pass


def smoke_pipeline_check() -> None:
    """Send a staging ``smoke`` event the team uses to verify the pipeline.

    Only smoke is excluded from a metric; this check is how staging verifies the
    pipeline end to end without polluting a metric.
    """
    track(
        "app_opened",
        {"learner_id": _opaque_id(), "first_visit": True},
        source="smoke",
    )


def emit_request_signal(request_id: str, route: str, outcome: str, duration_ms: float) -> None:
    """Emit the per-request structured log line and the histogram point.

    The log line is ``SLI-01``'s per-request point; the histogram feeds its
    aggregate query. Both are no-ops unless observability is enabled.
    """
    if not OBSERVABILITY_ENABLED:
        return
    _STRUCTURED_LOGGER.info(
        "request",
        extra={
            "request_id": request_id,
            "route": route,
            "outcome": outcome,
            "duration_ms": duration_ms,
        },
    )
    # OpenTelemetry histogram export would go here via OTLP; the slice logs the
    # point so a query can read it. The aggregate query is defined in docs.
