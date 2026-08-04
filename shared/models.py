"""
shared.models

Gemeinsame Pydantic Datenmodelle
für Backend und Frontend.

Architektur:

OpenWeatherMap
        |
        ↓
WeatherService
        |
        ↓
shared.models
        |
        ↓
FastAPI
        |
        ↓
Streamlit
"""


from datetime import datetime

from pydantic import BaseModel, Field


# ======================================================
# Requests
# ======================================================


class WeatherRequest(BaseModel):
    """
    Wetteranfrage über Stadt.
    """

    city: str = Field(
        min_length=1,
        description="Stadtname"
    )


    language: str = Field(
        default="de",
        description="Antwortsprache"
    )



class CoordinatesRequest(BaseModel):
    """
    Wetteranfrage über Koordinaten.
    """

    latitude: float = Field(
        ge=-90,
        le=90
    )


    longitude: float = Field(
        ge=-180,
        le=180
    )


    language: str = Field(
        default="de"
    )



class PredictionRequest(BaseModel):
    """
    Direkte ML Anfrage.

    Enthält die Wetterfeatures,
    welche durch das Machine-Learning-Modell
    verarbeitet werden.
    """

    temperature: float = Field(
        description="Aktuelle Temperatur in °C"
    )

    feels_like: float = Field(
        description="Gefühlte Temperatur in °C"
    )

    humidity: float = Field(
        description="Relative Luftfeuchtigkeit in Prozent"
    )

    pressure: float = Field(
        description="Luftdruck in hPa"
    )

    wind_speed: float = Field(
        description="Windgeschwindigkeit"
    )

    clouds: float = Field(
        description="Bewölkungsgrad in Prozent"
    )

    visibility: float = Field(
        description="Sichtweite in Metern"
    )



# ======================================================
# Location
# ======================================================


class LocationData(BaseModel):
    """
    Standortinformationen.
    """

    city: str = "Unbekannt"

    country: str = "-"

    country_name: str | None = None

    latitude: float = 0

    longitude: float = 0



# ======================================================
# Weather
# ======================================================


class WeatherData(BaseModel):
    """
    Wetterinformationen.
    """

    weather_id: int | None = None


    temperature: float = 0


    feels_like: float = 0


    minimum: float = 0


    maximum: float = 0


    humidity: int = 0


    pressure: int = 0


    wind_speed: float = 0


    wind_direction: int = 0


    visibility: float = 0


    clouds: int = 0


    description: str = "-"


    icon: str = ""



# ======================================================
# Sonne
# ======================================================


class SunData(BaseModel):
    """
    Sonneninformationen.
    """

    sunrise: datetime | None = None

    sunset: datetime | None = None



class PredictionData(BaseModel):
    """
    Ergebnis einer Wettervorhersage
    durch das ML-Modell.
    """


    value: float = Field(
        description="Berechneter Wetterkomfort-Score"
    )


    model_name: str = Field(
        description="Aktiv verwendetes ML-Modell"
    )


    features_used: list[str] = Field(
        description="Features welche das Modell verwendet"
    )


    prediction_time: datetime = Field(
        description="Zeitpunkt der Berechnung"
    )



# ======================================================
# Prediction Response
# ======================================================

class PredictionResponse(BaseModel):
    """
    Response für direkten ML Prediction Endpoint.
    """

    prediction: float

    model: str | None = None

    features_used: list[str]

    prediction_time: datetime



# ======================================================
# Weather Response
# ======================================================

class WeatherResponse(BaseModel):
    """
    Vollständige Wetterantwort.
    """

    location: LocationData


    weather: WeatherData


    sun: SunData | None = None


    prediction: PredictionData | None = None


    timestamp: datetime


    language: str = "de"



# ======================================================
# Health Response
# ======================================================

class HealthResponse(BaseModel):
    """
    Antwort des Health-Endpunkts.
    """

    status: str

    service: str

    version: str

    model_loaded: bool

    active_model: str | None = None

    model_algorithm: str | None = None

    feature_schema_version: str | None = None

    model_metrics: dict[str, float] | None = None

    prediction_count: int

    uptime_seconds: float | None = None

    utc_time: datetime



# ======================================================
# ModelInfo Response
# ======================================================

class ModelInfoResponse(BaseModel):

    name: str

    filename: str | None = None

    algorithm: str | None = None

    metrics: dict[str, float] | None = None

    created_at: datetime | None = None

    status: str | None = None



# ======================================================
# Metrics Response
# ======================================================

class MetricsResponse(BaseModel):

    predictions_total: int

    prediction_errors: int

    average_latency_ms: float | None = None

    last_model_name: str | None = None