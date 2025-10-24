# src/flows/training_flow.py
from __future__ import annotations
from prefect import flow, task
from typing import Dict, Any

# === Import your existing modules ===
from src.modelling.training import train_and_save
from src.modelling.predicting import predict_csv


# === Configuration parameters ===
DATA_PATH = "data/abalone.csv"
OUT_DIR = "src/web_service/local_objects"
VERSION = "v0.0.1"
PIPELINE_PATH = f"{OUT_DIR}/pipeline__{VERSION}.joblib"
PREDICTION_OUT = f"{OUT_DIR}/predictions.csv"


# === Define Prefect tasks ===
@task(name="Train model and save")
def task_train() -> Dict[str, Any]:
    """Call the existing training function."""
    return train_and_save(
        data_path=DATA_PATH,
        out_dir=OUT_DIR,
        version=VERSION,
        test_size=0.2,
        random_state=42,
        alpha=0.5,
    )


@task(name="Run predictions")
def task_predict(pipeline_path: str, csv_path: str, out_csv: str) -> Dict[str, Any]:
    """Call the existing prediction function."""
    return predict_csv(pipeline_path, csv_path, out_csv)


# === Define main flow ===
@flow(name="Abalone Training and Prediction Flow")
def training_flow() -> None:
    """Prefect workflow: training + prediction."""
    train_info = task_train()
    pred_info = task_predict(PIPELINE_PATH, DATA_PATH, PREDICTION_OUT)

    print("\n Training completed!")
    print(train_info)
    print("\n Prediction completed!")
    print(pred_info)
    return {"train": train_info, "predict": pred_info}


if __name__ == "__main__":
    training_flow()
