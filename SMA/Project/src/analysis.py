"""Post-model diagnostics: precision/recall slices for rubric deep analysis."""

from __future__ import annotations

import pandas as pd

from .config import GROWTH_CUTOFF


def _binary_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    prec = tp / (tp + fp) if (tp + fp) else None
    rec = tp / (tp + fn) if (tp + fn) else None
    return {"signals": tp + fp, "precision": prec, "recall": rec}


def prediction_diagnostics(frame: pd.DataFrame, pred_col: str) -> dict:
    """Break down rule quality on the test split by ticker and calendar month."""
    test = frame[frame.split == "test"].copy()
    target = (test["growth_future_30d"] >= GROWTH_CUTOFF).astype(int)
    pred = test[pred_col].astype(int)
    overall = _binary_metrics(target, pred)

    by_ticker = []
    for ticker, chunk in test.groupby("Ticker"):
        y_t = (chunk["growth_future_30d"] >= GROWTH_CUTOFF).astype(int)
        y_p = chunk[pred_col].astype(int)
        m = _binary_metrics(y_t, y_p)
        if m["signals"]:
            by_ticker.append({"ticker": str(ticker), **m})
    by_ticker.sort(key=lambda r: r["signals"], reverse=True)

    by_month = []
    if "Month" in test.columns:
        for month, chunk in test.groupby("Month"):
            y_t = (chunk["growth_future_30d"] >= GROWTH_CUTOFF).astype(int)
            y_p = chunk[pred_col].astype(int)
            by_month.append({"month": str(month), **_binary_metrics(y_t, y_p)})
    else:
        test["_month"] = pd.to_datetime(test["Date"]).dt.month
        for month, chunk in test.groupby("_month"):
            y_t = (chunk["growth_future_30d"] >= GROWTH_CUTOFF).astype(int)
            y_p = chunk[pred_col].astype(int)
            by_month.append({"month": int(month), **_binary_metrics(y_t, y_p)})

    worst_fp = []
    fp_mask = (pred == 1) & (target == 0)
    if fp_mask.any():
        cols = ["Date", "Ticker", "growth_future_30d", pred_col]
        worst_fp = (
            test.loc[fp_mask, cols]
            .sort_values("growth_future_30d")
            .head(10)
            .astype({"Date": str})
            .to_dict(orient="records")
        )

    return {
        "pred_column": pred_col,
        "overall_test": overall,
        "by_ticker_top_signals": by_ticker[:15],
        "by_month": by_month,
        "sample_false_positive_rows": worst_fp,
        "improvement_ideas": [
            "Raise threshold on tickers with precision < 0.45 in by_ticker slice.",
            "Add volatility regime filter (trade when realized vol above median).",
            "Blend DT and RF proba for low-liquidity names (high ln_volume requirement).",
        ],
    }