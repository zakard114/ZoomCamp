"""Vectorized trading simulation (Module 04: $100 per signal, 0.2% fee)."""

import numpy as np
import pandas as pd

from .config import FEE_RATE, SIM_YEARS, TRADE_NOTIONAL


def vector_simulate(frame: pd.DataFrame, pred_col: str) -> dict:
    test_pos = (frame.split == "test") & (frame[pred_col] == 1)
    count = int(test_pos.sum())
    gross = (
        frame.loc[test_pos, pred_col] * TRADE_NOTIONAL * (frame.loc[test_pos, "growth_future_30d"] - 1)
    ).sum()
    fees = (-frame.loc[test_pos, pred_col] * TRADE_NOTIONAL * FEE_RATE).sum()
    net = float(gross + fees)
    daily = frame.loc[test_pos].groupby("Date")[pred_col].count()
    avg = float(daily.mean()) if count else None
    q75 = float(daily.quantile(0.75)) if count else None
    capital = TRADE_NOTIONAL * 30 * q75 if q75 else None
    cagr = None
    if capital and capital > 0:
        cagr = float(((capital + net) / capital) ** (1 / SIM_YEARS))
    return {
        "pred_column": pred_col,
        "test_trades": count,
        "avg_trades_per_day": avg,
        "q75_trades_per_day": q75,
        "assumed_capital_usd": capital,
        "net_pnl_usd": net,
        "cagr_approx": cagr,
    }


def latest_signals(
    frame: pd.DataFrame, pred_col: str, split: str = "test", top_n: int = 20
) -> pd.DataFrame:
    mask = (frame.split == split) & (frame[pred_col] == 1)
    sig = frame.loc[mask, ["Date", "Ticker", "ticker_type", pred_col, "growth_future_30d"]].copy()
    if sig.empty:
        return sig
    last = sig["Date"].max()
    return sig[sig["Date"] == last].sort_values("Ticker").head(top_n)