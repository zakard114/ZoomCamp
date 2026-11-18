"""RandomForest classifier + probability threshold rule (lecture model)."""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from .config import (
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


def attach_predictions(
    frame: pd.DataFrame, proba: np.ndarray, threshold: float = PRED_THRESHOLD
) -> tuple[pd.DataFrame, str]:
    col = f"pred_rf_{threshold:.2f}"
    out = frame.copy()
    out[col] = (proba >= threshold).astype(int)
    return out, col