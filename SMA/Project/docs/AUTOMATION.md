# Automation (course rubric §6)

## End-to-end entry points

| Command | Purpose |
|---------|---------|
| `python run.py` | Load parquet → features → RF + DT (+ XGB) → vector + exact sim → SPX benchmark → strategy comparison |
| `python run_analysis.py` | Diagnostics JSON + exact sim snapshot (`docs/analysis_snapshot.json`) |
| `python run_eda.py` | Target rates, top correlations, `docs/figures/eda_top_correlations.png` |
| `python -m src.tuning` | RandomForest `RandomizedSearchCV` on train/valid slice |
| `python -m src.download --regime file` | Resolve local combined parquet (`SMA_DATA_PATH` or default on E:) |
| `python -m src.download --regime refresh` | Print steps to rebuild data from Module 02 |

`project.ipynb` calls the same `run_pipeline()` as `run.py`.

## Two data regimes

1. **File regime (default)** — use the committed-on-disk Module 02 combined parquet (not in Git). Fast, reproducible for grading.
2. **Refresh regime** — re-run Module 02 export, set `SMA_DATA_PATH`, then `run.py`.

**Incremental cache** — `src/incremental.py` stores parquet fingerprints under `E:\IT_SPACES\AI\.cache\sma-capstone\incremental` (override with `SMA_INCREMENTAL_CACHE`). Used by `run_pipeline()` before transforms.

## Dependencies

`requirements.txt` + shared ZoomCamp venv on `E:` (see README Setup).

## Scheduled run (cron / Task Scheduler)

Daily predictions (after you refresh parquet overnight):

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
cd E:\IT_SPACES\AI\ZoomCamp\SMA\Project
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe run.py >> E:\IT_SPACES\AI\.cache\logs\sma-capstone-run.log 2>&1
```

Windows Task Scheduler: trigger daily, action = above PowerShell one-liner.

## Portfolio artifact export

Signal Desk frozen JSON:

```powershell
cd E:\IT_SPACES\AI\Projects\sma\us-equity-signals
E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe ops\export_artifacts.py
```

Commit `artifacts/latest.json` and redeploy Render when cloud numbers should change.