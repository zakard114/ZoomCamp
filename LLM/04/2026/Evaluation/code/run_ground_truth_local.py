#!/usr/bin/env python3
"""Generate ground truth CSV with local Ollama (default) or llama-server.

Usage (Ollama):
  ollama pull qwen2.5:0.5b
  ollama serve
  python run_ground_truth_local.py
  python run_ground_truth_local.py --limit 5
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

import pandas as pd
from openai import OpenAI
from tqdm.auto import tqdm

from evaluation_paths import GROUND_TRUTH_LOCAL_CSV
from ingest import load_faq_data

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")

DATA_GEN_INSTRUCTIONS = """
You emulate a student who's taking our course.
Formulate 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record.

The output should resemble how people ask questions on the internet. Not too formal, not too short, not too long.

Format: number each question like 1. ... 2. ... (exactly 5).
""".strip()


def extract_questions_from_text(text: str) -> list[str]:
    questions = re.findall(r"\d+\.\s*(.*)", text)
    if not questions:
        questions = [line.strip() for line in text.split("\n") if line.strip()]
    return questions[:5]


def generate_ground_truth(doc, client: OpenAI, model: str):
    user_prompt = json.dumps(doc)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "developer", "content": DATA_GEN_INSTRUCTIONS},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    content = response.choices[0].message.content
    questions_list = extract_questions_from_text(content or "")
    records = [{"question": q, "document": doc["id"]} for q in questions_list]
    return records, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="0 = all llm-zoomcamp docs")
    parser.add_argument("--out", type=Path, default=GROUND_TRUTH_LOCAL_CSV)
    args = parser.parse_args()

    documents = load_faq_data()
    if args.limit > 0:
        documents = documents[: args.limit]

    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
    print(f"docs={len(documents)} model={OLLAMA_MODEL}")

    ground_truth = []
    for doc in tqdm(documents, desc="ground truth"):
        records, _ = generate_ground_truth(doc, client, OLLAMA_MODEL)
        ground_truth.extend(records)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(ground_truth)
    df.to_csv(args.out, index=False)
    print("saved:", args.out.resolve(), "rows:", len(df))


if __name__ == "__main__":
    main()
