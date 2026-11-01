"""Unit tests for the sanitized staging-availability monitor."""

from __future__ import annotations

import json
from unittest.mock import patch

from scripts import qrt_staging_availability as availability


class FakeResponse:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self, limit=-1):
        return self._body[:limit]


def test_probe_once_accepts_root_and_nonempty_api_catalogue():
    responses = [
        FakeResponse(200, b"<html>ok</html>"),
        FakeResponse(200, b'{"off-by-one":{"summary":"demo"}}'),
    ]
    with patch.object(availability, "urlopen", side_effect=responses):
        result = availability.probe_once("http://staging.invalid", timeout_seconds=1)

    assert result["ok"] is True
    assert [item["path"] for item in result["endpoints"]] == ["/", "/api/kinds"]
    assert all(item["ok"] for item in result["endpoints"])
    serialized = json.dumps(result)
    assert "staging.invalid" not in serialized


def test_probe_once_fails_when_catalogue_is_not_valid_json():
    responses = [
        FakeResponse(200, b"<html>ok</html>"),
        FakeResponse(200, b"not json"),
    ]
    with patch.object(availability, "urlopen", side_effect=responses):
        result = availability.probe_once("http://staging.invalid", timeout_seconds=1)

    assert result["ok"] is False
    assert result["endpoints"][1]["ok"] is False


def test_monitor_rejects_invalid_base_url():
    try:
        availability.probe_once("staging.invalid")
    except ValueError as exc:
        assert "STAGING_BASE_URL" in str(exc)
    else:
        raise AssertionError("an invalid base URL should be rejected")
