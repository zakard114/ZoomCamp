"""Lecture models: RandomForest + DecisionTree, probability threshold rules."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from .config import (
    DT_MAX_DEPTH,
    DT_RANDOM_STATE,
    GROWTH_CUTOFF,
    DROP_TICKER_AND_MONTH_WOM,
    PRED_THRESHOLD,
    RF_MAX_DEPTH,
    RF_N_ESTIMATORS,
    RF_RANDOM_STATE,
)
from .features import numerical_and_calendar_columns, with_dummies, train_valid_matrices
from .load_data import load_combined_parquet


def build_labeled_frame(df_raw: pd.DataFrame | None = None) -> tuple[pd.DataFrame, list[str]]:
    raw = df_raw if df_raw is not None else load_combined_parquet()
    base, numerical = numerical_and_calendar_columns(raw)
    frame, features = with_dummies(
        base,
        numerical,
        drop_ticker_and_month_wom=DROP_TICKER_AND_MONTH_WOM,
        growth_cutoff=GROWTH_CUTOFF,
    )
    return frame, features


def fit_random_forest(
    frame: pd.DataFrame, features: list[str]
) -> tuple[RandomForestClassifier, np.ndarray]:
    x_tv, y_tv, x_all = train_valid_matrices(frame, features)
    model = RandomForestClassifier(
        n_estimators=RF_N_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        random_state=RF_RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(x_tv, y_tv)
    proba = model.predict_proba(x_all)[:, 1]
    return model, proba


def fit_decision_tree(
    frame: pd.DataFrame, features: list[str]
) -> tuple[DecisionTreeClassifier, np.ndarray]:
    x_tv, y_tv, x_all = train_valid_matrices(frame, features)
    model = DecisionTreeClassifier(
        max_depth=DT_MAX_DEPTH,
        random_state=DT_RANDOM_STATE,
    )
    model.fit(x_tv, y_tv)
    proba = model.predict_proba(x_all)[:, 1]
    return model, proba


def attach_predictions(
    frame: pd.DataFrame,
    proba: np.ndarray,
    threshold: float = PRED_THRESHOLD,
    *,
    prefix: str = "pred_rf",
) -> tuple[pd.DataFrame, str]:
    col = f"{prefix}_{threshold:.2f}"
    out = frame.copy()
    out[col] = (proba >= threshold).astype(int)
    return out, col


def fit_xgboost(frame: pd.DataFrame, features: list[str]):
    """Optional third model (rubric §4); skips cleanly if xgboost is not installed."""
    try:
        import xgboost as xgb
    except ImportError:
        return None, None
    x_tv, y_tv, x_all = train_valid_matrices(frame, features)
    model = xgb.XGBClassifier(
        n_estimators=120,
        max_depth=8,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.85,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        eval_metric="logloss",
    )
    model.fit(x_tv, y_tv)
    proba = model.predict_proba(x_all)[:, 1]
    return model, proba


def attach_all_strategy_columns(
    frame: pd.DataFrame,
    proba_rf: np.ndarray,
    proba_dt: np.ndarray,
    thresholds: tuple[float, ...] = (0.55, 0.57),
    *,
    proba_xgb: np.ndarray | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    out = frame.copy()
    out["proba_rf"] = proba_rf
    out["proba_dt"] = proba_dt
    columns: list[str] = []
    for thr in thresholds:
        col = f"pred_rf_{thr:.2f}"
        out[col] = (proba_rf >= thr).astype(int)
        columns.append(col)
    col_dt = f"pred_dt_{thresholds[0]:.2f}"
    out[col_dt] = (proba_dt >= thresholds[0]).astype(int)
    columns.append(col_dt)
    if proba_xgb is not None:
        out["proba_xgb"] = proba_xgb
        col_xgb = f"pred_xgb_{thresholds[0]:.2f}"
        out[col_xgb] = (proba_xgb >= thresholds[0]).astype(int)
        columns.append(col_xgb)
    return out, columns