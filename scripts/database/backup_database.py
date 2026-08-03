"""
backup_database.py

Erstellt eine Sicherung
der SQLite-Datenbank.
"""

from __future__ import annotations

from datetime import datetime

import shutil

from pathlib import Path


DATABASE = Path(
    "database/weather.db"
)

BACKUP_DIR = Path(
    "database/backups"
)


def main() -> None:

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        BACKUP_DIR
        / f"weather_{timestamp}.db"
    )

    shutil.copy2(
        DATABASE,
        backup_file,
    )

    print()

    print(
        "Backup erstellt:"
    )

    print(
        backup_file
    )


if __name__ == "__main__":
    main()