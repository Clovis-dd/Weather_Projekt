"""
feature_engineering.py

Zentrale Feature-Erzeugung für das Wettermodell.

Input:
    pandas DataFrame mit Rohdaten

Output:
    pandas DataFrame mit ML Features
"""


from __future__ import annotations


import pandas as pd


from shared.logger import get_logger


logger = get_logger(
    __name__
)



def engineer_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Erstellt zusätzliche ML Features.

    Gibt immer einen DataFrame zurück.
    """


    if not isinstance(
        dataframe,
        pd.DataFrame,
    ):
        raise TypeError(
            "engineer_features expects pandas DataFrame"
        )


    engineered = dataframe.copy()



    # ----------------------------------------------
    # Temperatur Differenz
    # ----------------------------------------------

    if (
        "temperature" in engineered.columns
        and
        "feels_like" in engineered.columns
    ):

        engineered[
            "temperature_difference"
        ] = (
            engineered["temperature"]
            -
            engineered["feels_like"]
        )



    # ----------------------------------------------
    # Wind Faktor
    # ----------------------------------------------

    if "wind_speed" in engineered.columns:

        engineered[
            "wind_factor"
        ] = (
            engineered["wind_speed"]
            *
            1.0
        )



    # ----------------------------------------------
    # Feuchtigkeit Faktor
    # ----------------------------------------------

    if "humidity" in engineered.columns:

        engineered[
            "humidity_factor"
        ] = (
            engineered["humidity"]
            /
            100.0
        )



    logger.debug(
        "Feature engineering completed columns=%s",
        list(engineered.columns),
    )


    return engineered