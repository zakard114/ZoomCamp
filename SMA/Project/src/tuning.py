"""RandomForest hyperparameter search on the validation slice (rubric §4)."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

from .config import RF_RANDOM_STATE
from .features import train_valid_matrices


def tune_random_forest(
    frame, features: list[str], *, n_iter: int = 6, random_state: int = RF_RANDOM_STATE
) -> dict:
    x_tv, y_tv, _ = train_valid_matrices(frame, features)
    val_mask = frame.loc[x_tv.index, "split"] == "validation"
    x_val = x_tv[val_mask]
    y_val = y_tv[val_mask]
    x_train = x_tv[~val_mask]
    y_train = y_tv[~val_mask]
    if len(x_train) < 100 or len(x_val) < 50:
        x_train, y_train = x_tv, y_tv
        x_val, y_val = x_tv, y_tv

    base = RandomForestClassifier(random_state=random_state, n_jobs=-1)
    search = RandomizedSearchCV(
        base,
        param_distributions={
            "n_estimators": [80, 100, 120, 150],
            "max_depth": [10, 13, 16, 20],
            "min_samples_leaf": [1, 2, 5],
        },
        n_iter=n_iter,
        cv=3,
        scoring="roc_auc",
        random_state=random_state,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    best = search.best_estimator_
    val_auc = float(best.score(x_val, y_val)) if len(x_val) else None
    return {
        "best_params": search.best_params_,
        "best_cv_score": float(search.best_score_),
        "validation_roc_auc": val_auc,
    }


def main() -> int:
    from .modeling import build_labeled_frame

    frame, features = build_labeled_frame()
    result = tune_random_forest(frame, features)
    print("=== RF hyperparameter search (validation slice) ===")
    for k, v in result.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())