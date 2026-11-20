# Findings and reproduction notes

## Problem scope

Lecture-aligned **global equity panel** with a **probability-rule** long-only strategy on 30-day forward returns. Extended deliverable: **multi-threshold** RF rules, **DecisionTree** baseline, optional **XGBoost**, **vector + exact iterrows** simulators, **SPX benchmark** (yfinance), and **ticker/month diagnostics**.

## Reproduce verified numbers

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\SMA\Project
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe run.py
```

Expect primary `pred_rf_0.55` simulation stats to match [README verified run](../README.md#verified-run-local-2026-11-19) when parquet is unchanged.

Deep analysis artifact:

```powershell
python run_analysis.py
```

Writes `docs/analysis_snapshot.json` (exact sim, SPX CAGR, precision slices).

## EDA (rubric §3)

```powershell
python run_eda.py
```

Outputs JSON summary (stdout) and `docs/figures/eda_top_correlations.png`.

## Modeling

- **RF** — homework defaults (`n_estimators=100`, `max_depth=13`).
- **DT** — `max_depth=12` for a second lecture baseline.
- **XGBoost** — `src/modeling.py::fit_xgboost` when `xgboost` is installed.
- **Tuning** — `python -m src.tuning` (`RandomizedSearchCV` on train/valid).

Probability columns `proba_rf` / `proba_dt` are stored on the labeled frame for advanced rules.

## Simulation vs benchmarks

| Layer | Module | Rubric |
|-------|--------|--------|
| Vector (fast) | `src/simulation.py` | Multi-strategy compare in `run.py` |
| Exact reinvest | `src/exact_simulation.py` | `iterrows` cash walk |
| Top-3 / prob scaling | `src/strategies_advanced.py` | Concurrent cap + risk sizing |
| Metrics | `src/benchmark.py` | CAGR, Sharpe, max DD, rolling windows |
| SPX buy-and-hold | `src/sp500_benchmark.py` | `^GSPC` over test window |

`run.py` prints strategy comparison, exact sim, advanced rules, SPX benchmark, and whether primary CAGR exceeds SPX.

## Analysis (rubric §5 debug)

`src/analysis.py` — precision/recall on test by **Ticker** and **Month**, sample false-positive rows, improvement ideas. Invoked from `run_pipeline()` and `run_analysis.py`.

## Automation / incremental

- **Two regimes:** `python -m src.download --regime file|refresh` (see `docs/AUTOMATION.md`).
- **Incremental fingerprint:** `src/incremental.py` caches parquet metadata under `E:\IT_SPACES\AI\.cache\sma-capstone\incremental` (not in Git).

## Difficulties

- Combined parquet is **local on E:** — peers must use their own path or `SMA_DATA_PATH`.
- Forward labels at dataset tail can be **NaN** when the 30-day window is not observable.
- SPX benchmark requires network + `yfinance` on first fetch.
- Dataset is **~200k rows** after lecture filters — not a 1M-row novelty source (see rubric honesty in README).

## Live portfolio layer

[signal-desk](https://github.com/zakard114/signal-desk) serves `artifacts/latest.json` — does not re-train on Render. Ops **Inspector** can set the desk decision threshold and slider min/max (HoldRisk-style panel).