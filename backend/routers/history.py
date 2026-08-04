"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers.history

Description:
    REST-Endpunkte für gespeicherte Wetter-
    und Prediction-Historien.

Responsibilities:

    - historische Predictions abrufen
    - Repository verwenden
    - Datenbankzugriff kapseln

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations


# ======================================================
# Standard Library
# ======================================================

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

from backend.database import SessionLocal

from backend.repository import WeatherRepository

from shared.logger import get_logger



# ======================================================
# Router Configuration
# ======================================================

router = APIRouter(

    prefix="/history",

    tags=["Prediction History"],

)



# ======================================================
# Logger
# ======================================================

logger = get_logger(
    __name__
)



# ======================================================
# History Endpoints
# ======================================================


@router.get(
    "",
    summary="Prediction History",
    description=(
        "Returns all stored weather predictions."
    ),
)
def get_history() -> list[dict[str, Any]]:
    """
    Returns complete prediction history.
    """

    session = SessionLocal()


    try:

        repository = WeatherRepository(
            session
        )


        records = repository.get_all()


        return [

            record.to_dict()

            for record in records

        ]


    finally:

        session.close()



# ======================================================


@router.get(
    "/latest",
    summary="Latest Prediction",
    description=(
        "Returns the latest stored prediction."
    ),
)
def get_latest_history() -> dict[str, Any]:
    """
    Returns newest prediction entry.
    """

    session = SessionLocal()


    try:

        repository = WeatherRepository(
            session
        )


        record = repository.get_latest()


        if record is None:

            raise HTTPException(

                status_code=404,

                detail=(
                    "No prediction history available."
                ),

            )


        return record.to_dict()


    finally:

        session.close()



# ======================================================


@router.get(
    "/{history_id}",
    summary="Prediction By ID",
    description=(
        "Returns a prediction history entry "
        "by identifier."
    ),
)
def get_history_by_id(
    history_id: int,
) -> dict[str, Any]:
    """
    Returns prediction history entry.
    """

    session = SessionLocal()


    try:

        repository = WeatherRepository(
            session
        )


        record = repository.get_by_id(
            history_id
        )


        if record is None:

            raise HTTPException(

                status_code=404,

                detail=(
                    "Prediction not found."
                ),

            )


        return record.to_dict()


    finally:

        session.close()