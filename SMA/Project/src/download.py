"""Data source step: local parquet on E: (file regime) or refresh from Module 02."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import DATA_PATH, SMA_ROOT
from .load_data import resolve_data_path


def ensure_local_dataset(path: str | Path | None = None) -> str:
    resolved = resolve_data_path(path or DATA_PATH)
    return str(resolved)


def print_refresh_instructions() -> None:
    module02 = SMA_ROOT / "02" / "building_the_dataset"
    print("=== Refresh regime (download / rebuild) ===")
    print(f"1. Open Module 02 notebooks under: {module02}")
    print("2. Re-export `stocks_df_combined_* .parquet.brotli` to E: (see lecture).")
    print("3. Point `SMA_DATA_PATH` at the new file or replace the default path in config.")
    print("4. Re-run `python run.py` or `python -m src.tuning`.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SMA capstone data regimes")
    parser.add_argument(
        "--regime",
        choices=("file", "refresh"),
        default="file",
        help="file = use existing parquet; refresh = print rebuild steps",
    )
    parser.add_argument("--path", default=None, help="Override parquet path")
    args = parser.parse_args(argv)
    if args.regime == "refresh":
        print_refresh_instructions()
        return 0
    path = ensure_local_dataset(args.path)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())