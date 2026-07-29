#!/usr/bin/env python3
"""Download Gemma 4 E2B target + MTP assistant GGUF for local llama.cpp inference."""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models" / "gemma-4-e2b"

DOWNLOADS = [
    {
        "repo_id": "unsloth/gemma-4-E2B-it-GGUF",
        "filename": "gemma-4-E2B-it-Q4_K_M.gguf",
        "label": "target (E2B Q4_K_M)",
    },
    {
        "repo_id": "AtomicChat/gemma-4-E2B-it-assistant-GGUF",
        "filename": "gemma-4-E2B-it-assistant.Q4_K_M.gguf",
        "label": "assistant MTP head (Q4_K_M)",
    },
]


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Saving models under: {MODEL_DIR}")

    for item in DOWNLOADS:
        print(f"\n=== {item['label']} ===")
        print(f"repo: {item['repo_id']}")
        print(f"file: {item['filename']}")
        path = hf_hub_download(
            repo_id=item["repo_id"],
            filename=item["filename"],
            local_dir=str(MODEL_DIR),
        )
        size_mb = Path(path).stat().st_size / (1024 * 1024)
        print(f"done: {path} ({size_mb:.1f} MiB)")

    print("\n=== all downloads complete ===")
    for p in sorted(MODEL_DIR.glob("*.gguf")):
        size_mb = p.stat().st_size / (1024 * 1024)
        print(f"  {p.name}  ({size_mb:.1f} MiB)")


if __name__ == "__main__":
    main()
