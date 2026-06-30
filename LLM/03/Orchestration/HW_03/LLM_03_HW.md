# LLM Zoomcamp 2026 — Homework 3: AI Orchestration with Kestra

Submission write-up for **Homework 3: AI Orchestration with Kestra**.

**Course:** [LLM Zoomcamp 2026](https://courses.datatalks.club)  
**Official homework:** [cohorts/2026/03-orchestration/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/03-orchestration/homework.md)  
**Submit form:** https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw3

**Local Kestra materials:** `ZoomCamp/LLM/03/materials/`  
**Imported flows namespace:** `zoomcamp`

> Homework Q3–Q5 use `4_simple_agent.yaml` in course materials (`materials/flows/`).

---

## Homework form answers

| # | Form choice |
|---|-------------|
| 1 | **Copilot has access to current Kestra plugin documentation** |
| 2 | **Vague, generic, or fabricated — the model guesses from training data** |
| 3 | **60-100 tokens** |
| 4 | **2-5x more** |
| 5 | **2-4x more** |
| 6 | **Use traditional task-based workflows for predictability and auditability** |

---

## Setup

Kestra runs locally from `materials/` with Docker Compose. API keys are in `.env` (base64 `SECRET_*` values).

**Start Kestra:**

```bash
cd /e/IT_SPACES/AI/ZoomCamp/LLM/03/materials
docker compose up -d
docker compose ps
```

**Import flows:**

```bash
powershell ./import-flows.ps1
```

**Kestra UI:** http://localhost:8080 (`admin@kestra.io` / `Admin1234!`)

**Prompt for Q1 (ChatGPT and Kestra AI Copilot):**

```text
Create a Kestra flow that loads NYC taxi data from CSV to BigQuery
```

---

## Q1 — Context Engineering

Same prompt in ChatGPT (private window) vs Kestra AI Copilot.

### ChatGPT output

```yaml
id: nyc_taxi_csv_to_bigquery
namespace: dataengineering

variables:
  project_id: your-gcp-project
  dataset: nyc_taxi
  table: yellow_tripdata
  bucket: your-gcs-bucket

tasks:
  - id: download_csv
    type: io.kestra.plugin.core.http.Download
    uri: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.csv

  - id: upload_to_gcs
    type: io.kestra.plugin.gcp.gcs.Upload
    from: "{{ outputs.download_csv.uri }}"
    bucket: "{{ vars.bucket }}"
    name: yellow_tripdata_2024-01.csv

  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.LoadFromGcs
    serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
    projectId: "{{ vars.project_id }}"
    destinationTable: "{{ vars.project_id }}.{{ vars.dataset }}.{{ vars.table }}"
    sourceUris:
      - "gs://{{ vars.bucket }}/yellow_tripdata_2024-01.csv"
    format: CSV
    autodetect: true
    writeDisposition: WRITE_TRUNCATE
    createDisposition: CREATE_IF_NEEDED
    csvOptions:
      skipLeadingRows: 1
```

**Observation:** ChatGPT found a plausible NYC taxi CSV URL, but used non-existent or incorrect Kestra plugin types (`LoadFromGcs`, `gcs.Upload`) — hallucinated Kestra-specific syntax.

### Kestra AI Copilot output

```yaml
# Please replace the 'uri' in the 'download_taxi_data' task with the actual URL of the NYC taxi data CSV file.
# Also, update the 'destinationTable' in the 'load_to_bigquery' task with your BigQuery project, dataset, and table name.
id: cockroach_390559
namespace: company.team

tasks:
  - id: download_taxi_data
    type: io.kestra.plugin.core.http.Download
    uri: https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2021-financial-year-provisional/Download-data/annual-enterprise-survey-2021-financial-year-provisional-csv.csv
    saveAs: nyc_taxi_data.csv
  - id: load_to_bigquery
    type: io.kestra.plugin.gcp.bigquery.Load
    from: "{{ outputs.download_taxi_data.uri }}"
    destinationTable: your_project_id.your_dataset.nyc_taxi_data
    format: CSV
    csvOptions:
      skipLeadingRows: 1
      fieldDelimiter: ","
```

**Observation:** Copilot used a wrong sample data URL, but generated **valid Kestra plugin types** (`io.kestra.plugin.core.http.Download`, `io.kestra.plugin.gcp.bigquery.Load`) that the engine recognizes.

**Answer:** **Copilot has access to current Kestra plugin documentation**

**Why:** Generic ChatGPT relies on stale training data and invents plugin names. Kestra Copilot injects current plugin documentation as context, so YAML structure matches real Kestra tasks even when domain facts (CSV URL) are wrong.

---

## Q2 — RAG vs No RAG

Executed in Kestra UI:

- `zoomcamp` / `1_chat_without_rag`
- `zoomcamp` / `2_chat_with_rag`

Both flows ask: *"Which features were released in Kestra 1.1?"*

The homework asks how to describe the **non-RAG** response.

### Without RAG (`1_chat_without_rag.yaml`)

The model returned a long, confident list of features (e.g. plugin management UI, flow-level retry policies, worker API). The text sounds specific, but several items do **not** match actual Kestra 1.1 release notes — they are plausible combinations from general orchestration knowledge (fabrication / hallucination).

### With RAG (`2_chat_with_rag.yaml`)

```text
Kestra 1.1 introduced several major features, including:

1. **New Filters**: Redesigned UI filters ...
2. **No-Code Dashboard Editor**: Extended the no-code multi-panel editor ...
3. **Human Task**: Introduced human-in-the-loop workflows ...
4. **Multi-Agent AI Systems**: Enhanced AI agents to use other AI agents as tools ...
5. **Fix with AI**: Provided AI-powered suggestions for troubleshooting failed tasks ...
```

**Observation:** RAG version lists features grounded in ingested release documentation. Non-RAG version is detailed but unreliable — vague, generic, or fabricated.

**Answer:** **Vague, generic, or fabricated — the model guesses from training data**

---

## Q3 — Token usage (short summary)

Flow: `4_simple_agent.yaml`  
Input: `summary_length = short` (other inputs at defaults)  
Task measured: `multilingual_agent` (from `log_token_usage`)

**Token usage (`multilingual_agent`):**

```text
Input tokens:  282
Output tokens: 79
Total tokens:  361
```

**Answer:** **60-100 tokens** (79 falls in this range)

---

## Q4 — Token usage (long summary)

Flow: `4_simple_agent.yaml`  
Input: `summary_length = long`

**Token usage (`multilingual_agent`):**

```text
Input tokens:  282
Output tokens: 185
Total tokens:  467
```

**Comparison to Q3:**

| Setting | Output tokens (`multilingual_agent`) |
|---------|--------------------------------------|
| short   | 79                                   |
| long    | 185                                  |

185 ÷ 79 ≈ **2.3×**

**Answer:** **2-5x more**

---

## Q5 — Modifying a flow

In Kestra flow editor, `english_brevity` prompt changed from **exactly 1 sentence** to **exactly 3 sentences**. Flow saved and run with `summary_length = long`.

### Baseline (Q4 run, 1-sentence `english_brevity`, `summary_length = long`)

```text
English Brevity Agent:
- Output tokens: 53
```

### After modification (3-sentence `english_brevity`, `summary_length = long`)

```text
English Brevity Agent:
- Output tokens: 95
```

95 ÷ 53 ≈ **1.8×** (within the 2–4× range)

**Answer:** **2-4x more**

---

## Q6 — Best Practices

Scenario: production workflows needing **deterministic, repeatable, auditable** results (financial reporting, regulated industries).

**Answer:** **Use traditional task-based workflows for predictability and auditability**

**Why:** AI agents introduce non-deterministic outputs. For strict compliance and audit trails, explicit task-based workflows with fixed execution paths are the appropriate production pattern.

---

## Environment

| Item | Notes |
|------|--------|
| Kestra | `kestra/kestra:v1.3.21` via Docker Compose |
| Location | `E:\IT_SPACES\AI\ZoomCamp\LLM\03\materials` |
| LLM | Google Gemini (`gemini-2.5-flash`) |
| Secrets | `.env` with `GEMINI_API_KEY`, `SECRET_GEMINI_API_KEY`, `SECRET_TAVILY_API_KEY` (base64) |
| Docker data | Stored on E: drive (not C:) |

---

## Notes

- Flow `3_rag_with_websearch.yaml` was modified locally to use Gemini instead of OpenAI; not required for homework Q1–Q6.
- Flow `5_web_research_agent` `log_report` task falls back to `textOutput` when `research_report.md` is not saved by MCP filesystem on Windows.
