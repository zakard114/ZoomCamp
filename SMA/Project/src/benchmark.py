"""Benchmark metrics: passive test-period baseline, Sharpe, max drawdown."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import FEE_RATE, SIM_YEARS, TRADE_NOTIONAL
from .simulation import vector_simulate


def daily_trade_pnl(frame: pd.DataFrame, pred_col: str) -> pd.Series:
    test_pos = (frame.split == "test") & (frame[pred_col] == 1)
    if not test_pos.any():
        return pd.Series(dtype=float)
    rows = frame.loc[test_pos, ["Date", "growth_future_30d"]].copy()
    rows["pnl"] = TRADE_NOTIONAL * (rows["growth_future_30d"] - 1 - FEE_RATE)
    return rows.groupby("Date")["pnl"].sum().sort_index()


def rolling_annualized_returns(daily: pd.Series, window_days: int = 63) -> dict:
    """Approximate rolling CAGR windows on cumulative daily P&L (rubric metrics)."""
    if daily.empty:
        return {"rolling_windows": 0, "rolling_mean_cagr": None}
    cum = daily.cumsum()
    roll = cum.rolling(window_days, min_periods=max(10, window_days // 3)).apply(
        lambda x: float(x.iloc[-1] - x.iloc[0]) if len(x) else np.nan,
        raw=False,
    )
    roll = roll.dropna()
    if roll.empty:
        return {"rolling_windows": 0, "rolling_mean_cagr": None}
    scale = 252 / window_days
    annualized = roll / TRADE_NOTIONAL * scale
    return {
        "rolling_windows": int(len(roll)),
        "rolling_mean_annualized_return": float(annualized.mean()),
        "rolling_min_annualized_return": float(annualized.min()),
        "rolling_max_annualized_return": float(annualized.max()),
    }


def sharpe_and_drawdown(daily: pd.Series) -> dict:
    if daily.empty or len(daily) < 2:
        return {"sharpe_daily": None, "max_drawdown_usd": None}
    mu = float(daily.mean())
    sd = float(daily.std(ddof=1))
    sharpe = (mu / sd * np.sqrt(252)) if sd > 1e-12 else None
    cum = daily.cumsum()
    peak = cum.cummax()
    dd = cum - peak
    return {"sharpe_daily": sharpe, "max_drawdown_usd": float(dd.min())}


def passive_baseline(frame: pd.DataFrame) -> dict:
    """One $100 buy per test row (no model filter) — coarse market participation baseline."""
    test = frame[frame.split == "test"].copy()
    n_rows = len(test)
    if not n_rows:
        return {"label": "passive_all_test_rows", "test_trades": 0, "cagr_approx": None}
    gross = (TRADE_NOTIONAL * (test["growth_future_30d"] - 1)).sum()
    fees = (-TRADE_NOTIONAL * FEE_RATE * n_rows)
    net = float(gross + fees)
    daily = test.groupby("Date").size()
    q75 = float(daily.quantile(0.75)) if len(daily) else None
    capital = TRADE_NOTIONAL * 30 * q75 if q75 else None
    cagr = None
    if capital and capital > 0:
        cagr = float(((capital + net) / capital) ** (1 / SIM_YEARS))
    return {
        "label": "passive_all_test_rows",
        "test_trades": n_rows,
        "net_pnl_usd": net,
        "cagr_approx": cagr,
        "assumed_capital_usd": capital,
    }


def compare_strategies(frame: pd.DataFrame, pred_columns: list[str]) -> dict:
    rows = []
    for col in pred_columns:
        if col not in frame.columns:
            continue
        sim = vector_simulate(frame, col)
        daily = daily_trade_pnl(frame, col)
        risk = sharpe_and_drawdown(daily)
        rolling = rolling_annualized_returns(daily)
        rows.append(
            {
                "strategy": col,
                **sim,
                **risk,
                **rolling,
            }
        )
    passive = passive_baseline(frame)
    return {"strategies": rows, "passive_baseline": passive}