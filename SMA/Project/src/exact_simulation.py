"""Row-wise simulation with cash reinvestment (course rubric: exact / iterrows)."""

from __future__ import annotations

import pandas as pd

from .config import FEE_RATE, SIM_YEARS, TRADE_NOTIONAL


def exact_iterrows_simulate(
    frame: pd.DataFrame,
    pred_col: str,
    *,
    starting_cash_usd: float = 10_000.0,
) -> dict:
    """Walk test rows in time order; reinvest available cash each signal (capped at lecture notional)."""
    mask = (frame.split == "test") & (frame[pred_col] == 1)
    rows = frame.loc[mask, ["Date", "growth_future_30d"]].copy()
    rows = rows.dropna(subset=["growth_future_30d"]).sort_values("Date")
    cash = float(starting_cash_usd)
    trades = 0
  # iterrows: rubric “exact” path (slower than vector sim, same economic story)
    for _, row in rows.iterrows():
        if cash < 1.0:
            break
        stake = min(TRADE_NOTIONAL, cash)
        gross = stake * (float(row.growth_future_30d) - 1.0)
        fee = stake * FEE_RATE
        cash += gross - fee
        trades += 1
    net = cash - starting_cash_usd
    cagr = None
    if starting_cash_usd > 0 and cash > 0:
        cagr = float((cash / starting_cash_usd) ** (1 / SIM_YEARS))
    return {
        "label": "exact_iterrows_reinvest",
        "pred_column": pred_col,
        "starting_cash_usd": starting_cash_usd,
        "ending_cash_usd": float(cash),
        "test_trades": trades,
        "net_pnl_usd": float(net),
        "cagr_approx": cagr,
    }