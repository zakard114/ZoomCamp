"""End-to-end workflow: load → transform → predict → simulate → benchmark."""

from __future__ import annotations

from dataclasses import dataclass, field

from .analysis import prediction_diagnostics
from .benchmark import compare_strategies
from .config import PRED_THRESHOLD, SECOND_THRESHOLD
from .exact_simulation import exact_iterrows_simulate
from .incremental import load_or_refresh_raw
from .modeling import (
    attach_all_strategy_columns,
    build_labeled_frame,
    fit_decision_tree,
    fit_random_forest,
    fit_xgboost,
)
from .simulation import latest_signals, vector_simulate
from .sp500_benchmark import strategy_beats_benchmark, spy_buy_hold_cagr
from .strategies_advanced import (
    attach_prob_scaled_notional_flags,
    attach_topk_per_day_strategy,
    vector_simulate_scaled,
)


@dataclass
class PipelineResult:
    data_path: str
    n_rows: int
    n_features: int
    pred_column: str
    simulation: dict
    latest_trades: object
    strategy_columns: list[str] = field(default_factory=list)
    comparison: dict = field(default_factory=dict)
    exact_simulation: dict = field(default_factory=dict)
    advanced_strategies: dict = field(default_factory=dict)
    diagnostics: dict = field(default_factory=dict)
    sp500_benchmark: dict = field(default_factory=dict)
    beats_spx_cagr: bool | None = None
    incremental_meta: dict = field(default_factory=dict)


def run_pipeline() -> PipelineResult:
    raw, inc_meta = load_or_refresh_raw()
    frame, features = build_labeled_frame(raw)
    _, proba_rf = fit_random_forest(frame, features)
    _, proba_dt = fit_decision_tree(frame, features)
    _, proba_xgb = fit_xgboost(frame, features)
    frame, strategy_cols = attach_all_strategy_columns(
        frame,
        proba_rf,
        proba_dt,
        (PRED_THRESHOLD, SECOND_THRESHOLD),
        proba_xgb=proba_xgb,
    )
    frame, top3_col = attach_topk_per_day_strategy(frame, "proba_rf", PRED_THRESHOLD, max_per_day=3)
    frame = attach_prob_scaled_notional_flags(frame, f"pred_rf_{PRED_THRESHOLD:.2f}", "proba_rf")
    if top3_col not in strategy_cols:
        strategy_cols = list(strategy_cols) + [top3_col]
    comparison = compare_strategies(frame, strategy_cols)
    pred_col = f"pred_rf_{PRED_THRESHOLD:.2f}"
    sim = vector_simulate(frame, pred_col)
    exact = exact_iterrows_simulate(frame, pred_col)
    advanced = {
        "top3_per_day": vector_simulate(frame, top3_col),
        "prob_scaled": vector_simulate_scaled(frame, pred_col),
    }
    diag = prediction_diagnostics(frame, pred_col)
    spy = spy_buy_hold_cagr(frame)
    best_cagr = max(
        (row.get("cagr_approx") or 0.0 for row in comparison.get("strategies", [])),
        default=sim.get("cagr_approx") or 0.0,
    )
    beats = strategy_beats_benchmark(best_cagr, spy.get("cagr_approx"))
    trades = latest_signals(frame, pred_col)
    return PipelineResult(
        data_path=str(inc_meta.get("path", "")),
        n_rows=len(frame),
        n_features=len(features),
        pred_column=pred_col,
        simulation=sim,
        latest_trades=trades,
        strategy_columns=strategy_cols,
        comparison=comparison,
        exact_simulation=exact,
        advanced_strategies=advanced,
        diagnostics=diag,
        sp500_benchmark=spy,
        beats_spx_cagr=beats,
        incremental_meta=inc_meta,
    )