"""
app.py

Streamlit Frontend der Weather App.

Architektur:

Streamlit
    |
    ↓
frontend.backend_client
    |
    ↓
FastAPI Backend
    |
    ↓
OpenWeatherMap API


Verantwortlichkeiten:

- UI Darstellung
- Sprache
- Benutzerinteraktion
- Backend Kommunikation
- Wetteranzeige
- Prediction Anzeige
"""


import streamlit as st

from frontend.backend_client import (
    get_weather,
    get_weather_by_coordinates,
    BackendAPIError,
    CityNotFoundError,
    InvalidAPIKeyError,
    BackendConnectionError,
    BackendTimeoutError
)


from frontend.components.language_selector import (
    render_language_selector
)


from shared.models import (
    WeatherResponse,
    PredictionData
)


from shared.config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    DEFAULT_LANGUAGE,
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE
)


from shared.logger import (
    get_logger
)



logger = get_logger(
    __name__
)



# ======================================================
# Streamlit Konfiguration
# ======================================================


st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout=LAYOUT,

    initial_sidebar_state="expanded"

)



# ======================================================
# Session State
# ======================================================


def initialize_session_state() -> None:
    """
    Initialisiert Streamlit Session Variablen.
    """


    defaults = {

        "language": DEFAULT_LANGUAGE,

        "weather_data": None,

        "prediction": None

    }


    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ======================================================
# Übersetzungen
# ======================================================


def get_weather_texts(
    language_code: str
) -> dict[str, str]:
    """
    Wetterbezogene UI Texte.
    """


    translations = {

        "de": {

            "temperature": "🌡️ Temperatur",

            "feels_like": "🤗 Gefühlt",

            "minimum": "⬇️ Minimum",

            "maximum": "⬆️ Maximum",

            "humidity": "💧 Luftfeuchtigkeit",

            "pressure": "🔽 Luftdruck",

            "wind": "💨 Wind",

            "visibility": "👁️ Sichtweite",

            "clouds": "☁️ Bewölkung",

            "description": "📝 Wetterbeschreibung",

            "prediction": "🤖 ML Vorhersage"

        },


        "en": {

            "temperature": "🌡️ Temperature",

            "feels_like": "🤗 Feels like",

            "minimum": "⬇️ Minimum",

            "maximum": "⬆️ Maximum",

            "humidity": "💧 Humidity",

            "pressure": "🔽 Pressure",

            "wind": "💨 Wind",

            "visibility": "👁️ Visibility",

            "clouds": "☁️ Clouds",

            "description": "📝 Weather description",

            "prediction": "🤖 ML Prediction"

        },


        "fr": {

            "temperature": "🌡️ Température",

            "feels_like": "🤗 Ressenti",

            "minimum": "⬇️ Minimum",

            "maximum": "⬆️ Maximum",

            "humidity": "💧 Humidité",

            "pressure": "🔽 Pression",

            "wind": "💨 Vent",

            "visibility": "👁️ Visibilité",

            "clouds": "☁️ Nuages",

            "description": "📝 Description météo",

            "prediction": "🤖 Prédiction ML"

        }

    }


    return translations.get(

        language_code,

        translations["de"]

    )



def get_ui_texts(
    language_code: str
) -> dict[str, str]:
    """
    Allgemeine UI Texte.
    """


    translations = {

        "de": {

            "title":
                "🌤️ Weather App",

            "subtitle":
                "Aktuelle Wetterdaten über das FastAPI Backend.",

            "search":
                "Suchmethode auswählen:",

            "city":
                "Stadt",

            "coordinates":
                "Koordinaten",

            "city_input":
                "Stadt eingeben",

            "latitude":
                "Breitengrad",

            "longitude":
                "Längengrad",

            "button":
                "🌍 Wetter abrufen",

            "error":
                "Fehler"

        },


        "en": {

            "title":
                "🌤️ Weather App",

            "subtitle":
                "Current weather data via FastAPI backend.",

            "search":
                "Select search method:",

            "city":
                "City",

            "coordinates":
                "Coordinates",

            "city_input":
                "Enter city",

            "latitude":
                "Latitude",

            "longitude":
                "Longitude",

            "button":
                "🌍 Get weather",

            "error":
                "Error"

        },


        "fr": {

            "title":
                "🌤️ Weather App",

            "subtitle":
                "Données météo via backend FastAPI.",

            "search":
                "Choisir méthode:",

            "city":
                "Ville",

            "coordinates":
                "Coordonnées",

            "city_input":
                "Entrer une ville",

            "latitude":
                "Latitude",

            "longitude":
                "Longitude",

            "button":
                "🌍 Obtenir météo",

            "error":
                "Erreur"

        }

    }


    return translations.get(

        language_code,

        translations["de"]

    )


# ======================================================
# Wetteranzeige
# ======================================================


def display_weather(
    weather_response: WeatherResponse,
    language_code: str
) -> None:
    """
    Darstellung der Wetterdaten.
    """


    texts = get_weather_texts(
        language_code
    )


    location = (
        weather_response.location
    )


    weather = (
        weather_response.weather
    )



    # --------------------------------------------------
    # Kopfbereich
    # --------------------------------------------------


    col_icon, col_location, col_temperature = st.columns(
        [1, 2, 2]
    )



    with col_icon:

        if weather.icon:

            icon_url = (

                "https://openweathermap.org/img/wn/"

                f"{weather.icon}@2x.png"

            )


            st.image(
                icon_url,
                width=80
            )



    with col_location:

        st.subheader(
            f"📍 {location.city}"
        )


        if location.country:

            st.caption(
                location.country
            )


        st.write(
            weather.description.capitalize()
        )



    with col_temperature:

        st.metric(

            label=texts["temperature"],

            value=f"{weather.temperature:.1f} °C"

        )



    st.divider()



    # --------------------------------------------------
    # Temperatur Details
    # --------------------------------------------------


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(

            label=texts["feels_like"],

            value=f"{weather.feels_like:.1f} °C"

        )



    with col2:

        st.metric(

            label=texts["minimum"],

            value=f"{weather.minimum:.1f} °C"

        )



    with col3:

        st.metric(

            label=texts["maximum"],

            value=f"{weather.maximum:.1f} °C"

        )



    st.divider()



    # --------------------------------------------------
    # Wetter Details
    # --------------------------------------------------


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(

            label=texts["humidity"],

            value=f"{weather.humidity} %"

        )



    with col2:

        st.metric(

            label=texts["pressure"],

            value=f"{weather.pressure} hPa"

        )



    with col3:

        st.metric(

            label=texts["wind"],

            value=f"{weather.wind_speed:.1f} m/s"

        )



    st.divider()



    # --------------------------------------------------
    # Zusatzinformationen
    # --------------------------------------------------


    col1, col2 = st.columns(2)



    with col1:

        visibility_km = (

            weather.visibility / 1000

        )


        st.metric(

            label=texts["visibility"],

            value=f"{visibility_km:.1f} km"

        )



    with col2:

        st.metric(

            label=texts["clouds"],

            value=f"{weather.clouds} %"

        )



    st.divider()



    # --------------------------------------------------
    # Beschreibung
    # --------------------------------------------------


    st.subheader(
        texts["description"]
    )


    st.success(

        weather.description.capitalize()

    )


# ======================================================
# ML Prediction Anzeige
# ======================================================


def display_prediction(
    prediction: PredictionData | None,
    language_code: str
) -> None:
    """
    Darstellung der ML Prediction.
    """


    if prediction is None:

        return



    texts = get_weather_texts(
        language_code
    )



    st.divider()



    st.subheader(
        texts["prediction"]
    )



    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(

            label="Vorhersage",

            value=f"{prediction.value:.2f}"

        )



    with col2:

        st.info(

            f"""
**Modell**

{prediction.model_name}
"""

        )



    with col3:

        features = (

            ", ".join(
                prediction.features_used
            )

            if prediction.features_used

            else "-"

        )


        st.info(

            f"""
**Features**

{features}
"""

        )



# ======================================================
# Wetter abrufen
# ======================================================


def fetch_weather_data(
    search_type: str,
    city: str | None,
    latitude: float | None,
    longitude: float | None,
    language_code: str
) -> WeatherResponse:
    """
    Ruft Wetterdaten über Backend ab.
    """


    if search_type == "city":


        if not city:

            raise ValueError(
                "Bitte Stadt eingeben."
            )


        return get_weather(

            city.strip(),

            language_code

        )



    if search_type == "coordinates":


        if latitude is None or longitude is None:

            raise ValueError(
                "Bitte Koordinaten eingeben."
            )


        if not validate_coordinates(
            latitude,
            longitude
        ):

            raise ValueError(
                "Ungültige Koordinaten."
            )


        return get_weather_by_coordinates(

            latitude,

            longitude,

            language_code

        )



    raise ValueError(
        "Unbekannte Suchmethode."
    )



# ======================================================
# Koordinaten Validierung
# ======================================================


def validate_coordinates(
    latitude: float,
    longitude: float
) -> bool:
    """
    Prüft geografische Koordinaten.
    """


    return (

        -90 <= latitude <= 90

        and

        -180 <= longitude <= 180

    )



# ======================================================
# Hauptprogramm
# ======================================================


def main() -> None:
    """
    Startpunkt der Streamlit Anwendung.
    """

    # --------------------------------------------------
    # Streamlit Konfiguration
    # --------------------------------------------------

    st.set_page_config(

        page_title=PAGE_TITLE,

        page_icon=PAGE_ICON,

        layout=LAYOUT

    )



    # --------------------------------------------------
    # Sprache initialisieren
    # --------------------------------------------------

    if "language" not in st.session_state:

        st.session_state.language = DEFAULT_LANGUAGE



    language_code = st.session_state.language



    texts = get_ui_texts(
        language_code
    )



    # --------------------------------------------------
    # Kopfbereich
    # --------------------------------------------------

    col_title, col_language = st.columns(
        [5, 2]
    )



    with col_title:

        st.title(
            texts["title"]
        )



    with col_language:

        language_code = render_language_selector()



    texts = get_ui_texts(
        language_code
    )



    st.write(
        texts["subtitle"]
    )



    st.divider()



    # --------------------------------------------------
    # Suchmethode
    # --------------------------------------------------

    search_options = {

        "city": texts["city"],

        "coordinates": texts["coordinates"]

    }



    selected_mode = st.radio(

        texts["search"],

        options=list(
            search_options.values()
        ),

        horizontal=True

    )



    search_type = next(

        key

        for key, value

        in search_options.items()

        if value == selected_mode

    )



    city = None

    latitude = None

    longitude = None



    # --------------------------------------------------
    # Eingabe
    # --------------------------------------------------

    if search_type == "city":


        city = st.text_input(

            texts["city_input"],

            placeholder="Berlin"

        )



    else:


        col_lat, col_lon = st.columns(2)



        with col_lat:


            latitude = st.number_input(

                texts["latitude"],

                value=float(
                    DEFAULT_LATITUDE
                ),

                format="%.4f"

            )



        with col_lon:


            longitude = st.number_input(

                texts["longitude"],

                value=float(
                    DEFAULT_LONGITUDE
                ),

                format="%.4f"

            )



    st.divider()



    # --------------------------------------------------
    # Abrufen
    # --------------------------------------------------

    if st.button(

        texts["button"]

    ):


        try:


            weather_data = fetch_weather_data(

                search_type,

                city,

                latitude,

                longitude,

                language_code

            )


            display_weather(

                weather_data,

                language_code

            )


            display_prediction(

                weather_data.prediction,

                language_code

            )



        except CityNotFoundError as error:


            st.error(

                f"❌ {error}"

            )



        except InvalidAPIKeyError as error:


            st.error(

                f"🔑 {error}"

            )



        except BackendConnectionError as error:


            st.error(

                f"🔌 {error}"

            )



        except BackendTimeoutError as error:


            st.error(

                f"⏱️ {error}"

            )



        except BackendAPIError as error:


            st.error(

                f"⚠️ {error}"

            )



        except ValueError as error:


            st.warning(

                str(error)

            )



        except Exception as error:


            st.exception(
                error
            )



# ======================================================
# Start
# ======================================================


if __name__ == "__main__":

    main()