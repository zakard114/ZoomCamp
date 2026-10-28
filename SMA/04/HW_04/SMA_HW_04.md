# SMA Zoomcamp 2026 — Homework 4: Trading System

Q1–Q3 calculations: [[2026]_Module_04_Homework.ipynb](%5B2026%5D_Module_04_Homework.ipynb)

---

## Form answers

| # | Choice |
|---|--------|
| 1 | **1.126** |
| 2 | **0.57** |
| 3 | **7337** |
| 4 | see Q4 below |

---

## Setup

- Kernel: SMA / `HW_04/.venv` → `SMA/.venv` → `ML/.venv`
- Official text: `materials/homework4.md` (do not edit)
- Launch: `bash run-nbclassic.sh` — do not use `jupyter notebook`
- Frame: `../trading_strategy_and_simulation/stocks_df_combined_2026_09_18.parquet.brotli` on E:
- Random forest: `n_estimators=100`, `max_depth=13`, `random_state=42`
- Capital and CAGR follow the lesson: `100 * 30 *` the 75% daily trade count, then four-year CAGR

The lesson builds `Month` with `format='%m'`. In this file `Month` is already a month-start timestamp, so I formatted it with `.dt.strftime('%B')`. The homework says `ticker`. The column is `Ticker`.

---

## Q1 — Fewer dummies, `pred10_rf_best_rule_55` CAGR

**Question:** CAGR for the random forest rule at probability 0.55 after dropping `Ticker` and `month_wom` before `get_dummies`.

`df_with_dummies[NUMERICAL+DUMMIES]` has **208** features. The full dummy set has **301**. The 0.55 rule on the test set makes **3,756** trades, **6.06** per day on average. CAGR is **1.127879**. The lesson's original CAGR was 1.1195.

**Answer:** **1.126**. Raw CAGR **1.127879**. Rounded to three decimals it is 1.128. The form options are 1.121, 1.126, 1.136, 1.141. 1.128 is not a choice. The nearest is 1.126.

---

## Q2 — Random forest threshold with fewer than 5 trades a day

**Question:** Probability threshold of the second-best random forest rule, among thresholds that average fewer than 5 trades per day.

Same reduced-dummy forest as Q1. Threshold 0.55 averages 6.06 trades a day. Threshold 0.56 averages 5.35. Threshold **0.57** averages **4.85** and has the highest CAGR in that group, **1.091977**. Threshold 0.58 averages 4.49 and the CAGR falls to 1.067.

**Answer:** **0.57**. The form options are 0.54, 0.56, 0.57, 0.58.

---

## Q3 — Growth target above 1.022, trades for `pred5_clf_10`

**Question:** Number of test trades for the depth-10 tree after the positive label becomes `growth_future_30d > 1.022`.

This run uses the full dummy set again, not the reduced set from Q1. The positive rate falls from about 0.59 to **0.491**. The depth-10 tree, `max_depth=10`, `random_state=42`, fit on train+validation, flags **7,337** test rows.

**Answer:** **7337**.

---

## Q4 — Ideal strategy

I would keep the reduced-dummy random forest and trade only when its probability is at least 0.57. That was the highest CAGR among the rules that stay under 5 trades a day. I would still put $100 on each signal, and I would stop adding trades once the day reaches the 75% count the capital formula already uses, about 6 names. I would not use a 0.65 cutoff. It barely trades, so the CAGR is not something I would trust out of sample. Fees stay 0.2% for the round trip.
