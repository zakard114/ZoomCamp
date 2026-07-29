#!/usr/bin/env python3
"""Sync llm-zoomcamp 04-evaluation/code and data into LLM/04/2026/Evaluation/."""

from __future__ import annotations

import urllib.request
from pathlib import Path

REPO = "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/04-evaluation"
ROOT = Path(__file__).resolve().parents[1] / "04" / "2026" / "Evaluation"

FILES = {
    "code": [
        "01-data-gen.ipynb",
        "02-search-eval.ipynb",
        "03-rag-evals.ipynb",
        "04-llm-judge.ipynb",
        "evaluation_utils.py",
        "ingest.py",
        "main.py",
        "pyproject.toml",
        "rag_helper.py",
        "uv.lock",
    ],
    "data": [
        "agent-answers.csv",
        "agent-evaluations.csv",
        "ground-truth-data.csv",
        "ground_truth-new.csv",
        "rag-answers-new.csv",
        "rag-answers.csv",
        "rag-evaluations-new.csv",
        "rag-evaluations.csv",
    ],
}


def download(subdir: str, name: str) -> Path:
    dest_dir = ROOT / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    url = f"{REPO}/{subdir}/{name}"
    out = dest_dir / name
    print(f"  {subdir}/{name} ...", end=" ", flush=True)
    urllib.request.urlretrieve(url, out)
    print(f"{out.stat().st_size // 1024} KiB")
    return out


def main() -> None:
    print(f"Target: {ROOT}\n")
    for subdir, names in FILES.items():
        print(f"[{subdir}]")
        for name in names:
            download(subdir, name)
    local = ROOT / "data" / "local"
    local.mkdir(parents=True, exist_ok=True)
    print(f"\nCreated: {local}")
    print("Done.")


if __name__ == "__main__":
    main()
