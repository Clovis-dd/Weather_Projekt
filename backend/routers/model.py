"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers.model

Description:
    REST-Endpunkt für Informationen über das aktive
    Machine Learning Modell.

Responsibilities:

    - Modellinformationen bereitstellen
    - Champion Modell anzeigen
    - Model Monitoring unterstützen


Architecture:

    Client
       |
       ↓
    FastAPI Router
       |
       ↓
    ModelInformationService


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

from fastapi import APIRouter


# ======================================================
# Project Imports
# ======================================================

from backend.dependencies import (
    model_information_service,
)


# ======================================================
# Router
# ======================================================

router = APIRouter(
    prefix="/model",
    tags=["Machine Learning"],
)


# ======================================================
# Model Information
# ======================================================


@router.get(
    "",
    summary="Champion Model Information",
    description=(
        "Returns information about the active "
        "Champion machine learning model."
    ),
)
def get_model_information() -> dict[str, Any]:
    """
    Returns active model metadata.
    """

    return (
        model_information_service
        .get_model_information()
    )