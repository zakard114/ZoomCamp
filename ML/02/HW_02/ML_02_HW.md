# ML Zoomcamp 2026 — Homework 2: Machine Learning for Regression

Notebook: [`[2026]_HW_02.ipynb`](./%5B2026%5D_HW_02.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | **horsepower** |
| 2 | **254** |
| 3 | **With mean** |
| 4 | **0** |
| 5 | **0.029** |
| 6 | **2.236** |

---

## Setup

Ran the notebook in local Jupyter (nbclassic), same ML Zoomcamp `.venv` as Module 2.

- Data: `data/car_fuel_efficiency_2026.csv` (2026 pinned release; also loaded from the course URL)
- Official: `materials/homework.md` (do not edit)
- Launch: `bash run-nbclassic.sh` (not `jupyter notebook`)

---

## Q1 — Missing values column

**Question:** There's one column with missing values. What is it?

- `'engine_displacement'`
- `'horsepower'`
- `'vehicle_weight'`
- `'model_year'`

```python
df.isnull().sum()
```

**Output:**

```text
engine_displacement      0
horsepower             877
vehicle_weight           0
model_year               0
fuel_efficiency_mpg      0
```

**Answer:** **horsepower**

---

## Q2 — Horsepower median

**Question:** What's the median (50% percentile) for variable `'horsepower'`?

- 204
- 254
- 304
- 354

```python
df["horsepower"].median()
```

**Output:**

```text
254.0
```

**Answer:** **254**

---

## Q3 — Fill NA: 0 vs mean (RMSE)

**Question:** Which option gives better RMSE?

- With 0
- With mean
- Both are equally good

Split 60/20/20 with `seed=42`. Target is raw `fuel_efficiency_mpg` (no log). Mean of `horsepower` from **train only**. RMSE rounded to 3 decimals.

```python
mean_hp = df_train.horsepower.mean()
rmse_0 = round(rmse(y_val, w0 + X_val_0.dot(w)), 3)
rmse_m = round(rmse(y_val, w0 + X_val_m.dot(w)), 3)
```

**Output:**

```text
RMSE (Filled with 0): 2.205
RMSE (Filled with mean): 2.202
```

**Answer:** **With mean**

---

## Q4 — Best regularization `r`

**Question:** Which `r` gives the best RMSE?

- 0
- 0.01
- 0.1
- 1
- 5
- 10
- 100

Fill NA with 0. RMSE rounded to 4 decimals. Tie → smallest `r`.

```python
for r in [0, 0.01, 0.1, 1, 5, 10, 100]:
    w0, w = train_linear_regression_reg(X_train, y_train, r=r)
    score = round(rmse(y_val, w0 + X_val.dot(w)), 4)
    print(r, score)
```

**Output:**

```text
r=0     -> RMSE: 2.2053
r=0.01  -> RMSE: 2.2058
r=0.1   -> RMSE: 2.2241
r=1     -> RMSE: 2.3492
r=5     -> RMSE: 2.4094
r=10    -> RMSE: 2.4195
r=100   -> RMSE: 2.4292
```

**Answer:** **0**

---

## Q5 — Std of RMSE across seeds

**Question:** What's the value of std?

- 0.006
- 0.016
- 0.029
- 0.036

Seeds `0`–`9`, NA filled with 0, no regularization, `np.std` then `round(std, 3)`.

```python
round(np.std(scores), 3)
```

**Output:**

```text
0.029
```

**Answer:** **0.029**

---

## Q6 — Test RMSE (seed 9, r=0.001)

**Question:** What's the RMSE on the test dataset?

- 0.236
- 2.236
- 22.10
- 221.0

Split with `seed=9`, combine train+val, fill NA with 0, `r=0.001`, evaluate on test.

```python
score = rmse(y_test, y_pred)
print(round(score, 3))
```

**Output:**

```text
2.236
```

**Answer:** **2.236**
