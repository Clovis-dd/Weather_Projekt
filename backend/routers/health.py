"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers.health

Description:
    Health-, Monitoring- und Systemendpunkte
    der FastAPI-Anwendung.

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

from fastapi import APIRouter


# ======================================================
# Project Imports
# ======================================================

from backend.dependencies import (
    model_information_service,
)

from backend.prediction_monitor import (
    prediction_monitor,
)


# ======================================================
# Router Configuration
# ======================================================

router = APIRouter(
    prefix="",
    tags=["System"],
)


APPLICATION_START_TIME = datetime.now(UTC)



# ======================================================
# Root Endpoint
# ======================================================


@router.get(
    "/",
    summary="API Information",
)
def get_api_information() -> dict[str, str]:
    """
    Returns general API information.
    """

    return {
        "service": "Weather ML API",
        "application": (
            "Weather Analytics "
            "& Machine Learning Platform"
        ),
        "version": "1.0.0",
        "status": "running",
    }



# ======================================================
# Health Endpoint
# ======================================================


@router.get(
    "/health",
    summary="Health Check",
)
def get_health_status() -> dict[str, Any]:
    """
    Returns API and model health information.
    """

    champion = (
        model_information_service
        .get_champion()
    )


    return {

        "status": "ok",

        "service": (
            "Weather ML API"
        ),

        "version": (
            "1.0.0"
        ),

        "model_loaded": (
            champion is not None
        ),

        "active_model": (
            champion.name
            if champion
            else None
        ),

        "feature_schema_version": (
            champion.feature_schema_version
            if champion
            else None
        ),

        "prediction_count": (
            prediction_monitor
            .get_metrics()
            .get(
                "predictions_total",
                0,
            )
        ),

        "utc_time": datetime.now(
            UTC
        ),
    }



# ======================================================
# Metrics Endpoint
# ======================================================


@router.get(
    "/metrics",
    summary="Prediction Metrics",
)
def get_prediction_metrics() -> dict[str, Any]:
    """
    Returns prediction monitoring metrics.
    """

    return (
        prediction_monitor
        .get_metrics()
    )



# ======================================================
# Model Endpoint
# ======================================================


@router.get(
    "/model",
    summary="Champion Model",
)
def get_model_information() -> dict[str, Any]:
    """
    Returns information about
    the active ML model.
    """

    return (
        model_information_service
        .get_model_information()
    )



# ======================================================
# Runtime Endpoint
# ======================================================


@router.get(
    "/runtime",
    summary="Application Runtime",
)
def get_runtime_information() -> dict[str, Any]:
    """
    Returns application runtime.
    """

    uptime = (
        datetime.now(UTC)
        -
        APPLICATION_START_TIME
    )


    return {

        "started_at": (
            APPLICATION_START_TIME
            .isoformat()
        ),

        "uptime_seconds": (
            int(
                uptime.total_seconds()
            )
        ),

    }