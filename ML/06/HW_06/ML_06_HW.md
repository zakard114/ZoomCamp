# ML Zoomcamp 2026 — Homework 6: Decision Trees and Ensemble Learning

Notebook: [`[2026]_HW_06.ipynb`](./%5B2026%5D_HW_06.ipynb)

---

## Form answers

| # | Answer |
|---|--------|
| 1 | **model_year** |
| 2 | **1.837** |
| 3 | **150** |
| 4 | **10** |
| 5 | **vehicle_weight** |
| 6 | **0.1** |

---

## Setup

Ran locally with shared ML Zoomcamp `.venv` (nbclassic / script). Answers computed on the pinned 2026 CSV.

- Data: `data/car_fuel_efficiency_2026.csv` (2026 pinned release)
- Launch: `bash run-nbclassic.sh` or `.\run-nbclassic.ps1` (port **8891**)
- Kernel: this folder `.venv` → `ML\.venv`. Do not use `!pip` / `!wget`

---

## Dataset

Target: `fuel_efficiency_mpg` (regression).

Missing values: fill with zeros.

Split (exact):

```python
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
df_train, df_val = train_test_split(
    df_full_train, test_size=0.25, random_state=1
)
```

`DictVectorizer(sparse=True)` for feature matrices.

---

## Q1 — Decision tree split feature

**Question:** `DecisionTreeRegressor(max_depth=1)`. Which original feature is used for the split?

- `vehicle_weight`
- `model_year`
- `origin`
- `fuel_type`

If the tree prints a one-hot name such as `origin=USA`, map it back to the original column.

```python
dt = DecisionTreeRegressor(max_depth=1)
dt.fit(X_train, y_train)
print(export_text(dt, feature_names=dv.feature_names_))
```

**Output:**

```text
|--- model_year <= 1997.50
|   |--- value: [28.61]
|--- model_year >  1997.50
|   |--- value: [31.17]
```

**Answer:** **model_year**

---

## Q2 — Random forest RMSE

**Question:** `RandomForestRegressor(n_estimators=10, random_state=1, n_jobs=-1)`. Validation RMSE?

- 0.1837
- 1.837
- 18.37
- 183.7

```python
rf = RandomForestRegressor(n_estimators=10, random_state=1, n_jobs=-1)
rf.fit(X_train, y_train)
root_mean_squared_error(y_val, rf.predict(X_val))
```

**Output:**

```text
1.8332197358745623
```

Closest option (form rule): **1.837**

**Answer:** **1.837**

---

## Q3 — n_estimators

**Question:** Try `[10, 50, 100, 150]`, `random_state=1`. Which value has the lowest validation RMSE (3 decimal places)?

- 10
- 50
- 100
- 150

```python
for n in [10, 50, 100, 150]:
    model = RandomForestRegressor(n_estimators=n, random_state=1, n_jobs=-1)
    model.fit(X_train, y_train)
    rmse = root_mean_squared_error(y_val, model.predict(X_val))
    print(n, round(rmse, 3))
```

**Output:**

```text
10 1.833
50 1.774
100 1.77
150 1.769
```

**Answer:** **150**

---

## Q4 — max_depth by mean RMSE

**Question:** `max_depth` in `[10, 15, 20, 25]`. For each depth, `n_estimators` in `[10, 50, 100, 150]`. Best `max_depth` by mean RMSE. `random_state=1`.

- 10
- 15
- 20
- 25

```python
for depth in [10, 15, 20, 25]:
    rmses = []
    for n in [10, 50, 100, 150]:
        model = RandomForestRegressor(
            n_estimators=n, max_depth=depth, random_state=1, n_jobs=-1
        )
        model.fit(X_train, y_train)
        rmses.append(root_mean_squared_error(y_val, model.predict(X_val)))
    print(depth, round(float(np.mean(rmses)), 3))
```

**Output:**

```text
10 1.754
15 1.784
20 1.787
25 1.786
```

**Answer:** **10**

---

## Q5 — Feature importance

**Question:** `n_estimators=10`, `max_depth=20`, `random_state=1`. Most important among:

- `vehicle_weight`
- `horsepower`
- `acceleration`
- `engine_displacement`

```python
rf = RandomForestRegressor(
    n_estimators=10, max_depth=20, random_state=1, n_jobs=-1
)
rf.fit(X_train, y_train)
importances = pd.Series(rf.feature_importances_, index=dv.feature_names_)
importances.sort_values(ascending=False).head(10)
```

**Output (top rows):**

```text
model_year              0.296
vehicle_weight          0.203
fuel_type=Gasoline      0.161
horsepower              0.078
engine_displacement     0.061
acceleration            0.055
```

Among the four choices, **vehicle_weight** is highest.

**Answer:** **vehicle_weight**

---

## Q6 — XGBoost eta

**Question:** 100 rounds. `eta` 0.3 vs 0.1. Which is best on validation RMSE?

- 0.3
- 0.1
- Both give equal value

```python
xgb_params = {
    'eta': 0.3,
    'max_depth': 6,
    'min_child_weight': 1,
    'objective': 'reg:squarederror',
    'nthread': 8,
    'seed': 1,
    'verbosity': 1,
}
# train twice with eta 0.3 and 0.1, num_boost_round=100
```

**Output:**

```text
eta=0.3  RMSE=1.8264579799904583
eta=0.1  RMSE=1.724810059827976
```

**Answer:** **0.1**

---

## Learning in Public

Share a short post with `#mlzoomcamp` (no secrets). Submit the post link with the homework.

**Post link:**

---

If a numerical answer does not match an option exactly, pick the closest. If exactly between two options, pick the higher value.
