from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from preprocessing import TARGET_COL, RINGS_COL
from utils import load_joblib, setup_logger


def prepare_inference_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Remove target-related columns before inference to avoid leakage."""
    drop_cols = [TARGET_COL, RINGS_COL]
    return df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")


def predict_dataframe(pipeline_path: str | Path, df: pd.DataFrame) -> np.ndarray:
    """Run predictions using the saved pipeline on a dataframe."""
    pipe = load_joblib(pipeline_path)
    X = prepare_inference_frame(df)
    return pipe.predict(X)


def predict_csv(pipeline_path: str | Path, csv_path: str | Path, out_csv: str | None = None) -> dict[str, Any]:
    """Predict from a CSV file and optionally save the results."""
    setup_logger()
    df = pd.read_csv(csv_path)
    preds = predict_dataframe(pipeline_path, df)
    result = {
        "n_rows": int(len(df)),
        "pred_head": [float(x) for x in preds[:5]],
        "pred_mean": float(np.mean(preds)),
        "pred_std": float(np.std(preds)),
    }
    if out_csv:
        out_df = df.copy()
        out_df["pred_age"] = preds
        Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(out_csv, index=False)
        result["saved"] = str(out_csv)
    return result


def main() -> None:
    """Command-line entry for prediction."""
    res = predict_csv(
        "src/web_service/local_objects/pipeline__v0.0.1.joblib",
        "data/abalone.csv",
        "src/web_service/local_objects/predictions.csv",
    )
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
