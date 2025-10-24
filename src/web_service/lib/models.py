# Pydantic models for the web service

from pydantic import BaseModel, Field
from typing import Literal


class AbaloneInput(BaseModel):
    """Input model for single abalone prediction."""

    Sex: Literal["M", "F", "I"] = Field(..., description="Sex of the abalone: M (male), F (female), I (infant)")
    Length: float = Field(..., gt=0, description="Longest shell measurement (mm)")
    Diameter: float = Field(..., gt=0, description="Perpendicular to length (mm)")
    Height: float = Field(..., gt=0, description="With meat in shell (mm)")
    Whole_weight: float = Field(..., gt=0, description="Whole abalone weight (grams)", alias="Whole weight")
    Shucked_weight: float = Field(..., gt=0, description="Weight of meat (grams)", alias="Shucked weight")
    Viscera_weight: float = Field(..., gt=0, description="Gut weight after bleeding (grams)", alias="Viscera weight")
    Shell_weight: float = Field(..., gt=0, description="Weight after being dried (grams)", alias="Shell weight")

    class Config:
        """Pydantic configuration."""

        populate_by_name = True
        json_schema_extra = {
            "example": {
                "Sex": "M",
                "Length": 0.455,
                "Diameter": 0.365,
                "Height": 0.095,
                "Whole weight": 0.514,
                "Shucked weight": 0.2245,
                "Viscera weight": 0.101,
                "Shell weight": 0.15,
            }
        }


class PredictionOutput(BaseModel):
    """Output model for prediction results."""

    predicted_age: float = Field(..., description="Predicted age of the abalone (years)")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"predicted_age": 11.5}}
