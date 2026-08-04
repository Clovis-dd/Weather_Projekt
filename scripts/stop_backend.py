"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    stop_backend.py

Description:
    Stops the FastAPI backend server.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

import psutil

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()

from shared.logger import get_logger


logger = get_logger(__name__)


def stop_backend() -> None:
    """
    Stop the FastAPI backend server.
    """

    logger.info(
        "Stopping FastAPI backend..."
    )

    stopped = False

    for process in psutil.process_iter(["pid", "cmdline"]):

        try:

            command = " ".join(process.info["cmdline"] or [])

            if (
                "uvicorn" in command
                or "backend.api:app" in command
            ):

                process.terminate()

                print(
                    f"Stopped backend (PID {process.pid})"
                )

                stopped = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            continue

    if not stopped:

        print(
            "Backend is not running."
        )


if __name__ == "__main__":
    stop_backend()