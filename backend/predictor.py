"""
predictor.py

Production Prediction Service.

Verantwortlichkeiten:

- Eingabedaten entgegennehmen
- Features vorbereiten
- aktives Modell laden
- Prediction durchführen
- Ergebnis standardisieren
"""


from __future__ import annotations

from backend.prediction_monitor import prediction_monitor

from pathlib import Path

from typing import Any

import time

import pandas as pd


from backend.model_service import ModelService


from shared.feature_schema import (
    FEATURE_SCHEMA_VERSION,
)


from training.pipeline import (
    TrainingPipeline,
)


from shared.logger import (
    get_logger,
)



logger = get_logger(
    __name__
)



DEFAULT_MODELS_DIR = Path(
    "models"
)



class WeatherPredictor:
    """
    Produktions Predictor.

    Nutzt ausschließlich das Champion Modell.
    """

    def __init__(
            self,
            models_dir: Path = Path("models"),
    ) -> None:
        self.models_dir = (
                models_dir
                or DEFAULT_MODELS_DIR
        )

        self.model_service = ModelService(
            models_dir
        )

        self.pipeline = TrainingPipeline()

    def prepare_features(
            self,
            dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Erstellt ML Features.
        """

        logger.info(
            "Preparing prediction features"
        )

        features = self.pipeline.prepare_features(
            dataframe
        )

        return features



    def predict(
        self,
        weather_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Erstellt Wettervorhersage.
        """



        logger.info(
            "Prediction started"
        )



        dataframe = pd.DataFrame(
            [
                weather_data
            ]
        )



        features = self.prepare_features(
            dataframe
        )



        model = self.model_service.get_model()

        champion = (
            self.model_service
            .get_champion()
        )


        start_time = time.perf_counter()

        try:

            prediction = model.predict(
                features
            )

            latency_ms = (
                                 time.perf_counter()
                                 -
                                 start_time
                         ) * 1000

            prediction_monitor.record_success(
                latency_ms=latency_ms,
                model_name=(
                    champion.name
                    if champion
                    else "unknown"
                ),
            )


        except Exception:

            prediction_monitor.record_error()

            raise



        predicted_value = float(
            prediction[0]
        )



        result = {

            "prediction":
                predicted_value,


            "model":
                champion.name
                if champion
                else None,


            "feature_schema_version":
                FEATURE_SCHEMA_VERSION,

        }



        logger.info(
            "Prediction completed result=%s",
            result,
        )


        return result