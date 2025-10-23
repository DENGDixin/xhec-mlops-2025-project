from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Column constants
TARGET_COL = "Age"
RINGS_COL = "Rings"
HEIGHT_COL = "Height"
CATEGORICAL_INCLUDE = ["object"]
NUMERICAL_INCLUDE = ["int64", "float64"]


def add_age_and_drop_leak(df: pd.DataFrame, add: float = 1.5) -> pd.DataFrame:
    """Add target Age = Rings + 1.5 and return a new DataFrame."""
    df = df.copy()
    if RINGS_COL in df.columns:
        df[TARGET_COL] = df[RINGS_COL] + add
    return df


def split_x_y(df: pd.DataFrame, target_col: str = TARGET_COL) -> tuple[pd.DataFrame, np.ndarray]:
    """Split features and target arrays."""
    if target_col not in df.columns:
        raise ValueError(f"Target column `{target_col}` not found in dataframe.")
    y = df[target_col].to_numpy()
    X = df.drop(columns=[target_col, RINGS_COL], errors="ignore").copy()
    return X, y


def remove_train_outliers_height(
    X_train: pd.DataFrame, y_train: np.ndarray, threshold: float = 0.35
) -> tuple[pd.DataFrame, np.ndarray]:
    """Remove outliers where Height > 0.35 (training set only)."""
    if HEIGHT_COL not in X_train.columns:
        return X_train, y_train
    mask = X_train[HEIGHT_COL] <= threshold
    return X_train.loc[mask].copy(), y_train[mask].copy()


def infer_feature_columns(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Infer categorical and numerical column names."""
    categorical_cols = X.select_dtypes(include=CATEGORICAL_INCLUDE).columns.tolist()
    numerical_cols = X.select_dtypes(include=NUMERICAL_INCLUDE).columns.tolist()
    return categorical_cols, numerical_cols


def make_preprocessor(categorical_cols: list[str], numerical_cols: list[str]) -> ColumnTransformer:
    """Build the preprocessing transformer: StandardScaler + OneHotEncoder."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), categorical_cols),
        ],
        remainder="passthrough",
    )
