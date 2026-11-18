"""End-to-end workflow: load → transform → predict → simulate → latest trades."""

from __future__ import annotations

from dataclasses import dataclass

from .config import PRED_THRESHOLD
from .load_data import load_combined_parquet, resolve_data_path
from .modeling import attach_predictions, build_labeled_frame, fit_random_forest
from .simulation import latest_signals, vector_simulate


@dataclass
class PipelineResult:
    data_path: str
    n_rows: int
    n_features: int
    pred_column: str
    simulation: dict
    latest_trades: object  # pd.DataFrame


def run_pipeline() -> PipelineResult:
    path = resolve_data_path()
    raw = load_combined_parquet(path)
    frame, features = build_labeled_frame(raw)
    _, proba = fit_random_forest(frame, features)
    frame, pred_col = attach_predictions(frame, proba, PRED_THRESHOLD)
    sim = vector_simulate(frame, pred_col)
    trades = latest_signals(frame, pred_col)
    return PipelineResult(
        data_path=str(path),
        n_rows=len(frame),
        n_features=len(features),
        pred_column=pred_col,
        simulation=sim,
        latest_trades=trades,
    )