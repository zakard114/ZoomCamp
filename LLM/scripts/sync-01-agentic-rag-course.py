#!/usr/bin/env python3
"""Sync llm-zoomcamp 01-agentic-rag into LLM/01/2026/materials/ (+ work copy in Agentic_RAG/code/)."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

REPO = "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/01-agentic-rag"
ROOT_2026 = Path(__file__).resolve().parents[1] / "01" / "2026"
MATERIALS = ROOT_2026 / "materials"
WORK_CODE = ROOT_2026 / "Agentic_RAG" / "code"

LESSONS = [
    "01-intro.md",
    "02-environment.md",
    "03-rag.md",
    "04-dataset.md",
    "05-search.md",
    "06-building-prompt.md",
    "07-llm.md",
    "08-rag-helper.md",
    "09-data-ingestion.md",
    "10-rag-next-steps.md",
    "11-agents-intro.md",
    "12-rag-revision.md",
    "13-function-calling.md",
    "14-agentic-loop.md",
    "15-frameworks.md",
    "16-other-frameworks.md",
]

CODE_FILES = [
    ".gitignore",
    "agents.ipynb",
    "ingest.py",
    "notebook.ipynb",
    "persinsent_rag.ipynb",
    "persistent_rag_ingest.ipynb",
    "pyproject.toml",
    "rag_cleaned.ipynb",
    "rag_helper.py",
]


def download(rel_path: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"{REPO}/{rel_path}"
    print(f"  {rel_path} ...", end=" ", flush=True)
    urllib.request.urlretrieve(url, dest)
    print(f"{dest.stat().st_size // 1024} KiB")
    return dest


def main() -> None:
    print(f"Materials: {MATERIALS}")
    print(f"Work code: {WORK_CODE}\n")

    download("README.md", MATERIALS / "README.md")

    print("[lessons]")
    for name in LESSONS:
        download(f"lessons/{name}", MATERIALS / "lessons" / name)

    print("[code -> materials/code]")
    for name in CODE_FILES:
        download(f"code/{name}", MATERIALS / "code" / name)

    print("[code -> Agentic_RAG/code]")
    WORK_CODE.mkdir(parents=True, exist_ok=True)
    src_code = MATERIALS / "code"
    for path in src_code.iterdir():
        dest = WORK_CODE / path.name
        shutil.copy2(path, dest)
        print(f"  copied {path.name}")

    print("\nDone.")


if __name__ == "__main__":
    main()
