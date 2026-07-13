"""
weather_service.py

Kommunikation mit der OpenWeatherMap API.

Verantwortlichkeiten:

- Wetterdaten abrufen
- API Fehler behandeln
- OpenWeatherMap Response normalisieren
- WeatherResponse erzeugen
"""


from datetime import UTC, datetime
from typing import Any, Final


import requests


from shared.models import (
    LocationData,
    WeatherData,
    WeatherResponse,
    SunData
)


from shared.config import settings
from shared.logger import get_logger



logger = get_logger(
    __name__
)



# ======================================================
# Exceptions
# ======================================================


class WeatherAPIError(Exception):
    """
    Allgemeiner Fehler der Wetter API.
    """



class CityNotFoundError(
    WeatherAPIError
):
    """
    Stadt nicht gefunden.
    """



class InvalidAPIKeyError(
    WeatherAPIError
):
    """
    Ungültiger OpenWeatherMap API Key.
    """



# ======================================================
# Service
# ======================================================


class WeatherService:
    """
    Service für OpenWeatherMap Kommunikation.
    """


    BASE_URL: Final[str] = (
        "https://api.openweathermap.org/data/2.5/weather"
    )



    def __init__(self) -> None:

        self.session = requests.Session()



    # ==================================================
    # City
    # ==================================================


    def get_weather_by_city(
        self,
        city: str,
        language: str = "de"
    ) -> dict[str, Any]:
        """
        Holt Wetterdaten über Stadtname.
        """


        params = {

            "q": city,

            "appid": settings.OWM_API_KEY,

            "units": "metric",

            "lang": language

        }


        logger.info(
            "Weather request city=%s language=%s",
            city,
            language
        )


        return self._request_weather(
            params
        )



    # ==================================================
    # Coordinates
    # ==================================================


    def get_weather_by_coordinates(
        self,
        latitude: float,
        longitude: float,
        language: str = "de"
    ) -> dict[str, Any]:
        """
        Holt Wetterdaten über Koordinaten.
        """


        params = {

            "lat": latitude,

            "lon": longitude,

            "appid": settings.OWM_API_KEY,

            "units": "metric",

            "lang": language

        }


        logger.info(
            "Weather request lat=%s lon=%s",
            latitude,
            longitude
        )


        return self._request_weather(
            params
        )



    # ==================================================
    # HTTP Request
    # ==================================================


    def _request_weather(
        self,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Führt Request an OpenWeatherMap aus.
        """


        if not settings.OWM_API_KEY:

            raise InvalidAPIKeyError(
                "OpenWeatherMap API-Key fehlt."
            )



        try:

            response = self.session.get(

                self.BASE_URL,

                params=params,

                timeout=settings.REQUEST_TIMEOUT

            )



            logger.info(
                "OWM response status=%s",
                response.status_code
            )



            if response.status_code == 401:

                raise InvalidAPIKeyError(
                    "OpenWeatherMap API-Key ungültig."
                )



            if response.status_code == 404:

                raise CityNotFoundError(
                    "Ort nicht gefunden."
                )



            response.raise_for_status()



            return response.json()



        except requests.exceptions.Timeout as error:


            logger.error(
                "OpenWeatherMap Timeout."
            )


            raise WeatherAPIError(
                "Timeout bei OpenWeatherMap."
            ) from error



        except requests.exceptions.ConnectionError as error:


            logger.error(
                "OpenWeatherMap nicht erreichbar."
            )


            raise WeatherAPIError(
                "Keine Verbindung zu OpenWeatherMap."
            ) from error



        except requests.exceptions.RequestException as error:


            logger.exception(
                "OpenWeatherMap Request Fehler."
            )


            raise WeatherAPIError(
                "Fehler bei OpenWeatherMap Kommunikation."
            ) from error



    # ==================================================
    # Parser
    # ==================================================


    @staticmethod
    def parse_weather_data(
        data: dict[str, Any],
        language: str = "de"
    ) -> WeatherResponse:
        """
        Wandelt OpenWeatherMap Daten
        in internes Response Modell um.
        """


        weather_info = (
            data.get(
                "weather",
                [{}]
            )[0]
        )


        main = data.get(
            "main",
            {}
        )


        wind = data.get(
            "wind",
            {}
        )


        clouds = data.get(
            "clouds",
            {}
        )


        coordinates = data.get(
            "coord",
            {}
        )


        system = data.get(
            "sys",
            {}
        )



        sun = SunData(

            sunrise=(
                datetime.fromtimestamp(
                    system["sunrise"],
                    UTC
                )
                if system.get("sunrise")
                else None
            ),


            sunset=(
                datetime.fromtimestamp(
                    system["sunset"],
                    UTC
                )
                if system.get("sunset")
                else None
            )

        )



        response = WeatherResponse(


            location=LocationData(

                city=data.get(
                    "name",
                    "Unbekannt"
                ),


                country=system.get(
                    "country",
                    "-"
                ),


                latitude=coordinates.get(
                    "lat",
                    0
                ),


                longitude=coordinates.get(
                    "lon",
                    0
                )

            ),



            weather=WeatherData(


                weather_id=weather_info.get(
                    "id"
                ),


                temperature=main.get(
                    "temp",
                    0
                ),


                feels_like=main.get(
                    "feels_like",
                    0
                ),


                minimum=main.get(
                    "temp_min",
                    0
                ),


                maximum=main.get(
                    "temp_max",
                    0
                ),


                humidity=main.get(
                    "humidity",
                    0
                ),


                pressure=main.get(
                    "pressure",
                    0
                ),


                wind_speed=wind.get(
                    "speed",
                    0
                ),


                wind_direction=wind.get(
                    "deg",
                    0
                ),


                visibility=data.get(
                    "visibility",
                    0
                ),


                clouds=clouds.get(
                    "all",
                    0
                ),


                description=weather_info.get(
                    "description",
                    "-"
                ),


                icon=weather_info.get(
                    "icon",
                    ""
                )

            ),



            sun=sun,


            timestamp=datetime.now(
                UTC
            ),


            language=language

        )



        logger.info(
            "Weather parsed city=%s",
            response.location.city
        )


        return response