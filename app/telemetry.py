"""Privacy-conscious analytics event validation and delivery."""

from __future__ import annotations

import logging
import os
from typing import Any
from uuid import uuid4

import httpx

logger = logging.getLogger(__name__)

EVENT_SCHEMAS = {
    "app_opened": {"first_visit"},
    "exercise_started": {"exercise_id", "kind"},
    "exercise_generated": {"exercise_id", "kind", "generator"},
    "verification_run": {"exercise_id", "passed"},
    "exercise_completed": {"exercise_id", "kind"},
}

VALID_SOURCES = {"web", "usability-test", "smoke"}


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
        raise ValueError(
            f"{event_name} is missing required properties: {sorted(missing)}"
        )

    source = properties.get("source")
    if source not in VALID_SOURCES:
        raise ValueError(f"Invalid analytics source: {source}")


async def track_event(
    event_name: str,
    learner_id: str,
    properties: dict[str, Any],
) -> bool:
    """Send an event when analytics is configured.

    Analytics delivery failures must never interrupt application work.
    Invalid event schemas are programmer errors and should still raise.
    """
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
