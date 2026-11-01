"""Run the QR-04 availability check against the staging deployment.

The script deliberately reads the staging URL from STAGING_BASE_URL and never
writes that URL to the evidence file. Run it from a campus-connected machine.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

DEFAULT_DURATION_SECONDS = 7 * 24 * 60 * 60
DEFAULT_INTERVAL_SECONDS = 60
DEFAULT_TIMEOUT_SECONDS = 5
REQUIRED_AVAILABILITY = 99.9


def _valid_base_url(base_url: str) -> bool:
    parsed = urlparse(base_url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _probe_endpoint(base_url: str, path: str, timeout_seconds: float) -> dict[str, Any]:
    """Return a sanitized result for one staging endpoint probe."""
    started = time.monotonic()
    result: dict[str, Any] = {
        "path": path,
        "ok": False,
        "status": None,
        "elapsed_ms": None,
        "error": None,
    }
    url = base_url.rstrip("/") + path
    try:
        # `urlopen` follows no application-specific redirects itself; an HTTP
        # redirect ultimately yields the final response and its status here.
        with urlopen(url, timeout=timeout_seconds) as response:
            status = int(response.status)
            body = response.read(1_000_000)
        result["status"] = status
        ok = 200 <= status < 300
        if ok and path == "/api/kinds":
            try:
                kinds = json.loads(body.decode("utf-8"))
                ok = isinstance(kinds, dict) and bool(kinds)
            except (UnicodeDecodeError, json.JSONDecodeError):
                ok = False
                result["error"] = "response was not a non-empty JSON object"
        result["ok"] = ok
        if not ok and result["error"] is None:
            result["error"] = "endpoint did not return an acceptable response"
    except HTTPError as exc:
        result["status"] = exc.code
        result["error"] = f"HTTP {exc.code}"
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        # Do not write exception strings that may include a private host URL.
        result["error"] = type(exc).__name__
    finally:
        result["elapsed_ms"] = round((time.monotonic() - started) * 1000, 2)
    return result


def probe_once(base_url: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Probe the root page and API catalogue once; no private URL is recorded."""
    if not _valid_base_url(base_url):
        raise ValueError("STAGING_BASE_URL must be an http:// or https:// base URL")
    endpoints = [
        _probe_endpoint(base_url, "/", timeout_seconds),
        _probe_endpoint(base_url, "/api/kinds", timeout_seconds),
    ]
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "ok": all(endpoint["ok"] for endpoint in endpoints),
        "endpoints": endpoints,
    }


def run_monitor(
    base_url: str,
    *,
    duration_seconds: int = DEFAULT_DURATION_SECONDS,
    interval_seconds: int = DEFAULT_INTERVAL_SECONDS,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    evidence_path: str | Path,
) -> int:
    """Run minute-level checks, writing one sanitized JSON record per sample."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be greater than zero")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if not _valid_base_url(base_url):
        raise ValueError("STAGING_BASE_URL must be an http:// or https:// base URL")

    evidence = Path(evidence_path)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    # Include a sample at t=0 and at the end of an exact-multiple window,
    # so a seven-day run spans all 10,080 one-minute intervals.
    sample_count = duration_seconds // interval_seconds + 1
    started = time.monotonic()
    successful = 0

    print(
        f"Monitoring staging for {duration_seconds}s, every {interval_seconds}s; "
        f"evidence: {evidence} (URL omitted from log).",
        flush=True,
    )

    with evidence.open("w", encoding="utf-8", newline="\n") as output:
        for sample_index in range(sample_count):
            scheduled = started + sample_index * interval_seconds
            delay = scheduled - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            record = probe_once(base_url, timeout_seconds)
            record["sample"] = sample_index + 1
            record["elapsed_seconds"] = round(time.monotonic() - started, 2)
            output.write(json.dumps(record, separators=(",", ":")) + "\n")
            output.flush()
            if record["ok"]:
                successful += 1
            elif record["sample"] == 1 or record["sample"] % 10 == 0:
                print(
                    f"Sample {record['sample']}/{sample_count} failed; "
                    "see sanitized evidence log.",
                    flush=True,
                )

    availability = successful / sample_count * 100
    passed = availability >= REQUIRED_AVAILABILITY
    print(
        f"QR-04 staging availability: {successful}/{sample_count} successful "
        f"checks = {availability:.4f}% (required {REQUIRED_AVAILABILITY:.1f}%).",
        flush=True,
    )
    return 0 if passed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration-seconds",
        type=int,
        default=DEFAULT_DURATION_SECONDS,
        help="monitoring duration; use 604800 for the full seven-day QRT",
    )
    parser.add_argument(
        "--interval-seconds", type=int, default=DEFAULT_INTERVAL_SECONDS
    )
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--evidence",
        type=Path,
        default=Path("reports/week-05/evidence/qr-05-staging-availability.jsonl"),
    )
    args = parser.parse_args(argv)
    base_url = os.environ.get("STAGING_BASE_URL", "")
    if not base_url:
        parser.error("set STAGING_BASE_URL to the staging base URL; do not use production")
    try:
        return run_monitor(
            base_url,
            duration_seconds=args.duration_seconds,
            interval_seconds=args.interval_seconds,
            timeout_seconds=args.timeout_seconds,
            evidence_path=args.evidence,
        )
    except (OSError, ValueError) as exc:
        print(f"QR-04 monitor could not run: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
