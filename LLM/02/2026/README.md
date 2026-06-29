# Module 02 — 2026 Vector Search

Main workspace for the **2026 cohort**.

## Contents

| Path | Source | Notes |
|------|--------|-------|
| [`materials/`](materials/) | [02-vector-search](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/02-vector-search) | Upstream snapshot: `lessons/`, `code/`, `embed/`, `README.md` |
| [`Vector_Search/code/`](Vector_Search/code/) | same `code/` | **Run lesson notebooks here** |
| [`Vector_Search/embed/`](Vector_Search/embed/) | same `embed/` | ONNX `download.py`, `embedder.py` (homework + lesson 9) |
| [`Vector_Search/HW_02/`](Vector_Search/HW_02/) | homework | Your 2026 homework (uv + gitsource + minsearch) |

Re-sync course files (from `LLM/`):

```bash
python scripts/sync-02-vector-search-course.py
```

Download ONNX model (from `Vector_Search/embed/` or homework project):

```bash
cd Vector_Search/embed
uv run python download.py
```

## Homework

Official homework: [cohorts/2026/02-vector-search/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/02-vector-search/homework.md)  
Submit: [Vector_Search/HW_02/LLM_02_HW.md](Vector_Search/HW_02/LLM_02_HW.md) (notebook: [`vector_search_homework.ipynb`](Vector_Search/HW_02/vector_search_homework.ipynb))

## 2025 reference

Qdrant + FastEmbed archive: [`../2025/`](../2025/)
