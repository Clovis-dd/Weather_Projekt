"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    stop_all.py

Description:
    Stops all running platform services.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()

from shared.logger import get_logger

from scripts.stop_backend import stop_backend
from scripts.stop_streamlit import stop_streamlit


logger = get_logger(__name__)


def stop_all() -> None:
    """
    Stop all platform services.
    """

    logger.info(
        "Stopping all services..."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Stop Services")
    print("========================================")

    print()

    stop_backend()

    stop_streamlit()

    print()

    print("========================================")
    print(" All services stopped.")
    print("========================================")

    print()


if __name__ == "__main__":
    stop_all()