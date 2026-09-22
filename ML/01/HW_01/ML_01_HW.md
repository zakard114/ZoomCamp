# ML Zoomcamp 2026 — Homework 1: Introduction to Machine Learning

Submission write-up. Working notebook: `[2026]_HW_01.ipynb` (same folder).

**Official:** [`materials/homework.md`](materials/homework.md)  
**Submit:** https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw01

---

## Form answers

| # | Choice |
|---|--------|
| 1 | `3.0.5` (pandas `__version__`) |
| 2 | 10000 |
| 3 | 3 |
| 4 | 2 |
| 5 | 41.2 |
| 6 | Yes, it decreased |
| 7 | 0.369 |

---

## Setup

- Kernel: ML Zoomcamp / `HW_01/.venv` → `ML/.venv`
- Data: `data/car_fuel_efficiency_2026.csv` (2026 pinned release; not committed — download from course repo)

---

## Q1 — Pandas version

**Answer:** `3.0.5`

---

## Q2 — Records count

**Answer:** `10000`

---

## Q3 — Fuel types

**Answer:** `3` (Gasoline, Diesel, Hybrid)

---

## Q4 — Missing values

**Answer:** `2` columns have missing values

---

## Q5 — Max fuel efficiency (Asia)

**Answer:** `41.2`

---

## Q6 — Median horsepower

Original median: `254.0` → after mode fillna → new median: `252.0`  
**Answer:** Yes, it decreased

---

## Q7 — Sum of weights

`w ≈ [0.13644777, 0.2327492]`, `sum(w) ≈ 0.36919697`  
**Answer:** `0.369`

FAQ contribution (optional): https://github.com/DataTalksClub/faq/issues/281
