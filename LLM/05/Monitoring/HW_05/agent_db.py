# agent_db.py
"""Postgres helpers for agent tool-call monitoring (HW_05)."""

import os
from datetime import datetime, timezone

import psycopg


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "course_assistant"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        connect_timeout=int(os.getenv("POSTGRES_CONNECT_TIMEOUT", "5")),
    )


def save_tool_call(
    session_id: str,
    tool_name: str,
    tool_input: str | None,
    tool_output: str | None,
    duration_ms: float,
    timestamp: datetime | None = None,
) -> int:
    """Insert one tool-call row and return the new id."""
    ts = timestamp or datetime.now(timezone.utc)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO agent_tool_calls (
                    session_id, tool_name, tool_input, tool_output,
                    duration_ms, timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (session_id, tool_name, tool_input, tool_output, duration_ms, ts),
            )
            row_id = cur.fetchone()[0]
        conn.commit()
        return row_id
    finally:
        conn.close()


def get_tool_call_count(session_id: str | None = None) -> int:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if session_id:
                cur.execute(
                    "SELECT COUNT(*) FROM agent_tool_calls WHERE session_id = %s",
                    (session_id,),
                )
            else:
                cur.execute("SELECT COUNT(*) FROM agent_tool_calls")
            return cur.fetchone()[0]
    finally:
        conn.close()
