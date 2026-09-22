# ML Zoomcamp 2026 — Homework 1: Introduction to Machine Learning

Submission write-up for Module 01 homework  
(Pandas / NumPy refresh on the pinned 2026 car fuel-efficiency dataset).

**Course:** [Machine Learning Zoomcamp 2026](https://courses.datatalks.club/ml-zoomcamp-2026/)  
**Instructions:** [`materials/homework.md`](materials/homework.md) · [upstream homework.md](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/01-intro/homework.md)  
**Submit form:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw01

**Local folder:** `E:\IT_SPACES\AI\ZoomCamp\ML\01\HW_01\`  
**Working notebook:** [`[2026]_HW_01.ipynb`](./%5B2026%5D_HW_01.ipynb)  
**Homework URL (paste into form):** https://github.com/zakard114/ZoomCamp/tree/main/ML/01/HW_01  
**Notebook on GitHub:** https://github.com/zakard114/ZoomCamp/blob/main/ML/01/HW_01/%5B2026%5D_HW_01.ipynb  
**This write-up on GitHub:** https://github.com/zakard114/ZoomCamp/blob/main/ML/01/HW_01/ML_01_HW.md

**FAQ contribution (optional):** https://github.com/DataTalksClub/faq/issues/281

---

## Homework form answers (paste-ready)

| # | Answer |
|---|--------|
| 1 | **3.0.5** |
| 2 | **10000** |
| 3 | **3** |
| 4 | **2** |
| 5 | **41.2** |
| 6 | **Yes, it decreased** |
| 7 | **0.369** |

**Homework URL (repo folder):** https://github.com/zakard114/ZoomCamp/tree/main/ML/01/HW_01

---

## Setup

I ran [`[2026]_HW_01.ipynb`](./%5B2026%5D_HW_01.ipynb) in local Jupyter (nbclassic), same ML Zoomcamp `.venv` as Module 1 lessons.

- Kernel: Python (ml-zoomcamp) / `HW_01/.venv` → `ML/.venv`
- Data: `data/car_fuel_efficiency_2026.csv` (2026 pinned release; not committed — download from the course repo)

```text
https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/main/cohorts/2026/data/car_fuel_efficiency_2026.csv
```

---

## Q1 — Pandas version

**Question:** What version of Pandas did you install?

```python
pd.__version__
```

**Output:**

```text
3.0.5
```

**Answer:** **3.0.5**

---

## Q2 — Records count

**Question:** How many records are in the dataset?

- 5000
- 9000
- 10000
- 15000

```python
len(df)
# or df.shape[0]
```

**Output:**

```text
10000
```

**Answer:** **10000**

---

## Q3 — Fuel types

**Question:** How many fuel types are presented in the dataset?

- 1
- 2
- 3
- 4

```python
df["fuel_type"].nunique()
df["fuel_type"].unique()
```

**Output:**

```text
3
['Gasoline', 'Diesel', 'Hybrid']
```

**Answer:** **3**

---

## Q4 — Missing values

**Question:** How many columns in the dataset have missing values?

- 0
- 1
- 2
- 3
- 4

```python
(df.isnull().sum() > 0).sum()
```

**Output:**

```text
2
```

**Answer:** **2**

---

## Q5 — Max fuel efficiency (Asia)

**Question:** What's the maximum fuel efficiency of cars from Asia?

- 21.2
- 31.2
- 41.2
- 51.2

```python
df[df["origin"] == "Asia"]["fuel_efficiency_mpg"].max()
```

**Output:**

```text
41.2
```

**Answer:** **41.2**

---

## Q6 — Median value of horsepower

**Question:** After filling missing `horsepower` with the mode, did the median change?

- Yes, it increased
- Yes, it decreased
- No

```python
median_hp = df["horsepower"].median()
most_freq_hp = df["horsepower"].mode()[0]
df["horsepower"] = df["horsepower"].fillna(most_freq_hp)
new_median_hp = df["horsepower"].median()
print("Original median:", median_hp)
print("New median:", new_median_hp)
```

**Output:**

```text
Original median: 254.0
New median: 252.0
```

**Answer:** **Yes, it decreased**

---

## Q7 — Sum of weights

**Question:** Sum of all elements of `w` after the hand-rolled linear-regression steps.

- 0.0369
- 0.369
- 3.69
- 36.9

Asia only → `vehicle_weight`, `model_year` → first 7 rows → `X` → `XTX = X.T @ X` → invert →  
`y = [1100, 1300, 800, 900, 1000, 1100, 1200]` → `w = inv(XTX) @ X.T @ y` → `w.sum()`.

(See numbered cells `Q7-1` … `Q7-9` in the notebook.)

**Output:**

```text
w: [0.13644777 0.2327492 ]
sum of w: 0.36919696904925486
```

**Answer:** **0.369**

---

## Submission checklist

| Field | Value |
|-------|--------|
| Homework URL | https://github.com/zakard114/ZoomCamp/tree/main/ML/01/HW_01 |
| FAQ contribution | https://github.com/DataTalksClub/faq/issues/281 |
| Learning in public | optional |
| Time spent | optional |
