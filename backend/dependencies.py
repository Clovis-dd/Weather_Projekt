"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.dependencies

Description:
    Zentrale Application Dependencies.

Responsibilities:

    - Service Instanzen zentral bereitstellen
    - Dependency Injection ermöglichen
    - Gemeinsame Komponenten verwalten


Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations


# ======================================================
# Standard Library
# ======================================================

from pathlib import Path


# ======================================================
# Project Imports
# ======================================================

from backend.predictor import WeatherPredictor

from backend.services.weather_service import (
    WeatherService,
)

from backend.services.prediction_service import (
    PredictionService,
)

from backend.services.model_service import (
    ModelInformationService,
)


# ======================================================
# Services
# ======================================================


weather_service = WeatherService()



predictor = WeatherPredictor(
    models_dir=Path("models"),
)



prediction_service = PredictionService(
    predictor=predictor,
)



model_service = ModelInformationService(
    models_directory=Path("models"),
)



# Alias für neue Architektur
model_information_service = model_service