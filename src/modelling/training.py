from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocessing import (
    TARGET_COL,
    add_age_and_drop_leak,
    infer_feature_columns,
    make_preprocessor,
    remove_train_outliers_height,
    split_x_y,
)
from utils import ensure_dir, project_meta, save_joblib, save_json, setup_logger

DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42
DEFAULT_ALPHA = 1.0


def build_pipeline(preprocessor: ColumnTransformer, alpha: float = DEFAULT_ALPHA) -> Pipeline:
    """Build a full pipeline (preprocessor + Ridge model)."""
    from sklearn.linear_model import Ridge

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("ridge", Ridge(alpha=alpha)),
        ]
    )


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute standard regression metrics.

    Args:
        y_true: Ground-truth target values for the validation set.
        y_pred: Predicted target values from the model.

    Returns:
        A dictionary with:
            - rmse: Root Mean Squared Error.
            - mae: Mean Absolute Error.
            - r2: Coefficient of determination.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    return {"rmse": rmse, "mae": mae, "r2": r2}


def train_and_save(
    data_path: str,
    out_dir: str,
    version: str,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
    alpha: float = DEFAULT_ALPHA,
) -> Dict[str, Any]:
    """Train Ridge baseline pipeline and persist as joblib with meta.json."""
    setup_logger()

    # 1) Load & construct Age
    df = pd.read_csv(data_path)
    df = add_age_and_drop_leak(df, add=1.5)

    # 2) Split features/target
    X, y = split_x_y(df, target_col=TARGET_COL)

    # 3) Train/validation split
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # 4) Outlier removal on training only: keep Height <= 0.35
    X_train, y_train = remove_train_outliers_height(X_train, y_train, threshold=0.35)

    # 5) Preprocessor
    categorical_cols, numerical_cols = infer_feature_columns(X_train)
    preprocessor = make_preprocessor(categorical_cols, numerical_cols)

    # 6) Pipeline & fit
    pipe = build_pipeline(preprocessor, alpha=alpha)
    pipe.fit(X_train, y_train)

    # 7) Evaluate
    y_pred = pipe.predict(X_valid)
    metrics = evaluate(y_valid, y_pred)

    # 8) Persist
    out_dir_path = ensure_dir(out_dir)
    pipeline_path = Path(out_dir_path) / f"pipeline__{version}.joblib"
    save_joblib(pipe, pipeline_path)

    meta = {
        "version": version,
        "data_path": str(data_path),
        "artifacts": {"pipeline": str(pipeline_path)},
        "metrics_valid": metrics,
        "split": {"test_size": test_size, "random_state": random_state},
        "model": {"type": "Ridge", "alpha": alpha},
        "preprocessing": {
            "one_hot_drop": "first",
            "handle_unknown": "ignore",
            "scaler": "StandardScaler",
            "categorical_cols": categorical_cols,
            "numerical_cols": numerical_cols,
            "outlier_rule": "keep Height <= 0.35 on training only",
        },
        "meta": project_meta(),
    }
    meta_path = Path(out_dir_path) / f"meta__{version}.json"
    save_json(meta, meta_path)

    return {"pipeline_path": str(pipeline_path), "meta_path": str(meta_path), **metrics}


def main() -> None:
    """Entry point for CLI training.

    Reads arguments, trains the pipeline, saves artifacts (joblib + meta),
    and prints a JSON summary with file paths and metrics.
    """
    res = train_and_save(
        data_path="data/abalone.csv",
        out_dir="src/web_service/local_objects",
        version="v0.0.1",
        test_size=0.2,
        random_state=42,
        alpha=0.5,
    )
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
