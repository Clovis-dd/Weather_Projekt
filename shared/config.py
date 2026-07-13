"""
config.py

Zentrale Konfiguration der Weather App.

Gemeinsam genutzt von:

- Backend
- Frontend
- Logging
- Runtime Umgebung

Die ML-Modelldefinition liegt in:

shared.weather_model
"""

from pathlib import Path
from typing import Literal

from pydantic import Field

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


# ======================================================
# App
# ======================================================

PAGE_TITLE = "🌤️ Weather App"

PAGE_ICON = "🌤️"


LAYOUT: Literal[
    "centered",
    "wide",
] = "wide"



# ======================================================
# Sprache
# ======================================================

LANGUAGES = {

    "🇩🇪": {
        "code": "de",
        "name": "Deutsch",
    },

    "🇬🇧": {
        "code": "en",
        "name": "English",
    },

    "🇫🇷": {
        "code": "fr",
        "name": "Français",
    },

}


DEFAULT_LANGUAGE = "de"



# ======================================================
# Default Position
# ======================================================

DEFAULT_LATITUDE = 52.5200

DEFAULT_LONGITUDE = 13.4050



# ======================================================
# Runtime Settings
# ======================================================


class Settings(BaseSettings):
    """
    Zentrale Runtime-Konfiguration.

    Enthält keine fachliche
    Modelllogik.
    """


    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

        case_sensitive=True,

        extra="ignore",

    )


    # --------------------------------------------------
    # Server
    # --------------------------------------------------

    HOST: str = Field(

        default="127.0.0.1"

    )


    PORT: int = Field(

        default=9000

    )


    # --------------------------------------------------
    # Backend Kommunikation
    # --------------------------------------------------

    BACKEND_URL: str = Field(

        default="http://127.0.0.1:9000"

    )


    REQUEST_TIMEOUT: int = Field(

        default=10

    )


    # --------------------------------------------------
    # OpenWeatherMap
    # --------------------------------------------------

    OWM_API_KEY: str = Field(

        default=""

    )


    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    LOG_LEVEL: str = Field(

        default="INFO"

    )


    LOG_DIR: Path = Field(

        default=Path("logs")

    )


    APP_LOG_FILE: Path = Field(

        default=Path(
            "logs/app.log"
        )

    )


    WARNING_LOG_FILE: Path = Field(

        default=Path(
            "logs/warning.log"
        )

    )


    ERROR_LOG_FILE: Path = Field(

        default=Path(
            "logs/error.log"
        )

    )


    # --------------------------------------------------
    # Machine Learning Runtime
    # --------------------------------------------------

    MODEL_PATH: Path = Field(

        default=Path(
            "models/weather_model.pkl"
        )

    )



# ======================================================
# Singleton
# ======================================================

settings = Settings()