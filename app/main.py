"""Debugging Gym — MUP slice web application.

FastAPI backend serving a minimal web front end. A learner chooses a problem
kind, gets a generated exercise, connects their own VS Code to a debug
environment, and verifies the fix against the harness.

The debug environment uses the same debugpy approach proven in Week 2's
prototype: a container runs the exercise and exposes a Debug Adapter Protocol
server that the learner's own VS Code attaches to.
"""

from __future__ import annotations

import os
import secrets as _secrets
import time as _time
from pathlib import Path

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

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Debugging Gym")

store.init_db()


@app.middleware("http")
async def _request_signal(request: Request, call_next):
    """Record the per-request log point (SLI-01) for every HTTP request.

    Assigns a request_id, times the request, and emits the structured log line
    and histogram point with the route and outcome labels the diagnosability
    test reads.
    """
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
    telemetry.emit_request_signal(request_id, request.url.path, outcome, duration_ms)
    response.headers["x-request-id"] = request_id
    return response


# A tiny in-process session: role held by an opaque token. In production this
# would be a real session store; the MUP slice keeps it simple (US-014, US-018).
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
        {kind: {"summary": meta["summary"]} for kind, meta in generator.KINDS.items()}
    )


@app.post("/api/exercises")
async def create_exercise(request: Request) -> JSONResponse:
    """Generate and store a fresh exercise for a problem kind (teacher only).

    A student cannot generate; only a teacher may create a new exercise
    (DEC-010, DEC-023, US-016). The exercise is persisted so it can be
    re-fetched and verified by id (US-013).
    """
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
    telemetry.track(
        "exercise_generated",
        {
            "exercise_id": stored["id"],
            "kind": stored["kind"],
            "generator": stored["generator"],
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
async def launch(exercise_id: str) -> JSONResponse:
    """Return the launch configuration for connecting VS Code."""
    exercise = store.get_exercise(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")
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


@app.post("/api/exercises/{exercise_id}/verify")
async def verify(request: Request, exercise_id: str) -> JSONResponse:
    """Verify a learner's fix against the stored exercise harness.

    The exercise is read from the server store, not from the learner's local
    state, so a reopened exercise verifies against its stored harness (US-013).
    A passing run records a completion for the learner (US-019).
    """
    exercise = store.get_exercise(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")
    body = await request.json()
    source = body.get("source")
    if not source:
        raise HTTPException(status_code=400, detail="missing source")
    result = verify_fix(exercise_id, source, exercise["harness"])
    learner = request.headers.get("x-learner") or "anonymous"
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
        telemetry.track(
            "exercise_completed",
            {"learner_id": learner, "exercise_id": exercise_id},
        )
    return JSONResponse(result)


@app.post("/api/verify")
async def verify_submission(request: Request) -> JSONResponse:
    """Verify a learner's source against an explicit harness.

    Used when a learner reopens a previously saved exercise whose id is no
    longer in the server's memory: the harness is sent with the source, and the
    product still runs it in an isolated subprocess so a learner cannot tamper
    with the verdict (DEC-016 direction).
    """
    body = await request.json()
    source = body.get("source")
    harness = body.get("harness")
    if not source:
        raise HTTPException(status_code=400, detail="missing source")
    if not harness:
        raise HTTPException(status_code=400, detail="missing harness")
    result = verify_fix("local", source, harness)
    return JSONResponse(result)


# ---- Teacher / student interfaces (US-014..US-016) --------------------------


@app.post("/api/auth/teacher")
async def teacher_login(request: Request) -> JSONResponse:
    """Swap to the teacher interface for a valid teacher access key.

    Returns an opaque session token the client sends back as ``x-session``.
    """
    body = await request.json()
    key = body.get("key", "")
    if not store.is_valid_teacher_key(key):
        raise HTTPException(status_code=403, detail="invalid teacher key")
    import secrets

    token = secrets.token_hex(16)
    _SESSIONS[token] = "teacher"
    return JSONResponse({"session": token, "role": "teacher"})


@app.post("/api/exercises/teacher")
async def teacher_create_exercise(request: Request) -> JSONResponse:
    """Teacher generates an exercise from a prompt and stores it with a name/description.

    The prompt is passed to the generator as the kind name it resolves to; in a
    fuller implementation the prompt drives LLM generation directly. For now it
    generates from the catalogue and attaches the teacher's name and description.
    """
    _teacher_only(request)
    body = await request.json()
    prompt = body.get("prompt", "")
    name = body.get("name")
    description = body.get("description")
    if not prompt or not name:
        raise HTTPException(status_code=400, detail="prompt and name are required")

    # Resolve the prompt to a kind from the catalogue (the LLM path would use
    # the prompt directly; this keeps the slice deterministic).
    kind = next((k for k in generator.KINDS if k in prompt.lower()), "off-by-one")
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


@app.get("/api/exercises")
async def list_available_exercises(request: Request) -> JSONResponse:
    """List exercises available to a learner, with completion markers."""
    learner = request.headers.get("x-learner") or "anonymous"
    completed = store.completed_ids(learner)
    telemetry.track("app_opened", {"learner_id": learner, "first_visit": False})
    items = [
        {**store.to_public(ex), "completed": ex["id"] in completed} for ex in store.list_exercises()
    ]
    return JSONResponse(items)


@app.get("/api/exercises/{exercise_id}")
async def get_exercise(request: Request, exercise_id: str) -> JSONResponse:
    """Return a stored exercise (program, harness, task) by id (US-013)."""
    exercise = store.get_exercise(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")
    learner = request.headers.get("x-learner") or "anonymous"
    telemetry.track(
        "exercise_started",
        {"learner_id": learner, "exercise_id": exercise_id},
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


@app.get("/api/extension/download")
async def download_extension() -> FileResponse:
    """Serve the packaged VS Code extension for download (US-017).

    The file is expected at ``vscode-extension/*.vsix``; a placeholder package
    is served when none is built so the page still works.
    """
    candidates = sorted((BASE_DIR.parent / "vscode-extension").glob("*.vsix"))
    if candidates:
        return FileResponse(str(candidates[-1]), filename=candidates[-1].name)
    # Fallback: a small text placeholder explaining where the package is built.
    placeholder = (
        "Debugging Gym VS Code extension package.\n"
        "Run `npm install && npm run compile && npx vsce package` in vscode-extension/ "
        "to build the .vsix served here.\n"
    )
    return JSONResponse({"note": placeholder.strip()})


# Static assets (CSS, JS).
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
