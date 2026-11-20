#!/usr/bin/env python3
"""CLI entry: full capstone workflow on local combined parquet."""

import os
import sys

os.environ.setdefault("MPLCONFIGDIR", r"E:\IT_SPACES\AI\.cache\matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", r"E:\IT_SPACES\AI\.cache")
os.environ.setdefault("TEMP", r"E:\IT_SPACES\AI\.cache\tmp")
os.environ.setdefault("TMP", r"E:\IT_SPACES\AI\.cache\tmp")

from src.pipeline import run_pipeline


def main() -> int:
    result = run_pipeline()
    print("=== SMA Capstone pipeline ===")
    print(f"Data: {result.data_path}")
    print(f"Rows: {result.n_rows:,}  Features: {result.n_features}")
    print(f"Incremental cache hit: {result.incremental_meta.get('cache_hit')}")
    print(f"Primary strategy: {result.pred_column}")
    print("--- Simulation (primary vector) ---")
    for k, v in result.simulation.items():
        print(f"  {k}: {v}")
    print("--- Exact iterrows (primary) ---")
    for k, v in result.exact_simulation.items():
        print(f"  {k}: {v}")
    print("--- Advanced rules ---")
    for name, metrics in result.advanced_strategies.items():
        cagr = metrics.get("cagr_approx")
        trades = metrics.get("test_trades")
        print(f"  {name}: trades={trades} cagr={cagr}")
    print("--- SPX buy-and-hold (yfinance) ---")
    for k, v in result.sp500_benchmark.items():
        print(f"  {k}: {v}")
    print(f"  best_strategy_beats_spx_cagr: {result.beats_spx_cagr}")
    print("--- Strategy comparison (test) ---")
    for row in result.comparison.get("strategies", []):
        label = row.get("strategy", "?")
        cagr = row.get("cagr_approx")
        trades = row.get("test_trades")
        sharpe = row.get("sharpe_daily")
        print(f"  {label}: trades={trades} cagr={cagr} sharpe={sharpe}")
    passive = result.comparison.get("passive_baseline", {})
    print(f"  passive baseline: trades={passive.get('test_trades')} cagr={passive.get('cagr_approx')}")
    diag = result.diagnostics.get("overall_test", {})
    print(f"--- Diagnostics (test) precision={diag.get('precision')} recall={diag.get('recall')} ---")
    print("--- Latest test-day signals (primary) ---")
    if result.latest_trades is not None and len(result.latest_trades):
        print(result.latest_trades.to_string(index=False))
    else:
        print("  (no signals on last test date)")
    return 0


if __name__ == "__main__":
    sys.exit(main())