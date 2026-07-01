"""Paths to course CSVs and optional local outputs under Evaluation/data/.

This file is referenced by notebooks/scripts to make paths work regardless
of notebook working directory.
"""

from pathlib import Path

EVAL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = EVAL_ROOT / "data"
LOCAL_DIR = DATA_DIR / "local"

GROUND_TRUTH_CSV = DATA_DIR / "ground_truth-new.csv"
GROUND_TRUTH_LOCAL_CSV = LOCAL_DIR / "ground_truth.csv"

RAG_ANSWERS_CSV = DATA_DIR / "rag-answers-new.csv"
RAG_EVALUATIONS_CSV = DATA_DIR / "rag-evaluations-new.csv"

# Used by ingest.py for building the search/RAG index.
FAQ_CACHE = DATA_DIR / "faq_llm_zoomcamp.json"

