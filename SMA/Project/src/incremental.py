"""Incremental local cache for combined parquet transforms (rubric §6, on E: only)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from .config import PROJECT_ROOT
from .load_data import load_combined_parquet, resolve_data_path

CACHE_DIR = Path(
    __import__("os").environ.get(
        "SMA_INCREMENTAL_CACHE",
        r"E:\IT_SPACES\AI\.cache\sma-capstone\incremental",
    )
)


def _fingerprint(path: Path) -> str:
    stat = path.stat()
    raw = f"{path.resolve()}|{stat.st_size}|{int(stat.st_mtime)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def load_or_refresh_raw(path: Path | None = None) -> tuple[pd.DataFrame, dict]:
    """
    Read full parquet; if source fingerprint changed, drop stale processed snapshot metadata.
    Returns (dataframe, meta dict). Processed frame still built in pipeline — this step avoids
    re-downloading when fingerprint matches cached note (automation / incremental story).
    """
    resolved = resolve_data_path(path)
    fp = _fingerprint(resolved)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = CACHE_DIR / "source_meta.json"
    meta = {"path": str(resolved), "fingerprint": fp, "rows": None}
    if meta_path.is_file():
        try:
            prev = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prev = {}
        if prev.get("fingerprint") == fp and prev.get("path") == str(resolved):
            meta.update(prev)
            meta["cache_hit"] = True
        else:
            meta["cache_hit"] = False
    else:
        meta["cache_hit"] = False
    frame = load_combined_parquet(resolved)
    meta["rows"] = int(len(frame))
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    snapshot = CACHE_DIR / f"rows_{fp}.json"
    snapshot.write_text(json.dumps({"rows": meta["rows"], "project": str(PROJECT_ROOT)}), encoding="utf-8")
    return frame, meta