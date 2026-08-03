"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    reset_database.py

Description:
    Deletes the current SQLite database and recreates it.

WARNING:
    All stored data will be permanently removed.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from pathlib import Path

from scripts.bootstrap import initialize

initialize()

from backend.database import Base
from backend.database import engine

from shared.logger import get_logger


logger = get_logger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_FILE = PROJECT_ROOT / "database" / "weather.db"


def reset_database() -> None:
    """
    Delete and recreate the SQLite database.
    """

    logger.warning(
        "Database reset requested."
    )

    if DATABASE_FILE.exists():

        DATABASE_FILE.unlink()

        logger.info(
            "Database removed: %s",
            DATABASE_FILE,
        )

    else:

        logger.info(
            "No existing database found."
        )

    Base.metadata.create_all(
        bind=engine,
    )

    logger.info(
        "Database recreated successfully."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Database Reset")
    print("========================================")
    print(" Status : SUCCESS")
    print(" Database recreated successfully.")
    print("========================================")

    print()


if __name__ == "__main__":

    answer = input(
        "\nThis will permanently delete the database.\n"
        "Continue? (y/N): "
    )

    if answer.lower() == "y":

        reset_database()

    else:

        print("\nOperation cancelled.\n")