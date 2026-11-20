"""Benchmark CAGR vs lecture panel buy-and-hold proxy (^GSPC daily via yfinance)."""

from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd

from .config import SIM_YEARS


def _yf_download(ticker: str, start: str, end: str) -> pd.Series:
    import yfinance as yf

    px = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if px.empty:
        return pd.Series(dtype=float)
    if isinstance(px.columns, pd.MultiIndex):
        px = px.droplevel(1, axis=1)
    return px["Close"].sort_index()


def spy_buy_hold_cagr(frame: pd.DataFrame, *, symbol: str = "^GSPC") -> dict:
    """CAGR of holding SPX over the same calendar window as `split == test`."""
    test = frame[frame.split == "test"]
    if test.empty:
        return {"label": "spy_buy_hold", "cagr_approx": None, "error": "no test rows"}
    start = pd.to_datetime(test["Date"]).min()
    end = pd.to_datetime(test["Date"]).max() + pd.Timedelta(days=5)
    try:
        close = _yf_download(symbol, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    except Exception as exc:  # noqa: BLE001 — optional dependency at runtime
        return {"label": "spy_buy_hold", "cagr_approx": None, "error": str(exc)}
    if close.empty or len(close) < 2:
        return {"label": "spy_buy_hold", "cagr_approx": None, "error": "empty yfinance series"}
    years = max((close.index[-1] - close.index[0]).days / 365.25, SIM_YEARS)
    total_return = float(close.iloc[-1] / close.iloc[0])
    cagr = float(total_return ** (1 / years))
    return {
        "label": "spy_buy_hold",
        "symbol": symbol,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "years": years,
        "cagr_approx": cagr,
        "fetched_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def strategy_beats_benchmark(strategy_cagr: float | None, benchmark_cagr: float | None) -> bool | None:
    if strategy_cagr is None or benchmark_cagr is None:
        return None
    return strategy_cagr > benchmark_cagr