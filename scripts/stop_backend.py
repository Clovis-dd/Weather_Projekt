"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Stops the FastAPI backend.
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

import psutil

from shared.logger import get_logger


logger = get_logger(__name__)


def stop_backend() -> None:

    logger.info("Stopping FastAPI backend...")

    stopped = False

    for process in psutil.process_iter(["pid", "name", "cmdline"]):

        try:

            cmdline = " ".join(process.info["cmdline"] or [])

            if "backend.api:app" in cmdline or "uvicorn" in cmdline:

                process.terminate()

                print(f"Stopped backend (PID {process.pid})")

                stopped = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            pass

    if not stopped:

        print("Backend is not running.")


if __name__ == "__main__":
    stop_backend()