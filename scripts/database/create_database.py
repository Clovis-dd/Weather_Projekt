"""
create_database.py

Erstellt die SQLite-Datenbank
inklusive aller Tabellen.
"""

from __future__ import annotations

from database.database import Base
from database.database import engine


def main() -> None:

    print()

    print(
        "Erstelle Datenbank..."
    )

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Datenbank erfolgreich erstellt."
    )


if __name__ == "__main__":
    main()