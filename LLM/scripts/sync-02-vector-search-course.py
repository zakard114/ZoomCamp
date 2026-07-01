#!/usr/bin/env python3
"""Sync llm-zoomcamp 02-vector-search into LLM/02/2026/materials/ (+ work copy in Vector_Search/)."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

REPO = "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/02-vector-search"
ROOT_2026 = Path(__file__).resolve().parents[1] / "02" / "2026"
MATERIALS = ROOT_2026 / "materials"
WORK_CODE = ROOT_2026 / "Vector_Search" / "code"
WORK_EMBED = ROOT_2026 / "Vector_Search" / "embed"

LESSONS = [
    "01-intro.md",
    "02-embeddings.md",
    "03-embeddings-dataset.md",
    "04-vector-search.md",
    "05-minsearch-vector.md",
    "06-rag-vector.md",
    "07-sqlitesearch-vector.md",
    "08-pgvector.md",
    "09-onnx-embedder.md",
    "10-next-steps.md",
]

CODE_FILES = [
    "vector_search.ipynb",
    "vector_search_persistent.ipynb",
    "vector_search_pgvector.ipynb",
]

EMBED_FILES = [
    "download.py",
    "embedder.py",
]


def download(rel_path: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"{REPO}/{rel_path}"
    print(f"  {rel_path} ...", end=" ", flush=True)
    urllib.request.urlretrieve(url, dest)
    print(f"{dest.stat().st_size // 1024} KiB")
    return dest


def copy_tree(src_dir: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for path in src_dir.iterdir():
        dest = dest_dir / path.name
        shutil.copy2(path, dest)
        print(f"  copied {path.name}")


def main() -> None:
    print(f"Materials: {MATERIALS}")
    print(f"Work code: {WORK_CODE}")
    print(f"Work embed: {WORK_EMBED}\n")

    download("README.md", MATERIALS / "README.md")

    print("[lessons]")
    for name in LESSONS:
        download(f"lessons/{name}", MATERIALS / "lessons" / name)

    print("[code -> materials/code]")
    for name in CODE_FILES:
        download(f"code/{name}", MATERIALS / "code" / name)

    print("[embed -> materials/embed]")
    for name in EMBED_FILES:
        download(f"embed/{name}", MATERIALS / "embed" / name)

    print("[code -> Vector_Search/code]")
    copy_tree(MATERIALS / "code", WORK_CODE)

    print("[embed -> Vector_Search/embed]")
    copy_tree(MATERIALS / "embed", WORK_EMBED)

    print("\nDone.")


if __name__ == "__main__":
    main()
