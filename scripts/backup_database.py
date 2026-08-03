"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    backup_database.py

Description:
    Creates a timestamped backup of the SQLite database.

The backup is stored inside the backups' directory.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

from shared.logger import get_logger

logger = get_logger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_FILE = DATABASE_DIR / "weather.db"

BACKUP_DIR = DATABASE_DIR / "backups"


def backup_database() -> None:
    """
    Create a timestamped backup of the SQLite database.
    """

    if not DATABASE_FILE.exists():

        logger.error(
            "Database file not found: %s",
            DATABASE_FILE,
        )

        print("Database file not found.")
        return

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        BACKUP_DIR
        / f"weather_backup_{timestamp}.db"
    )

    shutil.copy2(
        DATABASE_FILE,
        backup_file,
    )

    logger.info(
        "Database backup created: %s",
        backup_file,
    )

    print()
    print("===================================")
    print(" Database Backup Created")
    print("===================================")
    print(f"Source : {DATABASE_FILE}")
    print(f"Backup : {backup_file}")
    print("===================================")
    print()


if __name__ == "__main__":
    backup_database()