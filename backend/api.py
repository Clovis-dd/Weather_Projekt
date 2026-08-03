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
from urllib import response

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

from backend.weather_service import (
    WeatherService,
    WeatherAPIError,
    CityNotFoundError,
    InvalidAPIKeyError,
)

from backend.prediction_monitor import (
    prediction_monitor,
)

from backend.model_service import ModelService

from shared.logger import get_logger

from shared.models import (
    HealthResponse,
    WeatherRequest,
    WeatherResponse,
    PredictionData,
)


from backend.database import SessionLocal

from backend.repository import WeatherRepository

from backend.models import WeatherHistory

from shared.models import PredictionData



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

weather_service = WeatherService()


# ======================================================
# Request Model
# ======================================================


class WeatherInput(
    BaseModel
):

    city: str

    language: str = "de"

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
    """
    Liefert den aktuellen Gesundheitsstatus der API.

    Der Health-Endpoint darf niemals durch ein fehlendes
    Modell abstürzen. Stattdessen wird lediglich geprüft,
    ob das Champion-Modell erfolgreich geladen werden kann.
    """

    champion = model_service.get_champion()

    model_loaded = False

    if champion is not None:
        try:
            model_service.get_model()
            model_loaded = True
        except Exception:
            logger.warning(
                "Champion model could not be loaded."
            )

    return HealthResponse(

        status="ok",

        service="weather-api",

        version="1.0.0",

        model_loaded=model_loaded,

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
            datetime.now(UTC) - START_TIME
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
# Weather
# ======================================================

@app.post("/weather")
def response(
    request: WeatherRequest,
) -> WeatherResponse:
    """
    Liefert aktuelle Wetterdaten einer Stadt
    inklusive ML-Vorhersage.
    """

    try:

        raw_data = weather_service.get_weather_by_city(
            city=request.city,
            language=request.language,
        )

        response = weather_service.parse_weather_data(
            raw_data,
            language=request.language,
        )

        prediction_result = predictor.predict(
            {
                "temperature": response.weather.temperature,
                "feels_like": response.weather.feels_like,
                "humidity": response.weather.humidity,
                "pressure": response.weather.pressure,
                "wind_speed": response.weather.wind_speed,
                "clouds": response.weather.clouds,
                "visibility": response.weather.visibility,
            }
        )

        response.prediction = PredictionData(

            value=prediction_result["prediction"],

            model_name=prediction_result["model"],

            features_used=[

                "temperature",

                "feels_like",

                "humidity",

                "pressure",

                "wind_speed",

                "clouds",

                "visibility",

            ],

            prediction_time=datetime.now(UTC),

        )

        session = SessionLocal()

        try:

            repository = WeatherRepository(session)

            repository.save(

                WeatherHistory(

                    city=response.location.city,

                    country=response.location.country,

                    temperature=response.weather.temperature,

                    feels_like=response.weather.feels_like,

                    humidity=response.weather.humidity,

                    pressure=response.weather.pressure,

                    wind_speed=response.weather.wind_speed,

                    prediction=response.prediction.value,

                )

            )

        finally:

            session.close()


        return response

    except CityNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except InvalidAPIKeyError as error:

        raise HTTPException(
            status_code=401,
            detail=str(error),
        ) from error

    except WeatherAPIError as error:

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error


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



# ======================================================
# History
# ======================================================

@app.get(
    "/history"
)
def history() -> list[dict[str, Any]]:
    """
    Liefert alle gespeicherten Vorhersagen.
    """

    session = SessionLocal()

    try:

        repository = WeatherRepository(
            session
        )

        history = repository.get_all()

        return [
            item.to_dict()
            for item in history
        ]

    finally:

        session.close()


@app.get(
    "/history/latest"
)
def latest_history() -> dict[str, Any]:
    """
    Liefert den neuesten Datensatz.
    """

    session = SessionLocal()

    try:

        repository = WeatherRepository(
            session
        )

        history = repository.get_latest()

        if history is None:

            raise HTTPException(
                status_code=404,
                detail="Keine Vorhersagen vorhanden.",
            )

        return history.to_dict()

    finally:

        session.close()


@app.get(
    "/history/{history_id}"
)
def history_by_id(
    history_id: int,
) -> dict[str, Any]:
    """
    Liefert einen Datensatz anhand seiner ID.
    """

    session = SessionLocal()

    try:

        repository = WeatherRepository(
            session
        )

        history = repository.get_by_id(
            history_id
        )

        if history is None:

            raise HTTPException(
                status_code=404,
                detail="Datensatz nicht gefunden.",
            )

        return history.to_dict()

    finally:

        session.close()