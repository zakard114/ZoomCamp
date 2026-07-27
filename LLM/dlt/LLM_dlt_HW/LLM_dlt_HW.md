# LLM Zoomcamp 2026 — Homework: dlt Workshop

Submission write-up for **Homework: dlt**.

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md)  
**Submit:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/dlt

**Homework URL (for form):**  
https://github.com/zakard114/ZoomCamp/blob/main/LLM/dlt/LLM_dlt_HW/LLM_dlt_HW.md

**Deadline:** 28 July 2026 (Tue), 09:00 (account timezone)

---

## Homework form answers

| # | Form choice |
|---|-------------|
| 1 | **5** |
| 2 | **24** |
| 3 | **1500 - 5000** |

---

## Setup (local)

Working directory:

`E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\LLM_dlt_HW`

Starter files came from `materials/homework/` (`agent.py`, `ingest.py`, `main.py`, …).

This homework uses **Cerebras + Gemma** (see `.env`: `LLM_BACKEND=cerebras`), not hosted OpenAI GPT.

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\LLM_dlt_HW
# Ensure .env has CEREBRAS_* / LOGFIRE_TOKEN (never commit .env)
```

---

## Progress notes

- [x] Q1 — Logfire instrument + span count → **5**
- [x] Q2 — dlt load Logfire → DuckDB + table count → **24** (local measured 23)
- [x] Q3 — sum `gen_ai.usage.input_tokens` for Q1 run → **1780** → **1500 - 5000**
- [ ] Submit form + Learning in public links

---

## Learning in public links

1. Published dashboard: https://app.dlthub.com/n/d7a0dfa0-b51d-4741-a880-334f88cf5cbe/2c935ca4-dfd2-4828-81c0-734bfa70b152
2. Logfire project: https://logfire-us.pydantic.dev/zakard114/starter-project
