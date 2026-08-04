"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.api

Description:
    FastAPI Application Entry Point.

Responsibilities:

    - create FastAPI application
    - configure middleware
    - register routers

Business logic is handled by routers and services.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations


from fastapi import FastAPI


from backend.middleware import RequestIDMiddleware


from backend.routers import (
    health_router,
    weather_router,
    prediction_router,
    history_router,
    model_router,
)


from shared.logger import get_logger



# ======================================================
# Logger
# ======================================================


logger = get_logger(
    __name__
)



# ======================================================
# Application
# ======================================================


app = FastAPI(

    title=(
        "Weather Analytics "
        "& Machine Learning Platform"
    ),

    description=(
        "Production-oriented "
        "weather analytics platform "
        "with machine learning prediction."
    ),

    version="1.0.0",

)



# ======================================================
# Middleware
# ======================================================


app.add_middleware(
    RequestIDMiddleware
)



# ======================================================
# Router Registration
# ======================================================


app.include_router(
    health_router
)


app.include_router(
    weather_router
)


app.include_router(
    prediction_router
)


app.include_router(
    history_router
)


app.include_router(
    model_router
)



logger.info(
    "Weather Analytics API started"
)