"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    start_backend.py

Description:
    Starts the FastAPI backend server.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

import uvicorn

from shared.config import settings
from shared.logger import get_logger


logger = get_logger(__name__)


def start_backend() -> None:
    """
    Start the FastAPI backend server.
    """

    logger.info(
        "Starting FastAPI backend..."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" FastAPI Backend")
    print("========================================")
    print(f"Host : {settings.HOST}")
    print(f"Port : {settings.PORT}")
    print("========================================")
    print()

    uvicorn.run(
        "backend.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    start_backend()