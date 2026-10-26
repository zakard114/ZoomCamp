# ML Zoomcamp 2026 — Homework 5: Deploying Machine Learning Models

Notebook: [`[2026]_HW_05.ipynb`](./%5B2026%5D_HW_05.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | `uv 0.13.5` (not graded) |
| 2 | **1.7.2** |
| 3 | |
| 4 | |
| 5 | **python:3.11.15-slim-bookworm** |
| 6 | |

Q3/Q4 were run once on the shared venv (scikit-learn 1.9.0) against a 1.7.2 pickle. It warned the versions do not match, so those probabilities are not written here. Q6 was not run in Docker.

Submit: https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw05

`homework.yaml` `due_at`: `2026-10-19T23:00:00Z`. The form was already opened on 2026-10-26.

---

## Setup

uv / FastAPI / Docker homework. The notebook holds notes and the homework commands. It does not retrain a model and it does not compute a conversion probability.

- Official: `materials/homework.md` (do not edit)
- Python: 3.11.15 (`.python-version`)
- Frozen artifact: `pipeline.bin`
- Expected sha256: `1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1`
- Data named by the homework: `data/course_lead_scoring_2026.csv`
- Launch: `bash run-nbclassic.sh` (port **8893**; 8888/8890/8891/8892 are other modules). Leave the server down.
- Kernel: this folder `.venv` → `ML\.venv`. Do not use `!pip` / `!wget`
- Image tag for this assignment: `zoomcamp-model:2026-hw5`. `README.md` says `zoomcamp-model:2026-hw10` because the artifact is reused later.
- `uv sync --locked` was started once because `sklearn` and `uvicorn` were missing from this folder `.venv`. It stayed on `Downloading numpy` / `Downloading scikit-learn` with no `Downloaded` line, so it was stopped. Sync is incomplete.

Homework setup commands (not run in this scaffold — no `smoke_test.py`, no `uvicorn`, no Docker):

```bash
uv sync --locked
sha256sum pipeline.bin
```

Model line from the homework:

```python
LogisticRegression(solver="liblinear", C=1.0)
```

with a `DictVectorizer` in front. Graded inference loads `pipeline.bin`. There is no `train_test_split` in this homework.

---

## Q1 — environment check

**Question:** Run `uv --version` and record the version in your notes. This is a setup check, not a graded answer: your local `uv` version is not a property of the model.

```bash
uv --version
```

**Answer:**

---

## Q2 — locked dependency

**Question:** Open `pyproject.toml` and `uv.lock`. Which Scikit-Learn version is part of the 2026 reference environment?

- `1.6.1`
- `1.7.2`
- `1.8.0`
- `2.0.0`

Do not regenerate the lockfile for the graded run; use `uv sync --locked`.

**Answer:**

---

## Q3 — load the model

**Question:** Write a Python script that loads `pipeline.bin` with `pickle` and calls `predict_proba` for this paid-ads lead. Report the probability of conversion rounded to three decimal places. The grader accepts an absolute error of at most `0.005`; do not choose the nearest answer from a list.

```json
{
  "lead_source": "paid_ads",
  "industry": "technology",
  "employment_status": "employed",
  "location": "north_america",
  "number_of_courses_viewed": 2,
  "annual_income": 79276.0,
  "interaction_count": 4,
  "lead_score": 0.41
}
```

**Answer:**

---

## Q4 — serve the model

**Question:** Start the provided API and POST this organic-search lead to `/predict`. Report `conversion_probability` rounded to three decimal places. The same `0.005` absolute tolerance applies. The response must contain a probability in `[0, 1]` and a boolean `conversion` field.

```bash
uv run uvicorn predict:app --host 0.0.0.0 --port 9696
```

```bash
curl -s http://localhost:9696/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "lead_source": "organic_search",
    "industry": "technology",
    "employment_status": "employed",
    "location": "europe",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0,
    "interaction_count": 7,
    "lead_score": 0.74
  }'
```

**Answer:**

---

## Q5 — container base image

**Question:** Which Python base-image tag is declared in the Dockerfile?

- `python:3.9-slim-bullseye`
- `python:3.11.15-slim-bookworm`
- `python:3.12-slim-bookworm`
- `python:3.13.10-slim-bookworm`

This question checks a version-controlled declaration. The displayed size of a local Docker image is not graded.

Build tag for this assignment (do not build in this scaffold):

```bash
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

`README.md` uses `zoomcamp-model:2026-hw10` because the artifact is reused later.

**Answer:**

---

## Q6 — run the container

**Question:** Run the same request from Question 4 against the container. Report `conversion_probability` rounded to three decimal places. The expected result is the same reference inference as Question 4, with the same `0.005` absolute tolerance. Also verify `GET /health` returns `{"status":"ok", ...}` and the model checksum recorded in `model_metadata.json`.

```bash
python q6_test.py
```

```bash
curl -s http://localhost:9696/health
```

**Answer:**
