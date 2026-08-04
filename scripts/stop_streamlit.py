"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    stop_streamlit.py

Description:
    Stops the Streamlit dashboard.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

import psutil

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()

from shared.logger import get_logger


logger = get_logger(__name__)


def stop_streamlit() -> None:
    """
    Stop the Streamlit dashboard.
    """

    logger.info(
        "Stopping Streamlit dashboard..."
    )

    stopped = False

    for process in psutil.process_iter(["pid", "cmdline"]):

        try:

            command = " ".join(process.info["cmdline"] or [])

            if "streamlit" in command:

                process.terminate()

                print(
                    f"Stopped Streamlit (PID {process.pid})"
                )

                stopped = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            continue

    if not stopped:

        print(
            "Streamlit is not running."
        )


if __name__ == "__main__":
    stop_streamlit()