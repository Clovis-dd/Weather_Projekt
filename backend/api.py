"""
backend/api.py

Production FastAPI Service.

Architektur:

API
 |
 Predictor
 |
 ModelLoader
 |
 ModelRegistry
"""


from __future__ import annotations

import os
from pathlib import Path

from typing import Any

from datetime import UTC, datetime

from backend.middleware import RequestIDMiddleware

START_TIME = datetime.now(
    UTC
)

from fastapi import (
    FastAPI,
    HTTPException,
)

from pydantic import BaseModel

from backend.model_loader import ModelLoader

from backend.model_registry import ModelRegistry

from backend.predictor import WeatherPredictor

from backend.prediction_monitor import (
    prediction_monitor,
)

from backend.model_service import ModelService

from shared.logger import get_logger
from shared.models import HealthResponse

logger = get_logger(
    __name__
)



# ======================================================
# Configuration
# ======================================================

MODELS_DIR = Path(
    os.getenv(
        "MODELS_DIR",
        "models"
    )
)


model_service = ModelService(
    MODELS_DIR
)


# ======================================================
# FastAPI
# ======================================================


app = FastAPI(

    title="Weather ML API",

    version="1.0",

)

app.add_middleware(
    RequestIDMiddleware
)

# ======================================================
# Services
# ======================================================


registry = ModelRegistry(
    MODELS_DIR
)


loader = ModelLoader(
    MODELS_DIR
)


def create_predictor() -> WeatherPredictor:
    return WeatherPredictor(
        MODELS_DIR
    )

predictor = create_predictor()


# ======================================================
# Request Model
# ======================================================


class WeatherInput(
    BaseModel
):

    temperature: float

    feels_like: float

    humidity: float

    pressure: float

    wind_speed: float

    clouds: float

    visibility: float



# ======================================================
# Health
# ======================================================

@app.get("/")
def root():

    return {
        "service": "Weather ML API",
        "status": "running",
        "version": "1.0",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:

    champion = model_service.get_champion()


    return HealthResponse(

        status="ok",

        service="weather-api",

        version="1.0.0",

        model_loaded=(
                model_service.get_model()
                is not None
        ),

        active_model=(
            champion.name
            if champion
            else None
        ),

        model_algorithm=(
            champion.algorithm
            if champion
            else None
        ),

        feature_schema_version=(
            champion.feature_schema_version
            if champion
            else None
        ),

        model_metrics=(
            champion.metrics
            if champion
            else None
        ),

        prediction_count=(
            prediction_monitor.predictions_total
        ),

        uptime_seconds=(
                datetime.now(UTC)
                -
                START_TIME
        ).total_seconds(),

        utc_time=datetime.now(UTC),
    )



# ======================================================
# Model Info
# ======================================================


@app.get(
    "/model"
)
def model_info() -> dict[str, Any]:


    champion = (
        registry.get_champion()
    )


    if champion is None:

        raise HTTPException(

            status_code=503,

            detail="No champion model available",

        )


    return {

        "model":
            champion.name,

        "algorithm":
            champion.algorithm,

        "feature_schema_version":
            champion.feature_schema_version,

        "metrics":
            champion.metrics,

    }


# ======================================================
# Metrics
# ======================================================

@app.get(
    "/metrics"
)
def metrics() -> dict[str, Any]:

    return prediction_monitor.get_metrics()


# ======================================================
# Prediction
# ======================================================


@app.post(
    "/predict"
)
def predict(
    data: WeatherInput,
) -> dict[str, Any]:


    logger.info(
        "API prediction request received"
    )


    try:

        result = predictor.predict(

            data.model_dump()

        )


        return result



    except Exception as error:


        logger.exception(
            "Prediction failed"
        )


        raise HTTPException(

            status_code=500,

            detail=str(error),

        ) from error