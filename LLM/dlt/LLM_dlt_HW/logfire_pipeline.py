"""Load Pydantic Logfire records into DuckDB via dlt (Homework Q2)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator

import dlt
import requests
from dotenv import load_dotenv

load_dotenv()

# US region project (starter-project on logfire-us)
LOGFIRE_BASE_URL = os.getenv("LOGFIRE_BASE_URL", "https://logfire-us.pydantic.dev")


def _parse_nested(value: Any) -> Any:
    """Parse JSON-serialized nested fields so dlt can normalize child tables."""
    if isinstance(value, str):
        s = value.strip()
        if (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]")):
            try:
                return _parse_nested(json.loads(s))
            except json.JSONDecodeError:
                return value
    if isinstance(value, dict):
        return {k: _parse_nested(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_parse_nested(v) for v in value]
    return value


@dlt.resource(name="records", write_disposition="replace")
def logfire_records(
    lookback_days: int = 7,
    limit: int = 1000,
) -> Iterator[dict[str, Any]]:
    """Pull Logfire `records` (spans/logs) via Query API v2."""
    token = os.environ.get("LOGFIRE_READ_TOKEN", "").strip().strip("'\"")
    if not token:
        raise RuntimeError("LOGFIRE_READ_TOKEN is missing in .env")

    min_timestamp = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).isoformat()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    body = {
        "sql": f"SELECT * FROM records ORDER BY start_timestamp DESC LIMIT {limit}",
        "min_timestamp": min_timestamp,
        "limit": limit,
    }

    response = requests.post(
        f"{LOGFIRE_BASE_URL}/v2/query",
        headers=headers,
        json=body,
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()

    rows = payload.get("data") or payload.get("rows") or []
    print(f"Fetched {len(rows)} Logfire records")

    for row in rows:
        yield _parse_nested(row)


def load_agent_traces() -> None:
    # Keep pipeline state/data on E: (never under C:\Users\...)
    pipelines_dir = os.getenv(
        "DLT_PIPELINES_DIR",
        r"E:\IT_SPACES\AI\.cache\dlt\pipelines",
    )
    os.makedirs(pipelines_dir, exist_ok=True)

    # pipeline_name != dataset_name — DuckDB binder confuses identical names
    pipeline = dlt.pipeline(
        pipeline_name="logfire_agent_traces",
        destination="duckdb",
        dataset_name="agent_traces",
        pipelines_dir=pipelines_dir,
    )
    load_info = pipeline.run(logfire_records())
    print(load_info)

    # Homework Q2 check
    import duckdb

    # dlt default DuckDB file: <pipeline_name>.duckdb in cwd
    con = duckdb.connect("logfire_agent_traces.duckdb", read_only=True)
    try:
        n = con.execute(
            """
            SELECT COUNT(*) AS n
            FROM information_schema.tables
            WHERE table_schema = 'agent_traces'
            """
        ).fetchone()[0]
        print("tables_in_agent_traces=", n)
        tables = con.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'agent_traces'
            ORDER BY table_name
            """
        ).fetchall()
        print("table_list=", [t[0] for t in tables])
    finally:
        con.close()


if __name__ == "__main__":
    load_agent_traces()
