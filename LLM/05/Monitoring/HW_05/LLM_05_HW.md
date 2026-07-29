# LLM Zoomcamp 2026 — Homework 5: Monitoring (OpenTelemetry)

**Submit form:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw5  
**Work dir:** `E:/IT_SPACES/AI/ZoomCamp/LLM/05/Monitoring/HW_05`  
**Backend (submission):** Cerebras `gemma-4-31b` (Ollama `qwen2.5:0.5b` also tested for comparison)

---

## Form answers

| Q | Answer | Evidence |
|---|--------|----------|
| 1 | **3** | Console: 3 ReadableSpan blocks (`search`, `llm`, `rag`) |
| 2 | **7000** | `input_tokens=7947` |
| 3 | **Over 2000ms** | `llm` span ~5204 ms |
| 4 | **rag, search, and llm** | `traces.db` spans table |
| 5 | **llm** | llm 9156 ms vs search 22 ms (excl. rag) |
| 6 | **They're identical** | 4 runs: `[7947, 7947, 7947, 7947]` |

---

## Setup

```bash
cd /e/IT_SPACES/AI/ZoomCamp/LLM/05/Monitoring/HW_05
uv add opentelemetry-api opentelemetry-sdk
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from starter import rag; print('ok')"
```

Query used for Q1–Q6:

```text
How does the agentic loop keep calling the model until it stops?
```

OTel span tree:

```text
rag
├─ search
└─ llm
```

---

## Q1 — First trace

**Script:** `q1_trace.py`

```bash
uv run python q1_trace.py
```

Wrapped `RAGBase` → `RAGTraced`; each of `rag()`, `search()`, `llm()` gets its own span via `tracer.start_as_current_span(...)`.

**Observed (Ollama run):**

- 3 JSON blocks printed: `search` → `llm` → `rag`
- Same `trace_id` on all three
- `search`/`llm` `parent_id` = `rag` `span_id`
- `search` ~3 ms, `llm` ~162 s (Ollama), total ~162 s

**Answer: 3** — backend does not change span count.

---

## Q2 — Span attributes (tokens)

**Scripts:** `q2_attribute.py`, `run_q1_q3_cerebras.py`

```python
span.set_attribute("input_tokens", input_tokens)
span.set_attribute("output_tokens", output_tokens)
```

| backend | input_tokens | form choice |
|---------|--------------|-------------|
| Cerebras gemma-4-31b | **7947** | **7000** |
| Ollama qwen2.5:0.5b | 2050 | 700 |

**Answer: 7000**

---

## Q3 — Span timing

Question is about the **llm** span duration, not total RAG time.

| backend | llm duration | form choice |
|---------|--------------|-------------|
| Cerebras gemma-4-31b | **5204 ms** | **Over 2000ms** |
| Ollama qwen2.5:0.5b | ~2–5 min | Over 2000ms |

**Answer: Over 2000ms**

---

## Q4 — SQLite export

**Script:** `q4_sqlite.py` → `traces.db`

Swapped `ConsoleSpanExporter` for custom `SQLiteSpanExporter`. RAG instrumentation unchanged — only the export destination changed.

```bash
uv run python q4_sqlite.py
sqlite3 traces.db "SELECT name, COUNT(*) FROM spans GROUP BY name;"
```

**Output:**

```text
llm|1
rag|1
search|1
```

No `judge` span in this pipeline.

**Answer: rag, search, and llm**

---

## Q5 — Query trace data

**Script:** `q5_duration.py`

```bash
uv run python q5_duration.py
```

Exclude parent `rag`; sum child durations:

```sql
SELECT name,
       ROUND(SUM(end_time - start_time) / 1e6, 2) AS total_ms
FROM spans
WHERE name != 'rag'
GROUP BY name
ORDER BY total_ms DESC;
```

**Output (2 runs in DB):**

```text
('llm', 2, 9156.41)
('search', 2, 21.99)
```

LLM = ~99.8% of child time. Search is negligible.

**Answer: llm**

---

## Q6 — Token stability

**Script:** `q6_token_stability.py`

```bash
uv run python q6_token_stability.py
```

4 RAG runs total; load with pandas:

```python
df = pd.read_sql_query(
    "SELECT input_tokens FROM spans WHERE name = 'llm'", conn
)
```

**Output:**

```text
[7947, 7947, 7947, 7947]
min=7947, max=7947, relative_spread_pct=0.00
```

Same query + fixed minsearch index → same retrieved context → same prompt size every run. SQLite only stores the logs; it does not affect search results.

**Answer: They're identical**

---

## Scripts

| File | Purpose |
|------|---------|
| `q1_trace.py` | Q1 console spans |
| `q2_attribute.py` | Q2 token attributes |
| `run_q1_q3_cerebras.py` | Q1–Q3 Cerebras rerun |
| `q4_sqlite.py` | Q4 SQLite export |
| `q5_duration.py` | Q5 duration query |
| `q6_token_stability.py` | Q6 token stability |
