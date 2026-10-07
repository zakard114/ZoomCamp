# ML Zoomcamp 2026 — Homework 3: Machine Learning for Classification

Notebook: [`[2026]_HW_03.ipynb`](./%5B2026%5D_HW_03.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | **technology** |
| 2 | **interaction_count and lead_score** |
| 3 | **lead_source** |
| 4 | **0.65** |
| 5 | **number_of_courses_viewed** |
| 6 | **0.001** |

---

## Setup

Ran the notebook in local Jupyter (nbclassic), same ML Zoomcamp `.venv` as Module 3.

- Data: `data/course_lead_scoring_2026.csv` (2026 pinned lead-scoring release)
- Official: `materials/homework.md` (do not edit)
- Launch: `bash run-nbclassic.sh` (port **8890**; 8888/8889 are other courses)
- Kernel: this folder `.venv`. Do not use `!pip` / `!wget`

---

## Dataset

Target: `converted` (client signed up or not).

Missing values: categorical → `'NA'`; numerical → `0.0`.

Split (exact):

```python
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
df_train, df_val = train_test_split(
    df_full_train, test_size=0.25, random_state=42
)
```

Keep `converted` out of the feature dataframes.

---

## Q1 — Mode of `industry`

**Question:** What is the most frequent observation (mode) for the column `industry`?

- `NA`
- `technology`
- `healthcare`
- `retail`

```python
df["industry"].mode()
# or df["industry"].value_counts()
```

**Output:**

```text
Q1 mode: technology
```

**Answer:** **technology**

---

## Q2 — Biggest correlation (numerical features)

**Question:** What are the two features that have the biggest correlation?

- `interaction_count` and `lead_score`
- `number_of_courses_viewed` and `lead_score`
- `number_of_courses_viewed` and `interaction_count`
- `annual_income` and `interaction_count`

Only consider the pairs above.

```python
df[numerical].corr()
```

**Output:**

```text
1. interaction_count & lead_score: 0.9287123432397134
2. number_of_courses_viewed & lead_score: 0.769352062184664
3. number_of_courses_viewed & interaction_count: 0.7216090038937035
4. annual_income & interaction_count: 0.10637458469219016
```

**Answer:** **interaction_count and lead_score**

---

## Q3 — Mutual information (train set)

**Question:** Which variable has the biggest mutual information score with `converted`? Round to 2 decimals.

- `industry`
- `location`
- `lead_source`
- `employment_status`

```python
# training set only
# round(score, 2)
```

**Output:**

```text
lead_source          0.03
employment_status    0.02
location             0.00
industry             0.00
```

**Answer:** **lead_source**

---

## Q4 — Logistic regression accuracy (validation)

**Question:** What accuracy did you get? Round to 2 decimal digits.

- 0.55
- 0.65
- 0.75
- 0.85

```python
model = LogisticRegression(solver='liblinear', C=1.0, max_iter=1000, random_state=42)
```

Include categorical features with one-hot encoding.

**Output:**

```text
Q4 validation accuracy: 0.65
```

**Answer:** **0.65**

---

## Q5 — Feature elimination (smallest difference)

**Question:** Which of the following features has the smallest difference vs the original accuracy?

- `'lead_source'`
- `'number_of_courses_viewed'`
- `'interaction_count'`

Difference does not have to be positive. Compare without rounding the original accuracy.

**Output:**

```text
Baseline accuracy (unrounded): 0.645
[without lead_source] accuracy: 0.64200 | difference (baseline - without): 0.00300
[without number_of_courses_viewed] accuracy: 0.64300 | difference (baseline - without): 0.00200
[without interaction_count] accuracy: 0.60100 | difference (baseline - without): 0.04400
```

**Answer:** **number_of_courses_viewed**

---

## Q6 — Regularized `C`

**Question:** Which `C` leads to the best accuracy on validation? Round to 3 decimal digits.

- 0.000001
- 0.00001
- 0.0001
- 0.001

If there are multiple options, select the smallest `C`.

```python
C_values = [0.000001, 0.00001, 0.0001, 0.001]
```

**Output:**

```text
C=1e-06  accuracy=0.59800  round3=0.598
C=1e-05  accuracy=0.59800  round3=0.598
C=0.0001  accuracy=0.61300  round3=0.613
C=0.001  accuracy=0.64500  round3=0.645
```

**Answer:** **0.001**
