"""Server-side exercise store for Debugging Gym.

The MUP slice generated exercises in memory, so a learner's progress depended
on local state. This module persists exercises and their completion records in
a local SQLite database, giving every generated or teacher-curated exercise a
stable id the product can re-fetch and verify against, independent of any local
files (US-013).

It also holds the teacher access key used to switch interfaces (US-014) and the
completion records that drive progress tracking (US-019).
"""

from __future__ import annotations

import os
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = os.environ.get("DEBUGGING_GYM_DB", str(Path(__file__).resolve().parent / "gym.db"))

# The teacher access key. In production this comes from the environment; the
# default is a placeholder that forces setting it. A non-empty value is always
# accepted, so a fresh checkout can demo the teacher interface.
TEACHER_KEY = os.environ.get("TEACHER_KEY", "")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the tables if they do not exist, and migrate old schemas."""
    conn = _connect()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                task TEXT NOT NULL,
                generator TEXT NOT NULL,
                source TEXT NOT NULL,
                harness TEXT NOT NULL,
                name TEXT,
                description TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS completions (
                exercise_id TEXT NOT NULL,
                learner TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                PRIMARY KEY (exercise_id, learner)
            );
            """
        )
        # Migrate a table created by an older schema that lacks the `kind`
        # column: add it (nullable initially) so existing rows survive.
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(exercises)")}
        if "kind" not in cols:
            conn.execute("ALTER TABLE exercises ADD COLUMN kind TEXT")
        conn.commit()
    finally:
        conn.close()


def save_exercise(
    *,
    kind: str,
    task: str,
    generator: str,
    source: str,
    harness: str,
    name: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Persist an exercise and return its stored row."""
    exercise_id = "ex-" + secrets.token_hex(3)
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO exercises (id, kind, task, generator, source, harness, name, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                exercise_id,
                kind,
                task,
                generator,
                source,
                harness,
                name,
                description,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
    finally:
        conn.close()
    row = get_exercise(exercise_id)
    assert row is not None
    return row


def get_exercise(exercise_id: str) -> dict[str, Any] | None:
    conn = _connect()
    try:
        row = conn.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
    finally:
        conn.close()
    return dict(row) if row else None


def list_exercises() -> list[dict[str, Any]]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT id, kind, task, generator, name, description, created_at
            FROM exercises
            ORDER BY created_at
            """
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def mark_completed(exercise_id: str, learner: str) -> None:
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO completions (exercise_id, learner, completed_at) VALUES (?, ?, ?)",
            (exercise_id, learner, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def completed_ids(learner: str) -> set[str]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT exercise_id FROM completions WHERE learner = ?", (learner,)
        ).fetchall()
    finally:
        conn.close()
    return {r["exercise_id"] for r in rows}


def is_valid_teacher_key(key: str) -> bool:
    """Whether a key unlocks the teacher interface."""
    if not key:
        return False
    return secrets.compare_digest(key, TEACHER_KEY)


def to_public(exercise: dict[str, Any]) -> dict[str, Any]:
    """The exercise view returned to a learner (no source/harness unless needed)."""
    return {
        "id": exercise["id"],
        "kind": exercise["kind"],
        "task": exercise["task"],
        "name": exercise.get("name"),
        "description": exercise.get("description"),
    }
