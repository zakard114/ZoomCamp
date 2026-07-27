# LLM Zoomcamp 2026 — Homework: dlt Workshop

Submission write-up for **Homework: dlt** (Logfire observability → dlt → DuckDB).

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)  
**Instructions:** [homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md)  
**Submit:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/dlt  

**Homework URL (for form):**  
https://github.com/zakard114/ZoomCamp/blob/main/LLM/dlt/LLM_dlt_HW/LLM_dlt_HW.md  

**Work dir:** `E:/IT_SPACES/AI/ZoomCamp/LLM/dlt/LLM_dlt_HW`  
**Backend (submission):** Cerebras `gemma-4-31b` (OpenAI-compatible; not hosted OpenAI GPT)  
**Logfire project:** https://logfire-us.pydantic.dev/zakard114/starter-project  

---

## Form answers

| Q | Answer | Evidence |
|---|--------|----------|
| 1 | **5** | Logfire span tree for `How do I run Ollama locally?` (agent + LLM + tool + LLM + one more node) |
| 2 | **24** | `information_schema.tables` on `agent_traces`; local measure **23**, form options → **24** |
| 3 | **1500 - 5000** | Sum of `gen_ai.usage.input_tokens` on LLM chats = **1780** (241 + 1539) |

---

## What this homework is about

Module 1 FAQ agent, rewritten with **Pydantic AI**, instrumented with **Pydantic Logfire**, then traces pulled back with **dlt** into DuckDB for analysis.

Logfire = realtime observability for LLM/agent runs (tool calls, messages, token usage).  
dlt = normalize nested JSON spans into typed parent/child tables.

Query used for Q1 / Q3:

```text
How do I run Ollama locally?
```

---

## Setup (local adaptations)

Official homework suggests `uv init` / `uv add` / `uv run`. On this Windows machine **`uv` often hangs**, so the working path was:

1. Homework folder: `LLM/dlt/LLM_dlt_HW`
2. `.env` with write/read tokens (**never committed**)
3. LLM via **Cerebras + Gemma** copied from shared `ZoomCamp/LLM/.env` (`LLM_BACKEND=cerebras`)
4. Skip `logfire auth` / `uv run logfire …` — use **Write Token in `.env`** instead
5. Run with venv Python directly (not `uv run`)

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\LLM_dlt_HW
# .env (gitignored): LOGFIRE_TOKEN, LOGFIRE_READ_TOKEN, CEREBRAS_*
.\.venv\Scripts\python.exe main.py
```

Instrumentation in `main.py` (homework Q1):

```python
from dotenv import load_dotenv
load_dotenv()

import logfire
logfire.configure()
logfire.instrument_pydantic_ai()
```

Agent model (`agent.py`) uses Cerebras OpenAI-compatible endpoint instead of `openai:gpt-…`.

**Learning note:** putting keys only in the editor without **Ctrl+S** left `.env` empty on disk — Cursor correctly flagged EMPTY until save.

---

## Q1 — Instrument with Logfire and count spans

### Official vs what we ran

| Official hint | What we did |
|---------------|-------------|
| `uv run python agent.py` | **`.\.venv\Scripts\python.exe main.py`** (`main.py` is the entrypoint; `uv` skipped) |
| Browser `logfire auth` | **Write token → `.env` as `LOGFIRE_TOKEN`** |
| Default OpenAI model | **Cerebras `gemma-4-31b`** |

### Console timeline (2026-07-27 21:30)

```text
Logfire project URL: https://logfire-us.pydantic.dev/zakard114/starter-project

21:30:10.441 faq_agent run
21:30:10.447   chat gemma-4-31b
21:30:13.205   running tool: search
21:30:13.405   chat gemma-4-31b
```

Logical steps visible in the console:

1. `faq_agent run` — agent
2. `chat gemma-4-31b` — LLM #1
3. `running tool: search` — tool
4. `chat gemma-4-31b` — LLM #2

### How we counted spans in Logfire (learning trap)

Live view showed **`1.78K` / `375`** next to the run. Those are **token metrics**, not span counts.

Correct place to count:

1. Open Live → click **`21:30:10 faq_agent run`**
2. Expand the **span tree** (or Raw Data span list)
3. Count nodes: agent / LLM / tool / LLM / (+ nested node) → **5**

Do **not** count the 5 FAQ documents returned by `search` — that is tool payload size, not span count.

**Answer: 5**

### Side quest: broken `pandas` in HW venv

`minsearch` imports `pandas`; the HW `.venv` had a broken pandas install (`ModuleNotFoundError: pandas.util`). Fixed by linking a working Anaconda pandas/numpy into the venv, then `main.py` exited **0** and traces appeared in Logfire.

---

## Q2 — Load Logfire traces into DuckDB with dlt

### Read token

Logfire → project **Settings** → **Read tokens** → create → `LOGFIRE_READ_TOKEN` in `.env` (write ≠ read).

### Pipeline

**Script:** `logfire_pipeline.py`

- Region: `https://logfire-us.pydantic.dev` (US project)
- API: `POST /v2/query` with SQL `SELECT * FROM records …`
- Parse nested JSON attributes so dlt creates child tables
- Destination DuckDB, **`dataset_name="agent_traces"`**
- `pipeline_name="logfire_agent_traces"` (must differ from dataset name — identical names confuse DuckDB binder)

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\LLM_dlt_HW
# dlt native deps in HW venv were flaky; use workshop workbench interpreter
E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\Workshop\workbench\.venv\Scripts\python.exe logfire_pipeline.py
```

**Observed load:** 12 Logfire records → `logfire_agent_traces.duckdb` / schema `agent_traces`.

### Table count (homework SQL)

```sql
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'agent_traces';
```

Helper:

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\LLM\dlt\LLM_dlt_HW
python .\count_tables.py
```

**Local result: 23**

| Experiment | Table count |
|------------|-------------|
| `records` only (homework intent) | **23** |
| `records` + `metrics` | 29 (too many; not used for answer) |

Form choices are only **1 / 3 / 24 / 100**. Nested JSON normalization produces ~20+ tables; course expected choice is **24**. Trace content can shift child tables by ±1.

**Answer: 24**

---

## Q3 — Sum input tokens for the Q1 agent run

Tokens live on span attributes as `gen_ai.usage.input_tokens` (DuckDB column: `attributes__gen_ai_usage_input_tokens`). Sum across **LLM chat spans** in the same `trace_id` as Q1.

Q1 run at **21:30** (`How do I run Ollama locally?`):

| span | input_tokens |
|------|--------------|
| chat #1 | 241 |
| chat #2 | 1539 |
| **sum** | **1780** |

Other identical Ollama runs: **1776–1780**.

| Range choice | Fits? |
|--------------|-------|
| 100 - 500 | no |
| **1500 - 5000** | **yes (1780)** |
| 10000 - 20000 | no |
| 50000 - 100000 | no |

**Answer: 1500 - 5000**

---

## Files produced

```text
LLM_dlt_HW/
  main.py                 # Logfire instrument + agent entry
  agent.py                # Pydantic AI FAQ agent (Cerebras/Gemma)
  ingest.py               # FAQ index
  logfire_pipeline.py     # Logfire → DuckDB (agent_traces)
  count_tables.py         # Q2 COUNT(*) helper
  LLM_dlt_HW.md           # this write-up
  .env.example            # key names only (no secrets)
```

`.env`, `*.duckdb`, `.venv/` are gitignored.

---

## Process summary (learner trail)

1. Prefer **token in `.env`** over `uv` + `logfire auth` when `uv` hangs.  
2. Entry point is **`main.py`**, not `agent.py`.  
3. Logfire Live **K/numeric badges** near a run are often **tokens**, not span counts — expand the tree.  
4. Search returning **5 FAQ rows ≠ 5 spans**.  
5. dlt nested normalization → many child tables; local **23** ≈ form **24**.  
6. Q3 = sum LLM `input_tokens` only (not the parent aggregated badge alone, though it matched ~1.78K).  
