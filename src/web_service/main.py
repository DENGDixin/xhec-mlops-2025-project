# Code with FastAPI (app = FastAPI(...))

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from loguru import logger
from typing import Any

from .lib.models import AbaloneInput, PredictionOutput
from ..modelling.utils import load_joblib

# Initialize FastAPI app
app = FastAPI(
    title="Abalone Age Prediction API",
    description="API for predicting the age of abalone based on physical measurements",
    version="1.0.0",
)

# Global variable to store the loaded pipeline
_pipeline = None
PIPELINE_PATH = Path(__file__).parent / "local_objects" / "pipeline__v0.0.1.joblib"


def get_pipeline() -> Any:
    """Load the pipeline once and cache it."""
    global _pipeline
    if _pipeline is None:
        try:
            _pipeline = load_joblib(PIPELINE_PATH)
            logger.info(f"Pipeline loaded from {PIPELINE_PATH}")
        except Exception as e:
            logger.error(f"Failed to load pipeline: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load model pipeline: {str(e)}")
    return _pipeline


@app.get("/")
def home() -> dict:
    """Health check endpoint."""
    return {"health_check": "App up and running!", "version": "1.0.0"}


@app.post("/predict", response_model=PredictionOutput, status_code=201)
def predict(payload: AbaloneInput) -> PredictionOutput:
    """Predict the age of an abalone based on physical measurements.

    Args:
        payload: AbaloneInput containing all required features

    Returns:
        PredictionOutput with predicted age
    """
    try:
        # Load the pipeline
        pipeline = get_pipeline()

        # Convert Pydantic model to DataFrame
        # Use model_dump with by_alias=True to get the correct column names
        input_data = payload.dict(by_alias=True)
        df = pd.DataFrame([input_data])

        # Make prediction
        prediction = pipeline.predict(df)
        predicted_age = float(prediction[0])

        logger.info(f"Prediction made: {predicted_age:.2f} years")

        return PredictionOutput(predicted_age=predicted_age)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/health")
def health_check() -> dict:
    """Extended health check that verifies the model is loaded."""
    try:
        pipeline = get_pipeline()
        return {"status": "healthy", "model_loaded": pipeline is not None, "pipeline_path": str(PIPELINE_PATH)}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "unhealthy", "error": str(e)})
