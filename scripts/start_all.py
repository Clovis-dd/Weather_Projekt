"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    start_all.py

Description:
    Starts the complete application stack.

Services
--------
- FastAPI Backend
- Streamlit Frontend

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

import subprocess
import sys

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()


def start_backend() -> subprocess.Popen:
    """
    Start the FastAPI backend.
    """

    return subprocess.Popen(
        [
            sys.executable,
            "scripts/start_backend.py",
        ],
        cwd=PROJECT_ROOT,
    )


def start_frontend() -> subprocess.Popen:
    """
    Start the Streamlit frontend.
    """

    return subprocess.Popen(
        [
            sys.executable,
            "scripts/start_frontend.py",
        ],
        cwd=PROJECT_ROOT,
    )


def main() -> None:

    print()
    print("========================================")
    print(" Weather Analytics Platform")
    print(" Starting Application")
    print("========================================")

    backend = start_backend()

    frontend = start_frontend()

    print(f"Backend PID  : {backend.pid}")
    print(f"Frontend PID : {frontend.pid}")

    print()
    print("Backend")
    print("http://127.0.0.1:9000")

    print()

    print("Frontend")
    print("http://localhost:8501")

    print("========================================")
    print()


if __name__ == "__main__":
    main()