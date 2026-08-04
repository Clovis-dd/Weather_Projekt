"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.services.prediction_service

Description:
    Service Layer für Machine Learning Predictions.

Responsibilities:

    - ML Predictor kapseln
    - Feature Übergabe vorbereiten
    - Prediction Ergebnisse normalisieren
    - PredictionData erzeugen
    - Fehler und Laufzeitinformationen protokollieren

Architecture:

    Router
        |
        ↓
    PredictionService
        |
        ↓
    WeatherPredictor
        |
        ↓
    Champion Model


Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations


# ======================================================
# Standard Library
# ======================================================

from datetime import UTC, datetime
from typing import Any


# ======================================================
# Third Party
# ======================================================

# Keine externen Imports notwendig


# ======================================================
# Project Imports
# ======================================================

from backend.predictor import WeatherPredictor

from shared.logger import get_logger

from shared.models import (
    PredictionData,
    PredictionRequest,
)


# ======================================================
# Logger
# ======================================================

logger = get_logger(
    __name__
)


# ======================================================
# Service
# ======================================================


class PredictionService:
    """
    Service für Machine Learning Predictions.

    Kapselt die Kommunikation zwischen API Layer
    und ML Predictor.
    """


    def __init__(
        self,
        predictor: WeatherPredictor,
    ) -> None:
        """
        Initialisiert den Prediction Service.

        Args:
            predictor:
                Aktiver ML Predictor.
        """

        self.predictor = predictor



    # ==================================================
    # Create Prediction
    # ==================================================

    def create_prediction(
        self,
        request: PredictionRequest,
    ) -> PredictionData:
        """
        Erstellt eine ML Vorhersage.

        Args:
            request:
                Validierte Prediction Features.

        Returns:
            PredictionData:
                Standardisiertes Prediction Ergebnis.

        Raises:
            RuntimeError:
                Wenn die Prediction Pipeline fehlschlägt.
        """


        logger.info(
            "Creating ML prediction."
        )


        try:

            features: dict[str, Any] = (
                request.model_dump()
            )


            logger.debug(
                "Prediction features=%s",
                list(
                    features.keys()
                ),
            )


            result: dict[str, Any] = (
                self.predictor.predict(
                    features
                )
            )


            prediction = PredictionData(

                value=float(
                    result["prediction"]
                ),


                model_name=str(
                    result["model"]
                ),


                features_used=list(
                    features.keys()
                ),


                prediction_time=datetime.now(
                    UTC
                ),

            )


            logger.info(
                "Prediction created model=%s value=%s",
                prediction.model_name,
                prediction.value,
            )


            return prediction



        except Exception as error:

            logger.exception(
                "Prediction creation failed."
            )


            raise RuntimeError(
                "Prediction service failed."
            ) from error