#!/usr/bin/env python3
"""CLI: diagnostics + SPX benchmark + exact sim snapshot (rubric §5 deep analysis)."""

import json
import os
import sys

os.environ.setdefault("MPLCONFIGDIR", r"E:\IT_SPACES\AI\.cache\matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", r"E:\IT_SPACES\AI\.cache")

from src.analysis import prediction_diagnostics
from src.config import PRED_THRESHOLD
from src.exact_simulation import exact_iterrows_simulate
from src.incremental import load_or_refresh_raw
from src.modeling import attach_all_strategy_columns, build_labeled_frame, fit_decision_tree, fit_random_forest, fit_xgboost
from src.sp500_benchmark import strategy_beats_benchmark, spy_buy_hold_cagr
from src.simulation import vector_simulate


def main() -> int:
    raw, cache_meta = load_or_refresh_raw()
    frame, features = build_labeled_frame(raw)
    _, proba_rf = fit_random_forest(frame, features)
    _, proba_dt = fit_decision_tree(frame, features)
    _, proba_xgb = fit_xgboost(frame, features)
    frame, strategy_cols = attach_all_strategy_columns(
        frame, proba_rf, proba_dt, (PRED_THRESHOLD, 0.57), proba_xgb=proba_xgb
    )
    pred_col = f"pred_rf_{PRED_THRESHOLD:.2f}"
    vec = vector_simulate(frame, pred_col)
    exact = exact_iterrows_simulate(frame, pred_col)
    diag = prediction_diagnostics(frame, pred_col)
    spy = spy_buy_hold_cagr(frame)
    beats = strategy_beats_benchmark(vec.get("cagr_approx"), spy.get("cagr_approx"))
    payload = {
        "cache_meta": cache_meta,
        "vector_primary": vec,
        "exact_primary": exact,
        "diagnostics": diag,
        "sp500_benchmark": spy,
        "primary_beats_spx_cagr": beats,
        "strategy_columns": strategy_cols,
    }
    out_path = os.path.join("docs", "analysis_snapshot.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    print(json.dumps({"written": out_path, "beats_spx": beats, "exact_trades": exact["test_trades"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())