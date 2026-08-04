"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers.weather

Description:
    Stellt REST-Endpunkte zum Abruf aktueller Wetterdaten,
    zur ML-Vorhersage sowie zur Speicherung der Ergebnisse
    in der Datenbank bereit.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

# ======================================================
# Standard Library
# ======================================================

from datetime import UTC, datetime

# ======================================================
# Third Party
# ======================================================

from fastapi import (
    APIRouter,
    HTTPException,
)

# ======================================================
# Project Imports
# ======================================================

from backend.database import SessionLocal

from backend.models import WeatherHistory

from backend.dependencies import (
    predictor,
    weather_service,
)


from backend.services.weather_service import (
    CityNotFoundError,
    InvalidAPIKeyError,
    WeatherAPIError,
)

from backend.repository import WeatherRepository

from shared.logger import get_logger

from shared.models import (
    PredictionData,
    WeatherRequest,
    WeatherResponse,
)

# ======================================================
# Router Configuration
# ======================================================

router = APIRouter(
    prefix="",
    tags=["Weather"],
)

# ======================================================
# Logger
# ======================================================

logger = get_logger(__name__)


# ======================================================
# Weather Endpoint
# ======================================================

@router.post(
    "/weather",
    response_model=WeatherResponse,
    summary="Current Weather & ML Prediction",
    description=(
        "Retrieves current weather data from OpenWeatherMap, "
        "generates a machine learning prediction and "
        "stores the result in the prediction history."
    ),
)
def get_weather(
    request: WeatherRequest,
) -> WeatherResponse:
    """
    Retrieves current weather information for a given city,
    performs a machine-learning prediction and returns the
    enriched weather response.
    """

    logger.info(
        "Weather request received for city '%s'.",
        request.city,
    )

    try:

        raw_weather = weather_service.get_weather_by_city(
            city=request.city,
            language=request.language,
        )

        response = weather_service.parse_weather_data(
            raw_weather,
            language=request.language,
        )

        feature_vector = {
            "temperature": response.weather.temperature,
            "feels_like": response.weather.feels_like,
            "humidity": response.weather.humidity,
            "pressure": response.weather.pressure,
            "wind_speed": response.weather.wind_speed,
            "clouds": response.weather.clouds,
            "visibility": response.weather.visibility,
        }

        prediction_result = predictor.predict(
            feature_vector,
        )

        response.prediction = PredictionData(
            value=prediction_result["prediction"],
            model_name=prediction_result["model"],
            prediction_time=datetime.now(UTC),
            features_used=list(feature_vector.keys()),
        )


        # ==================================================
        # Persist Prediction
        # ==================================================

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

        logger.info(
            "Prediction successfully created for '%s'.",
            response.location.city,
        )

        return response

    # ==================================================
    # Exception Handling
    # ==================================================

    except CityNotFoundError as error:

        logger.warning(
            "City '%s' not found.",
            request.city,
        )

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except InvalidAPIKeyError as error:

        logger.error(
            "Invalid OpenWeatherMap API key.",
        )

        raise HTTPException(
            status_code=401,
            detail=str(error),
        ) from error

    except WeatherAPIError as error:

        logger.exception(
            "Weather service failed.",
        )

        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except Exception as error:

        logger.exception(
            "Unexpected error while processing weather request.",
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from error