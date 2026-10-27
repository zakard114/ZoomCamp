# ML Zoomcamp 2026 — Homework 5: Deploying Machine Learning Models

Notebook: [`[2026]_HW_05.ipynb`](./%5B2026%5D_HW_05.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | `uv 0.13.5 (46776a95d 2026-10-21 x86_64-pc-windows-msvc)` (not graded) |
| 2 | **1.7.2** |
| 3 | **0.533** |
| 4 | **0.770** |
| 5 | **python:3.11.15-slim-bookworm** |
| 6 | **0.770** |

---

## Setup

Ran the notebook in local Jupyter (nbclassic) on the shared ML Zoomcamp `.venv`.

- Official: `materials/homework.md` (do not edit)
- Kernel: `E:\IT_SPACES\AI\ZoomCamp\ML\05\HW_05\.venv` → `E:\IT_SPACES\AI\ZoomCamp\ML\.venv`. Skill rule (`zoomcamp-shared-venv`, `ml-zoomcamp-hw-setup`): shared venv junction; installed scikit-learn is 1.9.0; `pipeline.bin` was created with 1.7.2.
- Launch: `bash run-nbclassic.sh` (port **8893**; 8888/8890/8891/8892 are other modules). Leave that server running.
- Do not use `!pip` / `!wget`
- Frozen artifact: `pipeline.bin`
- Expected sha256: `1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1`
- Data named by the homework: `data/course_lead_scoring_2026.csv`
- Image tag: `zoomcamp-model:2026-hw5`
- Q6: build/run that image, then `python q6_test.py` or the notebook `requests` cell against `localhost:9696` (not a local pickle load)

Model line from the homework:

```python
LogisticRegression(solver="liblinear", C=1.0)
```

with a `DictVectorizer` in front. Graded inference loads `pipeline.bin`.

---

## Q1 — environment check

**Question:** Run `uv --version` and record the version in your notes. This is a setup check, not a graded answer: your local `uv` version is not a property of the model.

```bash
uv --version
```

**Answer:** `uv 0.13.5 (46776a95d 2026-10-21 x86_64-pc-windows-msvc)`

---

## Q2 — locked dependency

**Question:** Open `pyproject.toml` and `uv.lock`. Which Scikit-Learn version is part of the 2026 reference environment?

- `1.6.1`
- `1.7.2`
- `1.8.0`
- `2.0.0`

The graded value is the lockfile version. The shared venv’s installed package is 1.9.0.

**Answer:** **1.7.2**

---

## Q3 — load the model

**Question:** Load `pipeline.bin` with `pickle` and call `predict_proba` for this paid-ads lead. Report the probability of conversion rounded to three decimal places. Absolute error at most `0.005`. There is no option list.

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

**Output:**

```text
0.532994
```

Rounded to 3 digits: **0.533**.

**Answer:** **0.533**

---

## Q4 — serve the model

**Question:** Score this organic-search lead and report `conversion_probability` rounded to three decimal places. The same `0.005` absolute tolerance applies. The response must contain a probability in `[0, 1]` and a boolean `conversion` field.

```json
{
  "lead_source": "organic_search",
  "industry": "technology",
  "employment_status": "employed",
  "location": "europe",
  "number_of_courses_viewed": 4,
  "annual_income": 80304.0,
  "interaction_count": 7,
  "lead_score": 0.74
}
```

**Output:**

```text
0.769799
```

Rounded to 3 digits: **0.770**.

**Answer:** **0.770**

---

## Q5 — container base image

**Question:** Which Python base-image tag is declared in the Dockerfile?

- `python:3.9-slim-bullseye`
- `python:3.11.15-slim-bookworm`
- `python:3.12-slim-bookworm`
- `python:3.13.10-slim-bookworm`

This question checks a version-controlled declaration. The displayed size of a local Docker image is not graded.

**Answer:** **python:3.11.15-slim-bookworm**

---

## Q6 — run the container

**Question:** Run the same request from Question 4 against the container. Report `conversion_probability` rounded to three decimal places. The expected result is the same reference inference as Question 4, with the same `0.005` absolute tolerance. Also verify that `/health` returns `{"status":"ok", ...}` and the model checksum recorded in `model_metadata.json`.

Build and run the image in a terminal from `HW_05` first (this blocks that terminal):

```bash
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

Then either run `python q6_test.py` in another terminal, or the notebook cell that `POST`s to `/predict` and `GET`s `/health` on `localhost:9696`.

**Output:**

```text
0.770
```

**Answer:** **0.770**
