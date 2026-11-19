# Findings and reproduction notes

## Problem scope

Lecture-aligned **global equity panel** with a **probability-rule** long-only strategy on 30-day forward returns. Extended deliverable: **multi-threshold** (`pred_rf_0.55`, `pred_rf_0.57`) and **second lecture model** (`DecisionTree` → `pred_dt_0.55`) with shared vector simulator.

## Reproduce verified numbers

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\SMA\Project
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe run.py
```

Expect primary `pred_rf_0.55` simulation stats to match [README verified run](../README.md#verified-run-local-2026-11-18) when parquet is unchanged.

## EDA (rubric §3)

```powershell
python run_eda.py
```

Outputs JSON summary (stdout) and `docs/figures/eda_top_correlations.png`.

## Modeling

- **RF** — homework defaults (`n_estimators=100`, `max_depth=13`).
- **DT** — `max_depth=12` for a second lecture baseline.
- **Tuning** — `python -m src.tuning` (small `RandomizedSearchCV` on train/valid; optional before production runs).

## Simulation vs baseline

`run.py` prints **strategy comparison**: RF thresholds, DT rule, and **passive baseline** (trade every test row at $100). Includes approximate **CAGR**, **Sharpe** (daily P&L series), **max drawdown**.

## Difficulties

- Combined parquet is **local on E:** — peers must use their own path or `SMA_DATA_PATH`.
- Forward labels at dataset tail can be **NaN** when the 30-day window is not observable.
- Vector sim is **lecture-fast**; exact `iterrows` reinvestment is listed as a future extension in `_planning/BACKLOG.md`.

## Live portfolio layer

[signal-desk](https://github.com/zakard114/signal-desk) serves `artifacts/latest.json` — does not re-train on Render.