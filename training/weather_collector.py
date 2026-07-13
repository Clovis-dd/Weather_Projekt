"""
weather_collector.py

Erzeugt Trainingsdaten für das ML-Modell.

Quelle:
OpenWeatherMap API

Ausgabe:

data/weather_history.csv
"""


from __future__ import annotations


from datetime import UTC, datetime

from pathlib import Path

import csv



from backend.weather_service import WeatherService


from shared.logger import get_logger


from shared.weather_model import (
    FEATURES,
    TARGET_NAME,
)



logger = get_logger(
    __name__
)



DATA_DIR = Path(
    "data"
)


DATA_FILE = (
    DATA_DIR /
    "weather_history.csv"
)



CITIES = [

    "Berlin",
    "Hamburg",
    "München",
    "Köln",
    "Frankfurt",
    "Stuttgart",
    "Düsseldorf",
    "Leipzig",
    "Dresden",

    "Paris",
    "London",
    "Amsterdam",
    "Brüssel",
    "Rom",
    "Madrid",
    "Wien",
    "Prag",
    "Zürich",

]



HEADERS = [

    "timestamp",

    "city",

    "country",

    *FEATURES,

    TARGET_NAME,

]



service = WeatherService()



# ======================================================
# Target Berechnung
# ======================================================


def calculate_weather_score(
    weather: dict,
) -> float:
    """
    Erzeugt künstliche Zielvariable.

    Diese Version dient als
    Startpunkt für supervised learning.
    """


    score = 100.0


    temperature = weather["temperature"]

    humidity = weather["humidity"]

    wind = weather["wind_speed"]

    clouds = weather["clouds"]



    score -= abs(
        22 - temperature
    ) * 2



    score -= max(

        humidity - 60,

        0

    ) * 0.4



    score -= wind * 1.2


    score -= clouds * 0.15



    return round(

        max(

            0,

            min(

                100,

                score

            )

        ),

        2

    )



# ======================================================
# Collection
# ======================================================


def collect_city(
    city: str,
) -> None:
    """
    Sammelt Wetterdaten einer Stadt.
    """


    raw = service.get_weather_by_city(
        city
    )


    parsed = service.parse_weather_data(
        raw
    )


    weather = parsed.weather



    row = {


        "timestamp":

            datetime.now(
                UTC
            ).isoformat(),



        "city":

            parsed.location.city,



        "country":

            parsed.location.country,



        "temperature":

            weather.temperature,



        "feels_like":

            weather.feels_like,



        "humidity":

            weather.humidity,



        "pressure":

            weather.pressure,



        "wind_speed":

            weather.wind_speed,



        "clouds":

            weather.clouds,



        "visibility":

            weather.visibility,



        TARGET_NAME:

            calculate_weather_score(

                weather.model_dump()

            )

    }



    file_exists = DATA_FILE.exists()



    with DATA_FILE.open(

        "a",

        newline="",

        encoding="utf-8",

    ) as file:



        writer = csv.DictWriter(

            file,

            fieldnames=HEADERS,

        )



        if not file_exists:

            writer.writeheader()



        writer.writerow(
            row
        )



    logger.info(

        "Collected city=%s",

        city

    )



# ======================================================
# Main
# ======================================================


def main():

    DATA_DIR.mkdir(
        exist_ok=True
    )


    for city in CITIES:

        try:

            collect_city(
                city
            )


        except Exception:

            logger.exception(

                "Collection failed city=%s",

                city

            )



if __name__ == "__main__":

    main()