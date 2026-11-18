"""Feature sets, dummies, and temporal split (Module 04 lecture logic)."""

import numpy as np
import pandas as pd

from .config import MIN_HISTORY_DATE, TRAIN_PROP, VAL_PROP


def clean_dataframe_from_inf_and_nan(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    out.fillna(0, inplace=True)
    return out


def temporal_split(
    df: pd.DataFrame,
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
    train_prop: float = TRAIN_PROP,
    val_prop: float = VAL_PROP,
) -> pd.DataFrame:
    train_end = min_date + pd.Timedelta(days=(max_date - min_date).days * train_prop)
    val_end = train_end + pd.Timedelta(days=(max_date - min_date).days * val_prop)
    date = df["Date"]
    split = np.where(
        date <= train_end,
        "train",
        np.where(date <= val_end, "validation", "test"),
    )
    out = df.copy()
    out["split"] = split
    return out


def numerical_and_calendar_columns(df_full: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    growth = [g for g in df_full.keys() if g.startswith("growth_") and "future" not in g]
    technical_indicators = [
        "adx", "adxr", "apo", "aroon_1", "aroon_2", "aroonosc",
        "bop", "cci", "cmo", "dx", "macd", "macdsignal", "macdhist", "macd_ext",
        "macdsignal_ext", "macdhist_ext", "macd_fix", "macdsignal_fix",
        "macdhist_fix", "mfi", "minus_di", "mom", "plus_di", "dm", "ppo",
        "roc", "rocp", "rocr", "rocr100", "rsi", "slowk", "slowd", "fastk",
        "fastd", "fastk_rsi", "fastd_rsi", "trix", "ultosc", "willr",
        "ad", "adosc", "obv", "atr", "natr", "ht_dcperiod", "ht_dcphase",
        "ht_phasor_inphase", "ht_phasor_quadrature", "ht_sine_sine", "ht_sine_leadsine",
        "ht_trendmod", "avgprice", "medprice", "typprice", "wclprice",
    ]
    patterns = [g for g in df_full.keys() if "cdl" in g]
    macro = [
        "gdppot_us_yoy", "gdppot_us_qoq", "cpi_core_yoy", "cpi_core_mom",
        "FEDFUNDS", "DGS1", "DGS5", "DGS10",
    ]
    frame = df_full.copy()
    frame["ln_volume"] = np.log(frame.Volume.to_numpy() + 1e-6)
    frame["div_payout"] = (frame.Dividends > 0).astype(int)
    frame["stock_split"] = (frame["Stock Splits"] > 0).astype(int)
    custom = [
        "SMA10", "SMA20", "growing_moving_average", "high_minus_low_relative",
        "volatility", "ln_volume", "div_payout", "stock_split",
    ]
    numerical = growth + technical_indicators + patterns + custom + macro

    df = frame[frame.Date >= MIN_HISTORY_DATE].copy()
    if pd.api.types.is_datetime64_any_dtype(df["Month"]):
        df["Month"] = df["Month"].dt.strftime("%B")
    else:
        df["Month"] = pd.to_datetime(df["Month"], format="%m").dt.strftime("%B")
    df["Weekday"] = df["Weekday"].astype("string")
    df["wom"] = ((df.Date.dt.day - 1) // 7 + 1).astype(str)
    df["month_wom"] = df.Month + "_w" + df.wom
    del df["wom"]
    return df, numerical


# Human-readable buckets for README / rubric
FEATURE_SETS = {
    "TO_PREDICT": "is_positive_growth_30d_future (30d forward return above cutoff)",
    "NUMERIC": "growth_* (past), TA indicators, candle patterns, custom + macro from lectures",
    "DUMMIES": "Month, Weekday, ticker_type (+ optional Ticker, month_wom)",
    "RAW_GROWTH": "growth_future_30d (simulation P&L only, not a model input)",
}


def with_dummies(
    df: pd.DataFrame,
    numerical: list[str],
    drop_ticker_and_month_wom: bool,
    growth_cutoff: float,
) -> tuple[pd.DataFrame, list[str]]:
    frame = df.copy()
    frame["is_positive_growth_30d_future"] = (
        frame["growth_future_30d"] > growth_cutoff
    ).astype(int)
    categorical = ["Month", "Weekday", "Ticker", "ticker_type", "month_wom"]
    if drop_ticker_and_month_wom:
        categorical = [c for c in categorical if c not in ("Ticker", "ticker", "month_wom")]
    dummies = pd.get_dummies(frame[categorical], dtype="int32")
    dummy_names = dummies.columns.to_list()
    frame = pd.concat([frame, dummies], axis=1)
    features = numerical + dummy_names
    frame = temporal_split(frame, frame.Date.min(), frame.Date.max())
    return frame, features


def train_valid_matrices(
    frame: pd.DataFrame, features: list[str]
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    cols = features + ["is_positive_growth_30d_future"]
    train_valid = frame[frame.split.isin(["train", "validation"])][cols].copy()
    all_rows = frame[cols].copy()
    train_valid = clean_dataframe_from_inf_and_nan(train_valid)
    all_rows = clean_dataframe_from_inf_and_nan(all_rows)
    y = train_valid.pop("is_positive_growth_30d_future")
    all_rows.pop("is_positive_growth_30d_future")
    return train_valid, y, all_rows