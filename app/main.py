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
from pathlib import Path

from uuid import UUID
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import generator
from .harness_runner import verify_fix
from .telemetry import new_learner_id, track_event

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Debugging Gym")

@app.middleware("http")
async def analytics_context(request: Request, call_next):
    """Assign a persistent opaque learner ID and track first visits."""
    learner_id = request.cookies.get("dg_learner_id")
    # first_visit = not (
    #     learner_id
    #     and learner_id.startswith("learner_")
    #     and len(learner_id) == 40
    # )

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
    """Generate and return a fresh exercise for a problem kind."""
    body = await request.json()
    kind = body.get("kind")
    if kind not in generator.KINDS:
        raise HTTPException(status_code=400, detail=f"unknown kind: {kind}")
    exercise = await generator.create_exercise(kind)

    learner_id = request.state.learner_id

    await track_event(
        "exercise_generated",
        learner_id,
        {
            "exercise_id": exercise["id"],
            "kind": exercise["kind"],
            "generator": exercise["generator"],
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
        }
    )


@app.get("/api/exercises/{exercise_id}/launch")
async def launch(request: Request, exercise_id: str) -> JSONResponse:
    """Return the launch configuration for connecting VS Code.

    In the slice, the debug environment runs in a local container; this endpoint
    returns the debugpy attach configuration a learner pastes into launch.json.
    """
    exercise = generator.EXERCISES.get(exercise_id)
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


@app.post("/api/exercises/{exercise_id}/verify")
async def verify(request: Request, exercise_id: str) -> JSONResponse:
    """Verify a learner's fix against the exercise harness."""
    exercise = generator.EXERCISES.get(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="exercise not found")

    body = await request.json()
    source = body.get("source")
    if not source:
        raise HTTPException(status_code=400, detail="missing source")

    result = verify_fix(exercise_id, source, exercise["harness"])

    learner_id = request.state.learner_id
    properties = {
        "exercise_id": exercise_id,
        "passed": result["passed"],
        "source": "web",
    }

    await track_event(
        "verification_run",
        learner_id,
        properties,
    )

    if result["passed"]:
        await track_event(
            "exercise_completed",
            learner_id,
            {
                "exercise_id": exercise_id,
                "kind": exercise["kind"],
                "source": "web",
            },
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


# Static assets (CSS, JS).
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
