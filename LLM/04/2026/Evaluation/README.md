# Module 04 — 2026 Evaluation

Main workspace for the **2026 cohort** (upstream: `llm-zoomcamp/04-evaluation`).

## Layout

| Path | Source | Notes |
|------|--------|-------|
| [`code/`](code/) | Course repo | Notebooks `01`–`04`, `evaluation_utils.py`, `ingest.py`, `rag_helper.py`, `pyproject.toml` |
| [`data/`](data/) | Course repo | **Only** these CSVs (no local copies) |
| | | `ground_truth-new.csv` → 01, 02, 03 |
| | | `rag-answers-new.csv` → 04 (or output of 03) |
| | | `rag-evaluations-new.csv` → output of 04 |
| [`data/faq_llm_zoomcamp.json`](data/faq_llm_zoomcamp.json) | One-time snapshot | FAQ for search/RAG in 02/03 (not in eval CSVs) |

Run notebooks from **`code/`**. Paths: `evaluation_paths.py`.

**Offline FAQ (once):** `python snapshot_faq_cache.py`

## Shared environment

| Resource | Path |
|----------|------|
| OpenAI key | `LLM/.env` |
| Python venv | `LLM/.venv` |
| Qdrant / cache | `LLM/04/` (compose, `cache/`, `.env.example`) |
| Local LLM (optional) | `LLM/models/`, `LLM/scripts/` |

## Sync course files

When upstream updates:

```powershell
E:\IT_SPACES\AI\venv\Scripts\python.exe E:\IT_SPACES\AI\ZoomCamp\LLM\scripts\sync-04-evaluation-course.py
```

## 2025 archive

[`../../2025/Evaluation/`](../../2025/Evaluation/) — prior ground-truth / offline eval work.
