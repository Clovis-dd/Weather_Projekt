"""
pipeline.py

Zentrale Training Pipeline.

Verantwortlichkeiten:

- Dataset vorbereiten
- Features validieren
- Feature Engineering anwenden
- Training vorbereiten
"""


from __future__ import annotations


import pandas as pd


from shared.feature_validator import (
    validate_feature_schema,
)


from shared.feature_schema import (
    FEATURES,
)


from shared.logger import get_logger



logger = get_logger(
    __name__
)



class TrainingPipeline:
    """
    Training Feature Pipeline.

    Verantwortlich für:

    - Feature Validierung
    - Feature Engineering
    - finale Feature Auswahl
    """


    def __init__(self):

        self.logger = get_logger(
            __name__
        )



    def prepare_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Erstellt finale ML Features.
        """

        self.logger.info(
            "Preparing ML features"
        )


        required = [

            "temperature",

            "feels_like",

            "humidity",

            "pressure",

            "wind_speed",

            "clouds",

            "visibility",

        ]



        missing = [

            column

            for column in required

            if column not in dataframe.columns

        ]



        if missing:

            raise ValueError(
                f"Missing input columns: {missing}"
            )



        engineered = dataframe[
            required
        ].copy()



        # -----------------------------
        # Feature Engineering
        # -----------------------------


        engineered[
            "temperature_difference"
        ] = (
            engineered["temperature"]
            -
            engineered["feels_like"]
        )



        engineered[
            "wind_factor"
        ] = (
            engineered["wind_speed"]
            *
            engineered["clouds"]
            /
            100
        )



        engineered[
            "humidity_factor"
        ] = (
            engineered["humidity"]
            /
            100
        )



        # -----------------------------
        # Finale Feature Auswahl
        # -----------------------------


        final_features = engineered.loc[
            :,
            list(FEATURES)
        ]



        validate_feature_schema(
            final_features.columns
        )

        self.logger.info(
            "ML feature preparation completed columns=%s",
            list(
                final_features.columns
            ),
        )



        return final_features