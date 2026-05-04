# LLM Zoomcamp — Module 1 homework (Introduction)

This folder is **homework only**: Docker stack for ES **8.17.6**, links, and **`homework_module1.ipynb`**.

**Lecture / course practice:** open **`../module-1-practice.ipynb`** in the parent `Introduction` folder (minsearch, RAG walkthrough, etc.).

## Elasticsearch (homework, 8.17.6)

- `docker-compose.yml` runs **Elasticsearch 8.17.6** (Q1 `build_hash` matches the 2025 assignment).
- Data directory (bind mount): **`ZoomCamp/docker-data/volumes/elasticsearch-hw-data`** (relative to repo root; keep on the same drive as the clone if possible).
- Do **not** run together with `LLM/docker-compose.elasticsearch.yml` (course, 8.4.3) — both need port **9200**.

```text
cd <your-clone>/ZoomCamp/LLM/01/Introduction/llm_01_hw
docker compose up -d
```

Check: `curl http://127.0.0.1:9200`

## Notebook

| File | Purpose |
|------|---------|
| **`homework_module1.ipynb`** | Homework 1 — work here. |
| **`../module-1-practice.ipynb`** | Lecture follow-along (not in this folder). |

## Links

| Item | URL |
|------|-----|
| Homework submission (2025) | https://courses.datatalks.club/llm-zoomcamp-2025/homework/hw1 |
| Cohort / intro materials | https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2025/01-intro |
| Reference solution (after solving, or when stuck) | https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/01-intro/homework_solution.ipynb |
| FAQ JSON (raw, 2025 cohort) | https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/cohorts/2025/01-intro/documents.json |

## Learning in public (optional)

If the form asks for a repo link, point to this folder path in your GitHub repo.
