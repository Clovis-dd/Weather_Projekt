"""
config.py

Zentrale Konfiguration der Weather App.
"""

from typing import Literal

# ---------------------------------
# Streamlit App Einstellungen
# ---------------------------------

# ---------------------------------
# Titel
# ---------------------------------

PAGE_TITLE = "🌤️ Weather App (OpenWeatherMap)"


# ---------------------------------
# Icon
# ---------------------------------

PAGE_ICON = "🌤️"


# ---------------------------------
# Sprachen
# ---------------------------------

LANGUAGES = {

    "🇩🇪": {
        "code": "de",
        "name": "Deutsch"
    },

    "🇬🇧": {
        "code": "en",
        "name": "English"
    },

    "🇫🇷": {
        "code": "fr",
        "name": "Français"
    }

}

DEFAULT_LANGUAGE = "de"


# ---------------------------------
# Default Standort
# ---------------------------------

DEFAULT_LATITUDE = 52.5200

DEFAULT_LONGITUDE = 13.4050


# ---------------------------------
# Layout
# ---------------------------------

LAYOUT: Literal[
    "centered",
    "wide"
] = "wide"
