"""
backend_client.py

Kommunikation zwischen Streamlit Frontend
und FastAPI Backend.

Verantwortlichkeiten:

- HTTP Kommunikation
- Request Handling
- Request-ID Verarbeitung
- Fehler Mapping
- JSON -> Pydantic Modelle
"""


from typing import Any


import requests


from shared.config import settings


from shared.models import (
    WeatherResponse,
    PredictionData
)


from shared.logger import get_logger



logger = get_logger(
    __name__
)



# ======================================================
# HTTP Session
# ======================================================


_session = requests.Session()



# ======================================================
# Exceptions
# ======================================================


class BackendAPIError(Exception):
    """
    Allgemeiner Backend Fehler.
    """
    pass



class CityNotFoundError(
    BackendAPIError
):
    """
    Standort nicht gefunden.
    """
    pass



class InvalidAPIKeyError(
    BackendAPIError
):
    """
    API-Key Problem.
    """
    pass



class BackendConnectionError(
    BackendAPIError
):
    """
    Backend nicht erreichbar.
    """
    pass



class BackendTimeoutError(
    BackendAPIError
):
    """
    Backend Timeout.
    """
    pass



# ======================================================
# Request Helper
# ======================================================


def _post(
    endpoint: str,
    payload: dict[str, Any]
) -> dict[str, Any]:
    """
    Führt POST Request gegen FastAPI Backend aus.
    """

    url = (
        f"{settings.BACKEND_URL.rstrip('/')}"
        f"{endpoint}"
    )


    logger.info(
        "Backend request endpoint=%s payload=%s",
        endpoint,
        payload
    )


    try:

        response = _session.post(

            url,

            json=payload,

            timeout=settings.REQUEST_TIMEOUT

        )


    except requests.exceptions.ConnectionError as error:

        logger.error(
            "Backend connection failed."
        )

        raise BackendConnectionError(
            "Backend nicht erreichbar."
        ) from error



    except requests.exceptions.Timeout as error:

        logger.error(
            "Backend timeout."
        )

        raise BackendTimeoutError(
            "Backend Timeout."
        ) from error



    logger.info(

        "Backend response status=%s request_id=%s",

        response.status_code,

        response.headers.get(
            "X-Request-ID",
            "-"
        )

    )


    return _handle_response(
        response
    )



# ======================================================
# Response Handling
# ======================================================


def _handle_response(
    response: requests.Response
) -> dict[str, Any]:
    """
    Verarbeitet Backend Antwort.
    """

    request_id = response.headers.get(
        "X-Request-ID",
        "-"
    )


    try:

        data = response.json()


    except ValueError:

        data = {
            "detail": response.text
        }



    if response.status_code == 404:

        logger.warning(
            "Backend 404 request_id=%s detail=%s",
            request_id,
            data.get("detail")
        )

        raise CityNotFoundError(

            data.get(
                "detail",
                "Ort nicht gefunden."
            )

        )



    if response.status_code == 401:

        logger.error(
            "Backend 401 request_id=%s",
            request_id
        )

        raise InvalidAPIKeyError(

            data.get(
                "detail",
                "API Key Fehler."
            )

        )



    if not response.ok:

        logger.error(

            "Backend error status=%s request_id=%s detail=%s",

            response.status_code,

            request_id,

            data.get("detail")

        )


        raise BackendAPIError(

            data.get(
                "detail",
                "Backend Fehler."
            )

        )



    return data



# ======================================================
# Weather
# ======================================================


def get_weather(
    city: str,
    language: str = "de"
) -> WeatherResponse:
    """
    Wetter über Stadtname.
    """

    data = _post(

        "/weather",

        {
            "city": city,

            "language": language
        }

    )


    return WeatherResponse.model_validate(
        data
    )



def get_weather_by_coordinates(
    latitude: float,
    longitude: float,
    language: str = "de"
) -> WeatherResponse:
    """
    Wetter über Koordinaten.
    """

    data = _post(

        "/weather/coordinates",

        {
            "latitude": latitude,

            "longitude": longitude,

            "language": language
        }

    )


    return WeatherResponse.model_validate(
        data
    )


def get_prediction_history() -> list[dict[str, Any]]:
    """
    Holt die komplette Vorhersagehistorie.
    """

    response = _session.get(

        f"{settings.BACKEND_URL}/history",

        timeout=settings.REQUEST_TIMEOUT,

    )

    response.raise_for_status()

    return response.json()


# ======================================================
# Prediction
# ======================================================


def predict(
    area: float
) -> PredictionData:
    """
    Direkte ML Prediction.
    """

    data = _post(

        "/predict",

        {
            "area": area
        }

    )


    return PredictionData.model_validate(
        data
    )