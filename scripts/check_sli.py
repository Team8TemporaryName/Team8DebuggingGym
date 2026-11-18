"""Run QR-05 QRT-01 against staging and its OpenObserve organization.

Required environment variables:
    STAGING_BASE_URL
    TEACHER_KEY
    OPENOBSERVE_URL
    OBSERVABILITY_ORGANIZATION
    OPENOBSERVE_TOKEN

Optional OpenObserve schema overrides:
    OPENOBSERVE_LOG_STREAM
    OPENOBSERVE_REQUEST_ID_FIELD
    OPENOBSERVE_ROUTE_FIELD
    OPENOBSERVE_OUTCOME_FIELD

OPENOBSERVE_TOKEN is the Base64-encoded username:password value for an
HTTP Basic Authorization header. This script never prints URLs, credentials,
session tokens, or exercise source.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

SLI_01_QUERY = (
    "histogram_quantile(0.95, sum by (le, route, outcome) "
    "(rate(request_duration_ms_bucket[5m])))"
)
LOG_DEADLINE_SECONDS = 5.0
METRIC_DEADLINE_SECONDS = 60.0
RETRY_INTERVAL_SECONDS = 0.25


class CheckError(RuntimeError):
    """A failed precondition or QRT assertion."""


@dataclass(frozen=True)
class Settings:
    staging_url: str
    teacher_key: str
    observe_url: str
    token: str
    staging_commit_sha: str
    stream: str | None
    request_field: str | None
    route_field: str | None
    outcome_field: str | None


def load_settings() -> Settings:
    names = (
        "STAGING_BASE_URL",
        "TEACHER_KEY",
        "OPENOBSERVE_URL",
        "OBSERVABILITY_ORGANIZATION",
        "OPENOBSERVE_TOKEN",
        "STAGING_COMMIT_SHA",
    )
    values = {name: os.getenv(name, "").strip() for name in names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise CheckError("Missing environment variable(s): " + ", ".join(missing))

    staging_url = values["STAGING_BASE_URL"].rstrip("/")
    observe_url = values["OPENOBSERVE_URL"].rstrip("/")
    staging_parts = urlsplit(staging_url)
    observe_parts = urlsplit(observe_url)

    if staging_parts.scheme not in {"http", "https"} or not staging_parts.netloc:
        raise CheckError("STAGING_BASE_URL must be an HTTP(S) application base URL.")
    if observe_parts.scheme not in {"http", "https"} or not observe_parts.netloc:
        raise CheckError("OPENOBSERVE_URL must be an HTTP(S) OpenObserve base URL.")
    if observe_parts.path not in {"", "/"}:
        raise CheckError(
            "OPENOBSERVE_URL must be the server base URL, without /web or another path."
        )
    if values["OBSERVABILITY_ORGANIZATION"].lower() != "staging":
        raise CheckError(
            "This test is staging-only. Set OBSERVABILITY_ORGANIZATION=staging; "
            "the script refuses to query another organization."
        )

    token = values["OPENOBSERVE_TOKEN"]
    if token.lower().startswith("basic "):
        token = token[6:].strip()

    return Settings(
        staging_url=staging_url,
        teacher_key=values["TEACHER_KEY"],
        observe_url=observe_url,
        token=token,
        staging_commit_sha=values["STAGING_COMMIT_SHA"],
        stream=os.getenv("OPENOBSERVE_LOG_STREAM", "").strip() or None,
        request_field=os.getenv("OPENOBSERVE_REQUEST_ID_FIELD", "").strip() or None,
        route_field=os.getenv("OPENOBSERVE_ROUTE_FIELD", "").strip() or None,
        outcome_field=os.getenv("OPENOBSERVE_OUTCOME_FIELD", "").strip() or None,
    )


def _json(raw: bytes) -> Any:
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CheckError("A service returned a response that was not valid JSON.") from exc


def _request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 3.0,
) -> tuple[int, Any, Any]:
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    request = Request(url, data=body, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=max(0.1, timeout)) as response:
            return response.status, response.headers, _json(response.read())
    except HTTPError as exc:
        return exc.code, exc.headers, _json(exc.read())
    except (URLError, TimeoutError, OSError) as exc:
        # Exception text can contain a private URL, so only expose its type.
        raise CheckError(
            f"Network request failed ({type(exc).__name__}); check connectivity and configuration."
        ) from None


def _expect(status: int, expected: int, operation: str) -> None:
    if status == expected:
        return
    if status in {401, 403}:
        reason = "authentication or authorization was rejected"
    elif status == 404:
        reason = "the endpoint or resource was not found"
    else:
        reason = f"the service returned HTTP {status}"
    raise CheckError(f"{operation}: expected HTTP {expected}; {reason}.")


def _oa_headers(settings: Settings) -> dict[str, str]:
    return {
        "Authorization": f"Basic {settings.token}",
        "User-Agent": "Debugging-Gym-QR-05-QRT-01/1.0",
    }


def _oa_url(settings: Settings, path: str) -> str:
    org = quote("staging", safe="")
    return f"{settings.observe_url}/api/{org}/{path.lstrip('/')}"


def _sql_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def _sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _field(record: dict[str, Any], name: str) -> Any:
    if name in record:
        return record[name]
    current: Any = record
    for part in name.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _select_field(
    fields: set[str], logical_name: str, override: str | None
) -> str:
    if override:
        if override not in fields:
            raise CheckError(
                f"The configured {logical_name} field {override!r} is absent from the stream schema."
            )
        return override

    possibilities = (
        logical_name,
        f"attributes.{logical_name}",
        f"log_attributes.{logical_name}",
    )
    matches = [item for item in possibilities if item in fields]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        available = ", ".join(sorted(fields)) or "(empty schema)"
        raise CheckError(
            f"Could not identify {logical_name} in the log stream schema. "
            f"Available fields: {available}. Set OPENOBSERVE_{logical_name.upper()}_FIELD."
        )
    raise CheckError(
        f"Multiple {logical_name} fields match: {', '.join(matches)}. "
        f"Set OPENOBSERVE_{logical_name.upper()}_FIELD explicitly."
    )


def discover_log_schema(
    settings: Settings,
) -> tuple[str, str, str, str]:
    headers = _oa_headers(settings)
    stream = settings.stream

    if stream is None:
        url = _oa_url(settings, "streams") + "?fetchSchema=true&type=logs"
        status, _, response = _request("GET", url, headers=headers)
        _expect(status, 200, "List staging OpenObserve log streams")
        streams = response.get("list", []) if isinstance(response, dict) else []
        if not streams:
            raise CheckError(
                "No log streams were returned for the staging organization. "
                "Check that staging telemetry is enabled and has emitted logs."
            )

        required_fields = {"request_id", "route", "outcome"}
        candidates = []
        for item in streams:
            schema = item.get("schema") or []
            names = {
                field.get("name", "")
                for field in schema
                if isinstance(field, dict) and field.get("name")
            }
            has_request_fields = all(
                any(
                    candidate in names
                    for candidate in (
                        logical,
                        f"attributes.{logical}",
                        f"log_attributes.{logical}",
                    )
                )
                for logical in required_fields
            )
            if has_request_fields and item.get("name"):
                candidates.append(item["name"])

        if len(candidates) != 1:
            choices = ", ".join(str(item.get("name", "?")) for item in streams)
            if candidates:
                reason = "More than one stream contains the request fields: " + ", ".join(candidates)
            else:
                reason = "No stream schema clearly contains request_id, route, and outcome"
            raise CheckError(
                f"{reason}. Available streams: {choices}. "
                "Inspect the schema and set OPENOBSERVE_LOG_STREAM."
            )
        stream = candidates[0]

    schema_url = _oa_url(
        settings,
        f"streams/{quote(stream, safe='')}/schema?type=logs",
    )
    status, _, schema_response = _request("GET", schema_url, headers=headers)
    _expect(status, 200, "Read the selected staging log stream schema")
    schema = (
        schema_response.get("schema", [])
        if isinstance(schema_response, dict)
        else []
    )
    fields = {
        item.get("name", "")
        for item in schema
        if isinstance(item, dict) and item.get("name")
    }

    return (
        stream,
        _select_field(fields, "request_id", settings.request_field),
        _select_field(fields, "route", settings.route_field),
        _select_field(fields, "outcome", settings.outcome_field),
    )


def _commit_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _staging_request(
    settings: Settings,
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 5.0,
) -> tuple[int, Any, Any]:
    request_headers = {"User-Agent": "Debugging-Gym-QR-05-QRT-01/1.0"}
    if headers:
        request_headers.update(headers)
    url = f"{settings.staging_url}/{path.lstrip('/')}"
    return _request(
        method, url, headers=request_headers, payload=payload, timeout=timeout
    )


def create_deliberate_failure(
    settings: Settings,
) -> tuple[str, str, float, float]:
    status, _, kinds = _staging_request(settings, "/api/kinds")
    _expect(status, 200, "Read staging exercise-kind catalogue")
    if not isinstance(kinds, dict) or not kinds:
        raise CheckError("Staging returned an empty or invalid exercise-kind catalogue.")
    kind = sorted(kinds)[0]

    status, _, auth = _staging_request(
        settings,
        "/api/auth/teacher",
        method="POST",
        payload={"key": settings.teacher_key},
    )
    _expect(status, 200, "Authenticate as a staging teacher")
    session = auth.get("session") if isinstance(auth, dict) else None
    if not session:
        raise CheckError("Teacher authentication returned no session token.")

    status, _, exercise = _staging_request(
        settings,
        "/api/exercises",
        method="POST",
        payload={"kind": kind},
        headers={"x-session": session},
    )
    _expect(status, 200, "Create staging exercise")
    exercise_id = exercise.get("id") if isinstance(exercise, dict) else None
    if not exercise_id:
        raise CheckError("Exercise creation returned no exercise ID.")

    request_started = time.time()
    status, response_headers, error_body = _staging_request(
        settings,
        f"/api/exercises/{quote(str(exercise_id), safe='')}/verify",
        method="POST",
        payload={},
        timeout=4.0,
    )
    response_monotonic = time.monotonic()
    if status != 400:
        raise CheckError(
            f"The deliberate verification request returned HTTP {status}, not HTTP 400."
        )
    detail = error_body.get("detail") if isinstance(error_body, dict) else None
    if detail != "missing source":
        raise CheckError(
            "The HTTP 400 response was not the expected missing-source validation."
        )
    request_id = (
        response_headers.get("x-request-id") if response_headers else None
    )
    if not request_id:
        raise CheckError("The HTTP 400 response did not contain x-request-id.")

    return str(exercise_id), str(request_id), request_started, response_monotonic


def find_request_log(
    settings: Settings,
    stream: str,
    request_field: str,
    route_field: str,
    outcome_field: str,
    exercise_id: str,
    request_id: str,
    request_started: float,
    response_monotonic: float,
) -> float:
    deadline = response_monotonic + LOG_DEADLINE_SECONDS
    sql = (
        f"SELECT * FROM {_sql_identifier(stream)} "
        f"WHERE {_sql_identifier(request_field)} = {_sql_string(request_id)} "
        "ORDER BY _timestamp DESC"
    )
    url = _oa_url(settings, "_search")
    headers = _oa_headers(settings)
    start_time = int((request_started - 10) * 1_000_000)
    last_problem = "no matching log point returned"

    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        payload = {
            "query": {
                "sql": sql,
                "start_time": start_time,
                "end_time": int((time.time() + 1) * 1_000_000),
                "from": 0,
                "size": 10,
            },
            "search_type": "other",
            "timeout": 1,
        }
        try:
            status, _, response = _request(
                "POST",
                url,
                headers=headers,
                payload=payload,
                timeout=min(1.25, remaining),
            )
            if status >= 500:
                last_problem = f"OpenObserve returned HTTP {status}"
            elif status != 200:
                _expect(status, 200, "Query staging request logs")
            else:
                hits = response.get("hits", []) if isinstance(response, dict) else []
                if hits:
                    if len(hits) != 1:
                        raise CheckError(
                            "Expected exactly one request log point, "
                            f"but OpenObserve returned {len(hits)}."
                        )
                    point = hits[0]
                    if _field(point, request_field) != request_id:
                        raise CheckError("The returned log point has a different request ID.")
                    expected_route = f"/api/exercises/{exercise_id}/verify"
                    if _field(point, route_field) != expected_route:
                        raise CheckError("The returned log point has the wrong verification route.")
                    if _field(point, outcome_field) != "client_error":
                        raise CheckError("The returned log point outcome is not client_error.")
                    return time.monotonic() - response_monotonic
        except CheckError as exc:
            message = str(exc)
            if "HTTP 5" not in message and not message.startswith("Network request failed"):
                raise
            last_problem = message

        time.sleep(min(RETRY_INTERVAL_SECONDS, max(0, deadline - time.monotonic())))

    raise CheckError(
        "The matching log point with the expected route and client_error outcome "
        f"did not appear within five seconds ({last_problem})."
    )


def query_sli_01(
    settings: Settings, response_monotonic: float
) -> tuple[str, float, float]:
    deadline = response_monotonic + METRIC_DEADLINE_SECONDS
    url = _oa_url(settings, "prometheus/api/v1/query")
    headers = _oa_headers(settings)
    last_problem = "no numeric failure series returned"

    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        params = urlencode({"query": SLI_01_QUERY, "time": str(time.time())})
        try:
            status, _, response = _request(
                "GET",
                f"{url}?{params}",
                headers=headers,
                timeout=min(3.0, remaining),
            )
            if status >= 500:
                last_problem = f"OpenObserve returned HTTP {status}"
            elif status != 200:
                _expect(status, 200, "Execute SLI-01 PromQL query")
            elif response.get("status") != "success":
                last_problem = "OpenObserve did not report a successful PromQL query"
            else:
                data = response.get("data", {})
                series_list = data.get("result", []) if isinstance(data, dict) else []
                for series in series_list:
                    labels = series.get("metric", {})
                    route = str(labels.get("route", ""))
                    if labels.get("outcome") != "client_error":
                        continue
                    if not route.startswith("/api/exercises/") or not route.endswith("/verify"):
                        continue
                    value = series.get("value")
                    if not isinstance(value, list) or len(value) < 2:
                        continue
                    try:
                        p95_ms = float(value[1])
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(p95_ms):
                        return route, p95_ms, time.monotonic() - response_monotonic
                last_problem = "the query returned no numeric client_error verification series"
        except CheckError as exc:
            message = str(exc)
            if "HTTP 5" not in message and not message.startswith("Network request failed"):
                raise
            last_problem = message

        time.sleep(min(1.0, max(0, deadline - time.monotonic())))

    raise CheckError(
        "The SLI-01 five-minute P95 query did not return a numeric client_error "
        f"verification series within one minute ({last_problem})."
    )


def main() -> int:
    try:
        settings = load_settings()
        print("QR-05 QRT-01 — staging diagnosability check")
        print("Environment: staging")
        print(f"Staging deployment commit: {settings.staging_commit_sha}")
        print(f"Script checkout commit: {_commit_sha()}")

        stream, request_field, route_field, outcome_field = discover_log_schema(
            settings
        )
        print(f"OpenObserve log stream: {stream}")

        exercise_id, request_id, request_started, response_monotonic = (
            create_deliberate_failure(settings)
        )
        route = f"/api/exercises/{exercise_id}/verify"
        print("Deliberate verification response: HTTP 400 (missing source)")
        print(f"Request ID: {request_id}")

        log_elapsed = find_request_log(
            settings,
            stream,
            request_field,
            route_field,
            outcome_field,
            exercise_id,
            request_id,
            request_started,
            response_monotonic,
        )
        print(f"Log request ID: {request_id}")
        print(f"Log route: {route}")
        print("Log outcome: client_error")
        print(f"Log point found after response: {log_elapsed:.2f}s (deadline: 5s)")

        metric_route, p95_ms, metric_elapsed = query_sli_01(
            settings, response_monotonic
        )
        print(f"SLI-01 failure route: {metric_route}")
        print("SLI-01 outcome: client_error")
        print(f"SLI-01 five-minute P95: {p95_ms:.3f} ms")
        print(
            f"SLI-01 series found after response: {metric_elapsed:.2f}s "
            "(deadline: 60s)"
        )
        print("Result: PASS — the QR-05 response measures were met.")
        return 0
    except CheckError as exc:
        print(f"QRT-01 FAILED: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("QRT-01 interrupted by the operator.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
