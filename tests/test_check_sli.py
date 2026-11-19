from __future__ import annotations

import time

from scripts.check_sli import Settings, query_sli_01


def test_query_sli_01_accepts_finite_post_response_range_sample(monkeypatch):
    now = time.time()
    response_wall_time = now - 2.0
    response_monotonic = time.monotonic() - 1.0
    settings = Settings(
        staging_url="http://staging.example",
        observe_url="http://openobserve.example",
        organization="staging-org-id",
        query_token="test-credential",
        stream=None,
        request_field=None,
        route_field=None,
        outcome_field=None,
    )
    response = {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [
                {
                    "metric": {
                        "route": "/api/exercises/ex-XXXXXX/verify",
                        "outcome": "client_error",
                    },
                    "values": [
                        [response_wall_time - 1.0, "3.5"],
                        [response_wall_time + 0.5, "NaN"],
                        [response_wall_time + 1.0, "4.75"],
                        [response_wall_time + 1.5, "NaN"],
                    ],
                }
            ],
        },
    }
    observed = {}

    def fake_request(method, url, **kwargs):
        observed["method"] = method
        observed["url"] = url
        return 200, {}, response

    monkeypatch.setattr("scripts.check_sli._request", fake_request)

    route, p95_ms, elapsed = query_sli_01(
        settings,
        response_monotonic,
        response_wall_time,
    )

    assert observed["method"] == "GET"
    assert "/prometheus/api/v1/query_range?" in observed["url"]
    assert route == "/api/exercises/ex-XXXXXX/verify"
    assert p95_ms == 4.75
    assert elapsed >= 0
