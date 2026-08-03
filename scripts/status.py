"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    status.py

Description:
    Displays the current status of the application services.

Checks
------
- FastAPI Backend
- Streamlit Dashboard

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

from urllib.request import urlopen
from urllib.error import URLError

from shared.config import settings


BACKEND_URL = f"http://{settings.HOST}:{settings.PORT}/health"
FRONTEND_URL = "http://localhost:8501"


def service_online(url: str) -> bool:
    """
    Returns True if the given service is reachable.
    """

    try:

        with urlopen(url, timeout=2):

            return True

    except URLError:

        return False

    except Exception:

        return False


def print_status(name: str, online: bool) -> None:
    """
    Print a formatted service status.
    """

    icon = "🟢" if online else "🔴"

    state = "ONLINE" if online else "OFFLINE"

    print(f"{icon} {name:<20} {state}")


def main() -> None:

    backend_online = service_online(BACKEND_URL)

    frontend_online = service_online(FRONTEND_URL)

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Service Status")
    print("========================================")

    print_status(
        "FastAPI Backend",
        backend_online,
    )

    print_status(
        "Streamlit Dashboard",
        frontend_online,
    )

    print("========================================")

    print()


if __name__ == "__main__":
    main()