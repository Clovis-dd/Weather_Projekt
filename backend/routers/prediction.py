"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers.prediction

Description:
    REST-Endpunkte für Machine Learning Predictions.

Responsibilities:

    - Prediction Requests entgegennehmen
    - Aktiven Predictor verwenden
    - Standardisierte Response liefern


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

from fastapi import (
    APIRouter,
    HTTPException,
)


# ======================================================
# Project Imports
# ======================================================

from backend import api

from shared.logger import get_logger

from shared.models import (
    PredictionRequest,
    PredictionResponse,
)


# ======================================================
# Router Configuration
# ======================================================

router = APIRouter(
    prefix="/predict",
    tags=["Machine Learning"],
)


# ======================================================
# Logger
# ======================================================

logger = get_logger(
    __name__
)


# ======================================================
# Endpoint
# ======================================================


@router.post(
    "",
    response_model=PredictionResponse,
    summary="Create ML Prediction",
    description=(
        "Creates a machine learning prediction "
        "using the active Champion model."
    ),
)
def create_prediction(
    request: PredictionRequest,
) -> PredictionResponse:
    """
    Creates a prediction using the active predictor.
    """


    logger.info(
        "Prediction request received"
    )


    try:

        result: dict[str, Any] = (
            api.predictor.predict(
                request.model_dump()
            )
        )


        return PredictionResponse(

            prediction=result["prediction"],

            model=result["model"],

            features_used=list(
                request.model_dump().keys()
            ),

            prediction_time=datetime.now(
                UTC
            ),

        )


    except Exception as error:

        logger.exception(
            "Prediction failed"
        )


        raise HTTPException(

            status_code=500,

            detail="Prediction service failed.",

        ) from error