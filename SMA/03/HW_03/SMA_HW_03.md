# SMA Zoomcamp 2026 — Homework 3: Time Series Modeling

Q1–Q4 calculations: [[2026]_Module_03_Homework.ipynb](https://github.com/zakard114/ZoomCamp/blob/main/SMA/03/HW_03/%5B2026%5D_Module_03_Homework.ipynb)

---

## Form answers

| # | Choice |
|---|--------|
| 1 | **0.025** |
| 2 | **0.588** |
| 3 | **1243** |
| 4 | **4** |
| 5 | see Q5 below |

---

## Setup

- Kernel: SMA / `HW_03/.venv` → `SMA/.venv` → `ML/.venv`
- Official text: `materials/homework3.md` (do not edit)
- Launch: `bash run-nbclassic.sh` — do not use `jupyter notebook`
- Frame: `../modeling/stocks_df_combined_2026_09_18.parquet.brotli` on E: (2000-01-03 to 2026-09-18, 202,292 rows)

The lesson OHLCV list names `Close` and `Adj Close_x`. This file has `Close_x`. The model uses growth, technicals, macros, and dummies, so I left the price column as it is.

---

## Q1 — Dummies for Month and Week-of-Month

**Question:** Absolute correlation of the strongest month-and-week dummy with `is_positive_growth_30d_future`, to three decimals.

`Month` is a month-start timestamp, so `October_w4` has to be built from `Date`. `get_dummies` prefixes the column: `month_wom_October_w4`. **115** dummies, **60** of them `month_wom`.

**Answer:** **0.025**. Raw absolute correlation **0.024584**. The form options are 0.015, 0.025, 0.035, 0.045.

---

## Q2 — New hand rules (pred3 / pred4) precision

**Question:** Precision of the better new rule, to three decimals.

`pred3` (`DGS10 <= 4.5` and `DGS5 <= 4`) is **0.587744** on the test set (15,910 positive calls). `pred4` (`DGS10 > 4` and `FEDFUNDS <= 4.795`) is **0.502544** (15,921 positive calls).

**Answer:** **0.588**. The form options are 0.558, 0.568, 0.578, 0.588, 0.598.

---

## Q3 — Unique correct predictions (`pred5_clf_10`)

**Question:** Test rows where the depth-10 tree is right and pred0–pred4 are all wrong.

`random_state=42`, fit on train+validation (**169,129** rows, no missing labels). The lesson join looks up prediction columns that are not on the frame yet, so I wrote the prediction vector onto the same rows.

**Answer:** **1243**.

---

## Q4 — Optimal Decision Tree depth (1–12)

**Question:** Depth with the highest precision on the test set.

Depth 1 calls every test row positive (precision 0.570). Depth 4 is the high point, and it stays above 0.58.

**Answer:** **4**. Test precision **0.629175**.

---

## Q5 — What data is missing?

The depth-10 tree leans on US core CPI, one-year gold and oil growth, and the funds rate. I would add the CPI surprise (actual minus consensus), because the file already has the CPI change and not whether the print was a surprise. A public source is the Cleveland Fed inflation nowcast.
