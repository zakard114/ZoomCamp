"""Paths and defaults for the capstone pipeline (E: drive, no data on GitHub)."""

from pathlib import Path
import os

# Project root: .../ZoomCamp/SMA/Project
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SMA_ROOT = PROJECT_ROOT.parent

_DEFAULT_PARQUET = (
    SMA_ROOT
    / "04"
    / "trading_strategy_and_simulation"
    / "stocks_df_combined_2026_09_18.parquet.brotli"
)

# Override with SMA_DATA_PATH if your parquet lives elsewhere on E:
DATA_PATH = Path(os.environ.get("SMA_DATA_PATH", str(_DEFAULT_PARQUET)))

TRAIN_PROP = 0.7
VAL_PROP = 0.15
MIN_HISTORY_DATE = "2000-01-01"

# Module 4 homework-aligned defaults (reduced dummies + RF + 0.55 rule)
DROP_TICKER_AND_MONTH_WOM = True
GROWTH_CUTOFF = 1.0
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 13
RF_RANDOM_STATE = 42
PRED_THRESHOLD = 0.55
SECOND_THRESHOLD = 0.57
DT_MAX_DEPTH = 12
DT_RANDOM_STATE = 42
TRADE_NOTIONAL = 100.0
FEE_RATE = 0.002
SIM_YEARS = 4