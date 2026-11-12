
"""Debugging Gym — MUP slice web application.

FastAPI backend serving a minimal web front end. A learner chooses a problem
kind, gets a generated exercise, connects their own VS Code to a debug
environment, and verifies the fix against the harness.
"""

from __future__ import annotations

import os
import secrets as _secrets
import time as _time
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    Response as _Response,
)
from fastapi.staticfiles import StaticFiles

from . import generator, store, telemetry
from .harness_runner import verify_fix
from .telemetry import new_learner_id, track_event

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Debugging Gym")

# Initialize persistent exercise storage.
store.init_db()

# ---------------------------------------------------------------------------
# Analytics: persistent anonymous learner identity
# ---------------------------------------------------------------------------


@app.middleware("http")
async def analytics_context(request: Request, call_next):
    """Assign a persistent opaque learner ID and track first visits."""
    learner_id = request.cookies.get("dg_learner_id")

    try:
        UUID(learner_id.removeprefix("learner_"))
        valid_learner_id = learner_id.startswith("learner_")
    except (ValueError, AttributeError):
        valid_learner_id = False

    first_visit = not valid_learner_id

    if first_visit:
        learner_id = new_learner_id()

    request.state.learner_id = learner_id

    response = await call_next(request)

    response.set_cookie(
        key="dg_learner_id",
        value=learner_id,
        httponly=True,
        samesite="lax",
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        max_age=60 * 60 * 24 * 365,
    )

    if request.url.path == "/" and request.method == "GET":
        await track_event(
            "app_opened",
            learner_id,
            {
                "first_visit": first_visit,
                "source": "web",
            },
        )

    return response


# ---------------------------------------------------------------------------
# Observability: request IDs and request timing
# ---------------------------------------------------------------------------


@app.middleware("http")
async def _request_signal(request: Request, call_next):
    """Record the per-request log point (SLI-01)."""
    request_id = request.headers.get("x-request-id") or _secrets.token_hex(8)
    start = _time.monotonic()

    response: _Response = await call_next(request)

    duration_ms = (_time.monotonic() - start) * 1000
    outcome = (
        "ok"
        if response.status_code < 400
        else "client_error"
        if response.status_code < 500
        else "server_error"
    )

    telemetry.emit_request_signal(
        request_id,
        request.url.path,
        outcome,
        duration_ms,
    )
    response.headers["x-request-id"] = request_id
    return response


# ---------------------------------------------------------------------------
# Teacher/student session handling
# ---------------------------------------------------------------------------

_SESSIONS: dict[str, str] = {}


def _role_for(request: Request) -> str:
    """The role attached to this request, or 'student' when anonymous."""
    token = request.headers.get("x-session")
    if token:
        role = _SESSIONS.get(token)
        if role:
            return role
    return "student"


def _teacher_only(request: Request) -> None:
    if _role_for(request) != "teacher":
        raise HTTPException(status_code=403, detail="teacher access required")


def _index_html() -> str:
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return _index_html()


@app.get("/api/kinds")
async def kinds() -> JSONResponse:
    """The catalogue of problem kinds a learner can choose from."""
    return JSONResponse(
        {
            kind: {"summary": meta["summary"]}
            for kind, meta in generator.KINDS.items()
        }
    )


# ---------------------------------------------------------------------------
# Exercise generation and storage
# ---------------------------------------------------------------------------


@app.post("/api/exercises")
async def create_exercise(request: Request) -> JSONResponse:
    """Generate and store a fresh exercise for a problem kind (teacher only)."""
    _teacher_only(request)

    body = await request.json()
    kind = body.get("kind")

    if kind not in generator.KINDS:
        raise HTTPException(status_code=400, detail=f"unknown kind: {kind}")

    exercise = await generator.create_exercise(kind)

    stored = store.save_exercise(
        kind=kind,
        task=exercise["task"],
        generator=exercise["generator"],
        source=exercise["source"],
        harness=exercise["harness"],
    )

    await track_event(
        "exercise_generated",
        request.state.learner_id,
        {
            "exercise_id": stored["id"],
            "kind": stored["kind"],
            "generator": stored["generator"],
            "source": "web",
        },
    )

    return JSONResponse(
        {
            "id": stored["id"],
            "kind": stored["kind"],
            "task": stored["task"],
            "generator": stored["generator"],
            "source": stored["source"],
            "harness": stored["harness"],
        }
    )


@app.get("/api/exercises/{exercise_id}/launch")
async def launch(request: Request, exercise_id: str) -> JSONResponse:
    """Return the launch configuration for connecting VS Code."""
    exercise = store.get_exercise(exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    await track_event(
        "exercise_started",
        request.state.learner_id,
        {
            "exercise_id": exercise_id,
            "kind": exercise["kind"],
            "source": "web",
        },
    )

    host = os.environ.get("DEBUG_HOST", "localhost")
    port = int(os.environ.get("DEBUG_PORT", "5678"))

    return JSONResponse(
        {
            "launch_json": {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Attach to Debugging Gym",
                        "type": "debugpy",
                        "request": "attach",
                        "connect": {"host": host, "port": port},
                        "pathMappings": [
                            {
                                "localRoot": "${workspaceFolder}",
                                "remoteRoot": "/app",
                            }
                        ],
                    }
                ],
            },
            "host": host,
            "port": port,
            "note": "Start the debug environment container, then attach from VS Code.",
        }
    )


# ---------------------------------------------------------------------------
# Exercise verification and completion tracking
# ---------------------------------------------------------------------------


@app.post("/api/exercises/{exercise_id}/verify")
async def verify(request: Request, exercise_id: str) -> JSONResponse:
    """Verify a learner's fix against the stored exercise harness."""
    exercise = store.get_exercise(exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    body = await request.json()
    source = body.get("source")

    if not source:
        raise HTTPException(status_code=400, detail="missing source")

    result = verify_fix(exercise_id, source, exercise["harness"])

    learner_id = request.state.learner_id
    learner = request.headers.get("x-learner") or learner_id

    await track_event(
        "verification_run",
        learner_id,
        {
            "exercise_id": exercise_id,
            "passed": result["passed"],
            "source": "web",
        },
    )

    telemetry.track(
        "verification_run",
        {
            "learner_id": learner,
            "exercise_id": exercise_id,
            "outcome": "pass" if result["passed"] else "fail",
        },
    )

    if result["passed"]:
        store.mark_completed(exercise_id, learner)
        result["completed"] = True

        await track_event(
            "exercise_completed",
            learner_id,
            {
                "exercise_id": exercise_id,
                "kind": exercise["kind"],
                "source": "web",
            },
        )

        telemetry.track(
            "exercise_completed",
            {
                "learner_id": learner,
                "exercise_id": exercise_id,
            },
        )

    return JSONResponse(result)


@app.post("/api/verify")
async def verify_submission(request: Request) -> JSONResponse:
    """Verify source against an explicitly supplied harness."""
    body = await request.json()
    source = body.get("source")
    harness = body.get("harness")

    if not source:
        raise HTTPException(status_code=400, detail="missing source")
    if not harness:
        raise HTTPException(status_code=400, detail="missing harness")

    result = verify_fix("local", source, harness)
    return JSONResponse(result)


# ---------------------------------------------------------------------------
# Teacher authentication and teacher-created exercises
# ---------------------------------------------------------------------------


@app.post("/api/auth/teacher")
async def teacher_login(request: Request) -> JSONResponse:
    """Return an opaque session token for a valid teacher access key."""
    body = await request.json()
    key = body.get("key", "")

    if not store.is_valid_teacher_key(key):
        raise HTTPException(status_code=403, detail="invalid teacher key")

    token = _secrets.token_hex(16)
    _SESSIONS[token] = "teacher"

    return JSONResponse({"session": token, "role": "teacher"})


@app.post("/api/exercises/teacher")
async def teacher_create_exercise(request: Request) -> JSONResponse:
    """Create an exercise from a teacher prompt and store its metadata."""
    _teacher_only(request)

    body = await request.json()
    prompt = body.get("prompt", "")
    name = body.get("name")
    description = body.get("description")

    if not prompt or not name:
        raise HTTPException(
            status_code=400,
            detail="prompt and name are required",
        )

    kind = next(
        (k for k in generator.KINDS if k in prompt.lower()),
        "off-by-one",
    )

    exercise = await generator.create_exercise(kind, prompt)

    stored = store.save_exercise(
        kind=kind,
        task=exercise["task"],
        generator="teacher:" + exercise["generator"],
        source=exercise["source"],
        harness=exercise["harness"],
        name=name,
        description=description,
    )

    return JSONResponse(
        {
            "id": stored["id"],
            "name": stored["name"],
            "description": stored["description"],
        }
    )


# ---------------------------------------------------------------------------
# Student exercise listing and retrieval
# ---------------------------------------------------------------------------


@app.get("/api/exercises")
async def list_available_exercises(request: Request) -> JSONResponse:
    """List exercises available to a learner, with completion markers."""
    learner = request.headers.get("x-learner") or request.state.learner_id
    completed = store.completed_ids(learner)

    telemetry.track(
        "app_opened",
        {
            "learner_id": learner,
            "first_visit": False,
        },
    )

    items = [
        {
            **store.to_public(ex),
            "completed": ex["id"] in completed,
        }
        for ex in store.list_exercises()
    ]

    return JSONResponse(items)


@app.get("/api/exercises/{exercise_id}")
async def get_exercise(request: Request, exercise_id: str) -> JSONResponse:
    """Return a stored exercise (program, harness, task) by id."""
    exercise = store.get_exercise(exercise_id)

    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    learner = request.headers.get("x-learner") or request.state.learner_id

    telemetry.track(
        "exercise_started",
        {
            "learner_id": learner,
            "exercise_id": exercise_id,
        },
    )

    await track_event(
        "exercise_started",
        request.state.learner_id,
        {
            "exercise_id": exercise_id,
            "kind": exercise["kind"],
            "source": "web",
        },
    )

    return JSONResponse(
        {
            "id": exercise["id"],
            "kind": exercise["kind"],
            "task": exercise["task"],
            "generator": exercise["generator"],
            "source": exercise["source"],
            "harness": exercise["harness"],
            "name": exercise.get("name"),
            "description": exercise.get("description"),
        }
    )


# ---------------------------------------------------------------------------
# VS Code extension download
# ---------------------------------------------------------------------------


@app.get("/api/extension/download")
async def download_extension():
    """Serve the packaged VS Code extension for download."""
    candidates = sorted(
        (BASE_DIR.parent / "vscode-extension").glob("*.vsix")
    )

    if candidates:
        return FileResponse(
            str(candidates[-1]),
            filename=candidates[-1].name,
        )

    placeholder = (
        "Debugging Gym VS Code extension package.\n"
        "Run `npm install && npm run compile && npx vsce package` "
        "in vscode-extension/ to build the .vsix served here.\n"
    )

    return JSONResponse({"note": placeholder.strip()})


# Static assets (CSS, JS).
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
    )

