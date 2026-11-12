"""Telemetry for Debugging Gym.

Supports OpenPanel analytics, the existing optional analytics pipeline,
and request observability. Telemetry failures must never interrupt
application functionality.
"""

from __future__ import annotations

import logging
import os
import secrets
from typing import Any
from uuid import uuid4

import httpx

logger = logging.getLogger(__name__)
_STRUCTURED_LOGGER = logging.getLogger("debugging_gym.requests")

EVENT_SCHEMAS = {
    "app_opened": {"first_visit"},
    "exercise_started": {"exercise_id", "kind"},
    "exercise_generated": {"exercise_id", "kind", "generator"},
    "verification_run": {"exercise_id", "passed"},
    "exercise_completed": {"exercise_id", "kind"},
}

VALID_SOURCES = {"web", "usability-test", "smoke"}

ANALYTICS_ENABLED = os.environ.get("ANALYTICS_ENABLED", "false").lower() == "true"
OBSERVABILITY_ENABLED = os.environ.get("OBSERVABILITY_ENABLED", "false").lower() == "true"
ANALYTICS_URL = os.environ.get("ANALYTICS_URL", "http://localhost:5081/api")
ANALYTICS_TOKEN = os.environ.get("ANALYTICS_TOKEN", "")


def new_learner_id() -> str:
    """Generate a random opaque learner identifier."""
    return f"learner_{uuid4().hex}"


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


def track(
    event: str,
    fields: dict[str, Any],
    *,
    source: str = "web",
) -> None:
    """Send an event through the existing optional analytics pipeline."""
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
        pass


def smoke_pipeline_check() -> None:
    """Send a staging smoke event to verify the analytics pipeline."""
    track(
        "app_opened",
        {
            "learner_id": secrets.token_hex(8),
            "first_visit": True,
        },
        source="smoke",
    )


def emit_request_signal(
    request_id: str,
    route: str,
    outcome: str,
    duration_ms: float,
) -> None:
    """Emit a structured request log when observability is enabled."""
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
