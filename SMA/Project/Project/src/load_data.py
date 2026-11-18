"""Load the combined lecture parquet (built in Module 02, reused in Module 04)."""

from pathlib import Path

import pandas as pd

from .config import DATA_PATH


def resolve_data_path(path: Path | None = None) -> Path:
    p = path or DATA_PATH
    if not p.is_file():
        raise FileNotFoundError(
            f"Combined dataset not found: {p}\n"
            "Build it with Module 02 (stocks_df_combined_*.parquet.brotli) "
            "or set env SMA_DATA_PATH to your copy on E:."
        )
    return p


def load_combined_parquet(path: Path | None = None) -> pd.DataFrame:
  # pd.read_parquet: single table with prices, TA columns, macro, and future growth
    p = resolve_data_path(path)
    return pd.read_parquet(p)