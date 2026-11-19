"""Exploratory analysis helpers (rubric §3): target rate, correlations, breakdowns."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = PROJECT_ROOT / "docs" / "figures"


def target_summary(frame: pd.DataFrame) -> dict:
    if "is_positive_growth_30d_future" not in frame.columns:
        return {}
    s = frame["is_positive_growth_30d_future"]
    by_split = frame.groupby("split")["is_positive_growth_30d_future"].mean().to_dict()
    by_type = (
        frame.groupby("ticker_type")["is_positive_growth_30d_future"].mean().sort_values(ascending=False)
    )
    return {
        "positive_rate_overall": float(s.mean()),
        "positive_rate_by_split": {k: float(v) for k, v in by_split.items()},
        "positive_rate_by_ticker_type": {k: float(v) for k, v in by_type.head(8).items()},
    }


def top_feature_correlations(
    frame: pd.DataFrame, features: list[str], top_n: int = 15
) -> pd.Series:
    target = "is_positive_growth_30d_future"
    tv = frame[frame.split.isin(["train", "validation"])][features + [target]]
    tv = tv.replace([np.inf, -np.inf], np.nan).fillna(0)
    corrs = tv[features].corrwith(tv[target]).abs().sort_values(ascending=False)
    return corrs.head(top_n)


def save_correlation_bar(frame: pd.DataFrame, features: list[str], path: Path | None = None) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    corrs = top_feature_correlations(frame, features, top_n=12)
    path = path or FIGURES_DIR / "eda_top_correlations.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    corrs.sort_values().plot(kind="barh", ax=ax, color="#d4a24c")
    ax.set_title("|corr| with is_positive_growth_30d_future (train+valid)")
    ax.set_xlabel("absolute correlation")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def run_eda_report(frame: pd.DataFrame, features: list[str]) -> dict:
    summary = target_summary(frame)
    corrs = top_feature_correlations(frame, features, top_n=15)
    fig = save_correlation_bar(frame, features)
    return {
        "summary": summary,
        "top_correlations": {k: float(v) for k, v in corrs.items()},
        "figure": str(fig) if fig else None,
    }