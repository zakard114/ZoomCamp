# SMA Zoomcamp 2026 — Capstone (floor build)

## Problem

Build an **end-to-end algo-trading workflow**: load the course combined equity dataset, engineer lecture features, train a **RandomForest** to flag 30-day forward return opportunities, apply a **probability threshold rule**, and **vector-simulate** fixed $100 trades with **0.2% fees** on the held-out test period.

**Scope for attempt 1 (2026-11-20):** US large-cap panel from the course pipeline (Module 02 → Module 04). Korea/KRX or DART angles are documented as future upgrades in Module 5 homework, not required for the rubric floor.

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
- **DUMMIES:** `Month`, `Weekday`, `ticker_type` (Ticker / `month_wom` dropped for reduced model, as in HW4 Q1)
- **Simulation label:** `growth_future_30d` (not used as input)

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
# Optional: junction .venv → ..\..\ML\.venv (see zoomcamp-shared-venv skill)
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe run.py
```

Dependencies: `requirements.txt` (already in shared `ML/.venv` if you completed Module 4).

## Rubric floor (bold = 6 minimum)

| Area | Evidence in this repo |
|------|------------------------|
| README problem | This file |
| Lecture data sources | Table above + parquet from M02/M04 |
| One frame + feature sets | `features.py` |
| RandomForest / DecisionTree | `modeling.py` (RF) |
| Vector sim ≥1 strategy | `simulation.py` |
| `.py` modules + driver notebook/CLI | `src/*`, `run.py`, `project.ipynb` |

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

Latest test-day signals (sample): `HINDUNILVR.NS`, `RELIANCE.NS`, `SBIN.NS` on `2026-09-18` — `growth_future_30d` may be **NaN** at the dataset tail (no full 30d forward window).

## Reproduce

1. Place or build the combined parquet (Module 02).
2. `python run.py` — prints simulation stats + latest test-day tickers with signals.
3. Open `project.ipynb` and run all cells (same pipeline).

## Future upgrades (post-deadline)

- Second strategy (`sim2_*`, threshold 0.57), benchmark vs S&P, KRX tickers, incremental refresh/Cron — per official [project rubric](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/tree/main/projects/README.md).