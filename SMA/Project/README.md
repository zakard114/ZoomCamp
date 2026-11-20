# SMA Zoomcamp 2026 — Capstone

**Product demo (Signal Desk):** Companion API/UI over frozen run artifacts. **This directory** is the graded ML pipeline and reproduction entry point.

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

## Derived features (rubric §2 — 20+ documented)

| Feature | Description |
|---------|-------------|
| `ln_volume` | log(volume) stability |
| `div_payout` | dividend event dummy |
| `stock_split` | split event dummy |
| `sma10_over_sma20` | short/long MA ratio |
| `rsi_x_vol` | RSI × volatility interaction |
| `yield_spread_10y_fed` | `DGS10 − FEDFUNDS` |
| `hl_rel_sq` | squared high–low range (custom) |
| `growth_vol_ratio` | past growth / volatility |
| `month_sin`, `month_cos` | calendar seasonality |
| `high_ln_volume` | above-median volume dummy |

Plus lecture TA, patterns, macro, and dummy sets in `FEATURE_SETS` → **216** model columns after dummies (see `run.py` output).

## Model & strategy

- **Models:** `RandomForestClassifier` (primary) + `DecisionTreeClassifier` + optional **XGBoost** (`fit_xgboost`)
- **Rules:** buy when `predict_proba >= threshold` → `pred_rf_0.55`, `pred_rf_0.57`, `pred_dt_0.55`, optional `pred_xgb_0.55`
- **Tuning:** optional `python -m src.tuning` (`RandomizedSearchCV` on train/valid)
- **Simulation:** vector sim + **exact `iterrows` reinvest** (`src/exact_simulation.py`); top-3/day and probability-scaled sizing (`src/strategies_advanced.py`); **CAGR**, **Sharpe**, **max drawdown**, rolling windows vs passive baseline and **^GSPC** (`src/benchmark.py`, `src/sp500_benchmark.py`)
- **Analysis:** `python run_analysis.py` → `docs/analysis_snapshot.json`; ticker/month precision (`src/analysis.py`)
- **EDA:** `python run_eda.py` → correlation chart in [`docs/figures/`](docs/figures/)

## Repository layout

```
SMA/Project/
  README.md
  requirements.txt
  run.py                 # CLI end-to-end
  run_eda.py             # EDA summary + figure
  project.ipynb          # same pipeline as run.py
  docs/                  # FINDINGS, AUTOMATION, figures/
  src/
    benchmark.py         # multi-strategy vs passive baseline
    exact_simulation.py  # iterrows reinvestment path
    strategies_advanced.py
    sp500_benchmark.py
    analysis.py
    incremental.py
    eda.py
    tuning.py
    download.py
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

## Verified run (local, 2026-11-19)

`ML\.venv\Scripts\python.exe run.py` on combined parquet (`stocks_df_combined_2026_09_18`):

| Metric | Value |
|--------|-------|
| Rows (after filters) | 202,292 |
| Features | 216 |
| Primary strategy | `pred_rf_0.55` |
| Test trades (primary) | 6,092 |
| Q75 trades / day | 11 |
| Assumed capital (USD) | 33,000 |
| Net P&L (USD) | ~19,183.6 |
| CAGR (approx., 4y) | ~1.121 |
| Sharpe (daily P&L, test) | ~5.71 |

Also compare `pred_rf_0.57`, `pred_dt_0.55`, and passive baseline via `run.py` (see `src/benchmark.py`).

Latest test-day signals (sample): `RELIANCE.NS`, `SBIN.NS` on `2026-09-18`. At the dataset tail, `growth_future_30d` can be **NaN** when the 30-day forward window is not yet observable.

## Reproduce

1. Place or build the combined parquet (Module 02).
2. Run `run.py` — primary simulation, **multi-strategy comparison**, latest signals.
3. `python run_eda.py` — EDA summary + figure.
4. `python -m src.download --regime refresh` — rebuild instructions (second automation regime).
5. Open `project.ipynb` and run all cells (same pipeline).

## Documentation

| Doc | Rubric |
|-----|--------|
| [`docs/FINDINGS.md`](docs/FINDINGS.md) | Problem steps, difficulties, reproduction |
| [`docs/AUTOMATION.md`](docs/AUTOMATION.md) | Cron, two data regimes, export to Signal Desk |

**Live portfolio demo:** https://signal-desk-c3dx.onrender.com · Capstone repo path: [`SMA/Project`](https://github.com/zakard114/ZoomCamp/tree/main/SMA/Project).

Course rubric: [official `projects/README.md`](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/projects/README.md).