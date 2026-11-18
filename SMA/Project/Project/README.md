# SMA Zoomcamp 2026 — Capstone

## Problem

End-to-end **algo-trading workflow**: load the course combined equity dataset, engineer lecture features, train a **RandomForest** for 30-day forward return opportunities, apply a **probability threshold** rule, and **vector-simulate** fixed $100 trades with **0.2% fees** on the held-out test period.

**Data scope:** Combined panel from course Modules 02–04 (prices, technical features, US macro, forward-return labels).

## Data sources (lecture)

| Source | Role |
|--------|------|
| **YFinance** | Prices, volume, corporate actions (via Module 02 build) |
| **TA-Lib-style columns** | Technical indicators & candle patterns in combined parquet |
| **FRED** | `FEDFUNDS`, yield curve (`DGS*`), CPI / GDP potential fields |

**Local file (not on GitHub):**

`E:/IT_SPACES/AI/ZoomCamp/SMA/04/trading_strategy_and_simulation/stocks_df_combined_2026_09_18.parquet.brotli`

Override with `SMA_DATA_PATH` if needed.

## Feature sets

Defined in `src/features.py` (`FEATURE_SETS`):

- **TO_PREDICT:** `is_positive_growth_30d_future` (growth cutoff = 1.0)
- **NUMERIC:** past growth, TA, patterns, custom (`ln_volume`, splits, etc.), macro
- **DUMMIES:** `Month`, `Weekday`, `ticker_type` (Ticker / `month_wom` dropped for reduced model, as in Module 4 homework)
- **Simulation label:** `growth_future_30d` (not used as a model input)

## Model & strategy

- **Model:** `RandomForestClassifier` (`n_estimators=100`, `max_depth=13`, `random_state=42`)
- **Rule:** buy signal when `predict_proba >= 0.55` → column `pred_rf_0.55`
- **Simulation:** vector sim on `split == "test"` only; capital assumption `100 × 30 × Q75(daily trades)`; approximate **CAGR** over 4 years (Module 4 formula)

## Repository layout

```
SMA/Project/
  README.md
  requirements.txt
  run.py                 # CLI end-to-end
  project.ipynb          # calls the same functions as run.py
  src/
    download.py          # locate local combined parquet
    load_data.py
    features.py
    modeling.py
    simulation.py
    pipeline.py
```

## Setup (shared ZoomCamp venv on E:)

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\SMA\Project
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe run.py
```

Dependencies: `requirements.txt` (shared `ML/.venv` if you completed earlier modules).

## Verified run (local, 2026-11-18)

`ML\.venv\Scripts\python.exe run.py` on combined parquet (`stocks_df_combined_2026_09_18`):

| Metric | Value |
|--------|-------|
| Rows (after filters) | 202,292 |
| Features | 208 |
| Strategy | `pred_rf_0.55` |
| Test trades | 3,756 |
| Avg trades / day (test) | ~6.06 |
| Q75 trades / day | 7 |
| Assumed capital (USD) | 21,000 |
| Net P&L (USD) | ~12,983.6 |
| CAGR (approx., 4y) | ~1.128 |

Latest test-day signals (sample): `HINDUNILVR.NS`, `RELIANCE.NS`, `SBIN.NS` on `2026-09-18`. At the dataset tail, `growth_future_30d` can be **NaN** when the 30-day forward window is not yet observable.

## Reproduce

1. Place or build the combined parquet (Module 02).
2. Run `run.py` — prints simulation stats and latest test-day tickers with signals.
3. Open `project.ipynb` and run all cells (same pipeline).

## Course project rubric

Evaluation criteria and optional extensions: [course `projects/README.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/tree/main/projects/README.md).