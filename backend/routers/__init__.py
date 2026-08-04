"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.routers

Beschreiung:
    Dieses Paket enthält alle FastAPI-Router der Anwendung.

Jeder Router kapselt einen fachlichen Bereich
(z. B. Weather, Prediction oder History).

Die Router werden zentral in backend.api registriert.
"""

from .health import router as health_router
from .weather import router as weather_router
from .prediction import router as prediction_router
from .history import router as history_router
from .model import router as model_router

__all__ = [
    "health_router",
    "weather_router",
    "prediction_router",
    "history_router",
    "model_router",
]