"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Stops all platform services.
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

from scripts.stop_backend import stop_backend
from scripts.stop_streamlit import stop_streamlit


def stop_all() -> None:

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Stopping Services")
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