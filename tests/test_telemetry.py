import asyncio

import httpx

from app.telemetry import (
    EVENT_SCHEMAS,
    new_learner_id,
    track_event,
    validate_event,
)


def test_new_learner_ids_are_unique_and_opaque():
    first = new_learner_id()
    second = new_learner_id()

    assert first.startswith("learner_")
    assert first != second
    assert len(first) == 40


def test_all_event_schemas_accept_valid_properties():
    for event_name, required_fields in EVENT_SCHEMAS.items():
        properties = {
            field: "test-value" for field in required_fields
        }
        properties["source"] = "web"

        validate_event(event_name, properties)


def test_invalid_event_name_is_rejected():
    try:
        validate_event("unknown_event", {"source": "web"})
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown event should be rejected")


def test_missing_required_property_is_rejected():
    try:
        validate_event(
            "exercise_started",
            {"source": "web"},
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Missing event property should be rejected")


def test_invalid_source_is_rejected():
    event_name = next(iter(EVENT_SCHEMAS))
    properties = {
        field: "test-value"
        for field in EVENT_SCHEMAS[event_name]
    }
    properties["source"] = "invalid"

    try:
        validate_event(event_name, properties)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid source should be rejected")


def test_analytics_failure_does_not_interrupt_application(monkeypatch):
    monkeypatch.setenv("OPENPANEL_API_URL", "https://api.openpanel.dev/track")
    monkeypatch.setenv("OPENPANEL_CLIENT_ID", "test-client")
    monkeypatch.setenv("OPENPANEL_CLIENT_SECRET", "test-secret")

    class FailingClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, *args, **kwargs):
            raise httpx.ConnectError("OpenPanel is unavailable")

    monkeypatch.setattr(
        "app.telemetry.httpx.AsyncClient",
        FailingClient,
    )

    result = asyncio.run(
        track_event(
            "app_opened",
            new_learner_id(),
            {
                "first_visit": True,
                "source": "web",
            },
        )
    )

    assert result is False
