"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    bootstrap.py

Description:
    Initializes the application runtime environment.

Responsibilities
----------------
- Add the project root directory to sys.path
- Prepare the Python runtime environment
- Ensure consistent imports across all helper scripts

This module should be imported before any project-specific
modules are loaded.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

import sys
from pathlib import Path


def initialize() -> Path:
    """
    Initialize the project runtime environment.

    Returns
    -------
    Path
        Absolute path to the project root directory.
    """

    project_root = Path(__file__).resolve().parents[1]

    project_root_str = str(project_root)

    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return project_root


PROJECT_ROOT = initialize()


if __name__ == "__main__":

    print()
    print("===================================")
    print(" Weather Analytics Platform")
    print(" Bootstrap")
    print("===================================")
    print(f"Project Root : {PROJECT_ROOT}")
    print("Python Path successfully initialized.")
    print("===================================")
    print()