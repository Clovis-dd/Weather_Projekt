"""
reset_database.py

Löscht die Datenbank
und erstellt sie neu.
"""

from __future__ import annotations

from pathlib import Path

from database.database import Base
from database.database import engine


DATABASE = Path(
    "database/weather.db"
)


def main() -> None:

    print()

    print(
        "WARNUNG!"
    )

    print(
        "Alle Daten gehen verloren."
    )

    answer = input(
        "Datenbank wirklich löschen? (ja/nein): "
    )

    if answer.lower() != "ja":

        print(
            "Abgebrochen."
        )

        return

    if DATABASE.exists():

        DATABASE.unlink()

        print(
            "SQLite-Datei gelöscht."
        )

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Neue Datenbank erstellt."
    )


if __name__ == "__main__":
    main()