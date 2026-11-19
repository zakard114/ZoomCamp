"""End-to-end workflow: load → transform → predict → simulate → benchmark."""

from __future__ import annotations

from dataclasses import dataclass, field

from .benchmark import compare_strategies
from .config import PRED_THRESHOLD, SECOND_THRESHOLD
from .load_data import load_combined_parquet, resolve_data_path
from .modeling import (
    attach_all_strategy_columns,
    build_labeled_frame,
    fit_decision_tree,
    fit_random_forest,
)
from .simulation import latest_signals, vector_simulate


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


def run_pipeline() -> PipelineResult:
    path = resolve_data_path()
    raw = load_combined_parquet(path)
    frame, features = build_labeled_frame(raw)
    _, proba_rf = fit_random_forest(frame, features)
    _, proba_dt = fit_decision_tree(frame, features)
    frame, strategy_cols = attach_all_strategy_columns(
        frame, proba_rf, proba_dt, (PRED_THRESHOLD, SECOND_THRESHOLD)
    )
    comparison = compare_strategies(frame, strategy_cols)
    pred_col = f"pred_rf_{PRED_THRESHOLD:.2f}"
    sim = vector_simulate(frame, pred_col)
    trades = latest_signals(frame, pred_col)
    return PipelineResult(
        data_path=str(path),
        n_rows=len(frame),
        n_features=len(features),
        pred_column=pred_col,
        simulation=sim,
        latest_trades=trades,
        strategy_columns=strategy_cols,
        comparison=comparison,
    )