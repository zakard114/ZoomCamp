"""Empirical rules on top of model probabilities (rubric §5 advanced / new strategy)."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import FEE_RATE, SIM_YEARS, TRADE_NOTIONAL
from .simulation import vector_simulate


def attach_topk_per_day_strategy(
    frame: pd.DataFrame,
    proba_col: str,
    threshold: float,
    *,
    max_per_day: int = 3,
    prefix: str = "pred_rf_top3",
) -> tuple[pd.DataFrame, str]:
    """Long-only: at most `max_per_day` names per session with proba >= threshold (highest proba first)."""
    out = frame.copy()
    col = f"{prefix}_{threshold:.2f}"
    out[col] = 0
    test = out.split == "test"
    candidates = test & (out[proba_col] >= threshold)
    if not candidates.any():
        return out, col
    day_rank = out.loc[candidates, ["Date", proba_col]].copy()
    day_rank["_rank"] = day_rank.groupby("Date")[proba_col].rank(method="first", ascending=False)
    idx = day_rank.index[day_rank["_rank"] <= max_per_day]
    out.loc[idx, col] = 1
    return out, col


def attach_prob_scaled_notional_flags(
    frame: pd.DataFrame,
    pred_col: str,
    proba_col: str,
    *,
    min_scale: float = 0.5,
    max_scale: float = 2.0,
) -> pd.DataFrame:
    """Risk sizing: scale fixed trade size by clipped model probability on active signals."""
    out = frame.copy()
    scale = np.clip(out[proba_col].astype(float), 0.0, 1.0)
    scale = min_scale + (max_scale - min_scale) * scale
    out["_trade_scale"] = np.where(out[pred_col] == 1, scale, 0.0)
    return out


def vector_simulate_scaled(
    frame: pd.DataFrame,
    pred_col: str,
    scale_col: str = "_trade_scale",
) -> dict:
    """Vector sim where each row stake = TRADE_NOTIONAL * scale_col (default 0 off-signal)."""
    test_pos = (frame.split == "test") & (frame[pred_col] == 1)
    if not test_pos.any():
        base = vector_simulate(frame, pred_col)
        base["label"] = "prob_scaled_vector"
        return base
    stake = TRADE_NOTIONAL * frame.loc[test_pos, scale_col].clip(lower=0.0)
    gross = (stake * (frame.loc[test_pos, "growth_future_30d"] - 1.0)).sum()
    fees = (-stake * FEE_RATE).sum()
    net = float(gross + fees)
    count = int(test_pos.sum())
    daily = frame.loc[test_pos].groupby("Date")[pred_col].count()
    q75 = float(daily.quantile(0.75)) if count else None
    capital = TRADE_NOTIONAL * 30 * q75 if q75 else None
    cagr = None
    if capital and capital > 0:
        cagr = float(((capital + net) / capital) ** (1 / SIM_YEARS))
    return {
        "label": "prob_scaled_vector",
        "pred_column": pred_col,
        "test_trades": count,
        "net_pnl_usd": net,
        "assumed_capital_usd": capital,
        "cagr_approx": cagr,
    }