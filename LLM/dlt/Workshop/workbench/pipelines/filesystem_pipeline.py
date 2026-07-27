"""dlt filesystem pipeline: load raw AI-agent session logs into DuckDB.

Sources: Claude Code (`~/.claude`), a Claude variant (`~/.zlaude`), Codex
(`~/.codex`), a Codex variant (`~/.zodex`), and the workshop sample logs under
`../agent_logs` (used when real agent dirs are empty on this machine).

Every source stores sessions as JSONL transcripts with heterogeneous per-line
records, so we keep each line verbatim in a `data` column and pull a few
lightweight fields up for convenience. All sources land in one unified table,
`log_records`, discriminated by an `agent` column. Model later with DuckDB's
JSON functions.

Offline note: this file is adapted from materials/code/filesystem_pipeline.py
so Lesson 02 can proceed without downloading the filesystem-pipeline toolkit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Optional

import dlt
from dlt.sources import TDataItems
from dlt.sources.filesystem import FileItemDict, filesystem

HOME = Path.home()
WORKSHOP_ROOT = Path(__file__).resolve().parents[2]  # .../LLM/dlt/Workshop
TABLE_NAME = "log_records"

# agent name -> (local_dir, file_glob). Claude-style layouts keep sessions
# under projects/; Codex-style layouts keep them under sessions/YYYY/MM/DD/.
# Workshop samples are flat JSONL under agent_logs/.
_SOURCE_SPECS: dict[str, tuple[Path, str]] = {
    "claude": (HOME / ".claude", "projects/**/*.jsonl"),
    "zlaude": (HOME / ".zlaude", "projects/**/*.jsonl"),
    "codex": (HOME / ".codex", "sessions/**/*.jsonl"),
    "zodex": (HOME / ".zodex", "sessions/**/*.jsonl"),
    "workshop_sample": (WORKSHOP_ROOT / "agent_logs", "**/*.jsonl"),
}


def _bucket_url(local_dir: Path) -> str:
    """file:// URI that works on Windows (file:///C:/...)."""
    return local_dir.resolve().as_uri()


def _available_sources() -> dict[str, tuple[str, str]]:
    """Only include source roots that exist and contain at least one match."""
    available: dict[str, tuple[str, str]] = {}
    for agent, (local_dir, file_glob) in _SOURCE_SPECS.items():
        if not local_dir.is_dir():
            continue
        matches = list(local_dir.glob(file_glob))
        if not matches:
            continue
        available[agent] = (_bucket_url(local_dir), file_glob)
    return available


def _session_id_from_name(file_name: str) -> str:
    """The session id lives in the filename for every source.

    Claude/zlaude: '<uuid>.jsonl'. Codex/zodex: 'rollout-<ts>-<uuid>.jsonl',
    where the uuid is the trailing five dash-joined groups.
    """
    stem = file_name[:-6] if file_name.endswith(".jsonl") else file_name
    if stem.startswith("rollout-"):
        parts = stem.split("-")
        if len(parts) >= 5:
            return "-".join(parts[-5:])
    return stem


def raw_reader(agent: str):
    """Build a transformer that turns each JSONL line into a raw record row."""

    @dlt.transformer(name=f"read_{agent}")
    def _read(items: Iterator[FileItemDict]) -> Iterator[TDataItems]:
        for file_obj in items:
            file_name = file_obj["file_name"]
            rel_path = file_obj.get("relative_path", file_name)
            session_id = _session_id_from_name(file_name)
            rows = []
            with file_obj.open() as f:  # binary; decode per line, tolerate bad utf-8
                for line_no, raw in enumerate(f):
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8", errors="replace")
                    line = raw.strip()
                    if not line:
                        continue
                    rec_type: Optional[str] = None
                    ts: Optional[str] = None
                    try:
                        rec = json.loads(line)
                        if isinstance(rec, dict):
                            rec_type = rec.get("type")
                            t = rec.get("timestamp")
                            ts = t if isinstance(t, str) else (str(t) if t is not None else None)
                    except json.JSONDecodeError:
                        pass
                    rows.append(
                        {
                            "agent": agent,
                            "session_id": session_id,
                            "source_file": rel_path,
                            "line_no": line_no,
                            "type": rec_type,
                            "timestamp": ts,
                            "data": line,
                        }
                    )
            if rows:
                yield rows

    return _read


def build_resources(sample: bool = False):
    sources = _available_sources()
    if not sources:
        raise FileNotFoundError(
            "No agent log sources found. Expected JSONL under ~/.claude/projects "
            f"or {WORKSHOP_ROOT / 'agent_logs'}."
        )
    resources = []
    for agent, (bucket_url, file_glob) in sources.items():
        files = filesystem(
            bucket_url=bucket_url,
            file_glob=file_glob,
            files_per_page=1 if sample else 100,
        )
        if sample:
            files = files.add_limit(1)  # one file per source for a quick verify
        resources.append(files | raw_reader(agent))
    return resources


def load(sample: bool = False) -> None:
    sources = _available_sources()
    print(f"sources={list(sources)}")
    # dataset_name must differ from the DuckDB catalog (agent_logs.duckdb stem),
    # otherwise DuckDB 1.5+ raises an ambiguous catalog/schema binder error.
    pipeline = dlt.pipeline(
        pipeline_name="agent_logs",
        destination="duckdb",
        dataset_name="logs",
        dev_mode=sample,  # throwaway dataset for sample runs; keep data for full load
    )
    info = pipeline.run(
        build_resources(sample=sample),
        table_name=TABLE_NAME,
        write_disposition="replace",
    )
    print(info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    import sys

    load(sample="--sample" in sys.argv)
