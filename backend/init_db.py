"""
backend/init_db.py

Initialisiert die SQLite-Datenbank.

Verantwortlich für:

- Erzeugen aller Tabellen
- Initialisierung der Datenbank

Ausführung:

python -m backend.init_db
"""

from backend.database import Base
from backend.database import engine

# Alle Modelle importieren,
# damit SQLAlchemy die Tabellen kennt.
from backend import models  # noqa: F401


def init_database() -> None:
    """
    Erstellt alle Datenbanktabellen.
    """

    Base.metadata.create_all(bind=engine)

    print("SQLite database initialized.")


if __name__ == "__main__":
    init_database()