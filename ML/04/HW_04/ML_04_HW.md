# ML Zoomcamp 2026 — Homework 4: Evaluation Metrics for Classification

Notebook: [`[2026]_HW_04.ipynb`](./%5B2026%5D_HW_04.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | **lead_score** |
| 2 | **0.732** |
| 3 | **0.63** |
| 4 | **0.41** |
| 5 | **0.007** |
| 6 | **0.001** |

---

## Setup

Ran the notebook in local Jupyter (nbclassic), same ML Zoomcamp `.venv` as Module 4.

- Data: `data/course_lead_scoring_2026.csv` (2026 pinned lead-scoring release — same file as HW3, **different split seed**)
- Official: `materials/homework.md` (do not edit)
- Launch: `bash run-nbclassic.sh` (port **8891**; 8888/8889/8890 are other notebooks)
- Kernel: this folder `.venv`. Do not use `!pip` / `!wget`

---

## Dataset

Target: `converted` (client signed up or not).

Missing values: categorical → `'NA'`; numerical → `0.0`.

Split (exact — `random_state=1`, not 42):

```python
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
df_train, df_val = train_test_split(
    df_full_train, test_size=0.25, random_state=1
)
```

Keep `converted` out of the feature dataframes.

---

## Q1 — ROC AUC feature importance

**Question:** Which numerical variable (among the following 4) has the highest AUC?

- `lead_score`
- `number_of_courses_viewed`
- `interaction_count`
- `annual_income`

Use the **training** set. If AUC < 0.5, negate the feature.

```python
# roc_auc_score(y_train, df_train[col])
# if auc < 0.5: roc_auc_score(y_train, -df_train[col])
```

**Output:**

```text
lead_score: 0.788
number_of_courses_viewed: 0.723
interaction_count: 0.765
annual_income: 0.608
```

**Answer:** **lead_score**

---

## Q2 — Model AUC (validation)

**Question:** What's the AUC of this model on the validation dataset? (round to 3 digits)

- 0.532
- 0.632
- 0.732
- 0.832

```python
LogisticRegression(solver='liblinear', C=1.0, max_iter=1000)
```

One-hot encode with `DictVectorizer`. Official snippet has **no** `random_state` on the model. AUC uses `predict_proba[:, 1]` on the validation set.

**Output:**

```text
0.732
```

**Answer:** **0.732**

---

## Q3 — Precision and recall intersection

**Question:** At which threshold precision and recall curves intersect?

- 0.43
- 0.63
- 0.73
- 0.83

Thresholds from 0.0 to 1.0 with step 0.01. Ignore thresholds where both metrics are zero, and rows where precision is undefined (`tp + fp == 0`). Choose the threshold with the smallest absolute difference between precision and recall.

**Output:**

```text
0.63
```

**Answer:** **0.63**

---

## Q4 — Max F1 threshold

**Question:** At which threshold F1 is maximal?

- 0.21
- 0.41
- 0.61
- 0.81

$$F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$

Same threshold grid as Q3. The form asks for the threshold, not the F1 value.

**Output:**

```text
threshold      0.410000
tp           572.000000
fp           352.000000
fn            14.000000
precision      0.619048
recall         0.976109
f1             0.757616
```

**Answer:** **0.41**

---

## Q5 — 5-fold CV standard deviation

**Question:** How large is standard deviation of the scores across different folds?

- 0.001
- 0.007
- 0.013
- 0.060

```python
KFold(n_splits=5, shuffle=True, random_state=1)
```

Folds of `df_full_train` only. Each fold fits `DictVectorizer` on that fold's train and scores validation AUC with `predict_proba[:, 1]`. Standard deviation is `np.std` (not pandas `.std()`).

**Output:**

```text
0.006853233151022138
```

Rounded to 3 digits: **0.007**.

**Answer:** **0.007**

---

## Q6 — Best `C` (5-fold mean AUC)

**Question:** Which `C` leads to the best mean ROC AUC?

- 0.000001
- 0.001
- 1

```python
C_values = [0.000001, 0.001, 1]
```

Round mean and std to 3 decimal digits. Ties: lowest std, then smallest `C`.

**Output:**

```text
C=1e-06: mean AUC = 0.617, std = 0.019
C=0.001: mean AUC = 0.749, std = 0.010
C=1: mean AUC = 0.732, std = 0.007
```

**Answer:** **0.001**
