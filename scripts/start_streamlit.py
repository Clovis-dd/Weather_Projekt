"""
start_streamlit.py

Startet den Streamlit-Server für die Weather App.
"""
from __future__ import annotations

"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    start_streamlit.py

Description:
    Starts the Streamlit dashboard.

Author:
    Clovis Wassom Leugoué
"""

import subprocess
import sys

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()

from shared.logger import get_logger


logger = get_logger(__name__)


FRONTEND_APP = PROJECT_ROOT / "frontend" / "app.py"


def start_streamlit() -> None:
    """
    Start the Streamlit dashboard.
    """

    logger.info(
        "Starting Streamlit dashboard..."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Streamlit Dashboard")
    print("========================================")
    print("URL : http://localhost:8501")
    print("========================================")

    print()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(FRONTEND_APP),
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


if __name__ == "__main__":
    start_streamlit()
initialize()


from streamlit.web.cli import main


sys.argv = [
    "streamlit",
    "run",
    "frontend/app.py",
]


main()