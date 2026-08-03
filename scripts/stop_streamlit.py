"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Stops the Streamlit dashboard.
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

import psutil

from shared.logger import get_logger


logger = get_logger(__name__)


def stop_streamlit() -> None:

    logger.info("Stopping Streamlit dashboard...")

    stopped = False

    for process in psutil.process_iter(["pid", "name", "cmdline"]):

        try:

            cmdline = " ".join(process.info["cmdline"] or [])

            if "streamlit" in cmdline:

                process.terminate()

                print(f"Stopped Streamlit (PID {process.pid})")

                stopped = True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            pass

    if not stopped:

        print("Streamlit is not running.")


if __name__ == "__main__":
    stop_streamlit()