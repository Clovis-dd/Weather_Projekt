"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    create_database.py

Description:
    Creates the SQLite database and all configured tables.

This script is safe to execute multiple times.
Existing tables will not be recreated.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from scripts.bootstrap import initialize

initialize()

from backend.database import Base
from backend.database import engine

from shared.logger import get_logger


logger = get_logger(__name__)


def create_database() -> None:
    """
    Create all database tables.
    """

    logger.info(
        "Creating SQLite database..."
    )

    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database successfully initialized."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Database Initialization")
    print("========================================")
    print(" Status : SUCCESS")
    print(" Database successfully created.")
    print("========================================")

    print()


if __name__ == "__main__":

    create_database()