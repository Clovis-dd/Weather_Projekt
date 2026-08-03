"""
tests/backend/test_database.py

Tests für die SQLite Datenbankschicht.

Prüft:

- Datenbank Engine
- SessionFactory
- ORM Tabellen
- Speichern von Daten
"""


from pathlib import Path


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from backend.database import Base
from backend.models import WeatherHistory



def create_test_database(
    tmp_path: Path,
):
    """
    Erstellt eine temporäre Testdatenbank.
    """

    database_file = (
        tmp_path
        /
        "test_weather.db"
    )

    engine = create_engine(
        f"sqlite:///{database_file}",
        connect_args={
            "check_same_thread": False
        },
    )


    Base.metadata.create_all(
        engine
    )


    SessionLocal = sessionmaker(
        bind=engine
    )


    return SessionLocal()



def test_database_creates_tables(
    tmp_path,
):

    session = create_test_database(
        tmp_path
    )

    assert session is not None

    session.close()



def test_database_saves_weather_history(
    tmp_path,
):

    session = create_test_database(
        tmp_path
    )


    weather = WeatherHistory(

        city="Duisburg",

        country="Germany",

        temperature=20.5,

        feels_like=20.0,

        humidity=60,

        pressure=1015,

        wind_speed=3.5,

        prediction=21.2,

    )


    session.add(
        weather
    )

    session.commit()


    result = session.query(
        WeatherHistory
    ).first()


    assert result is not None

    assert result.city == "Duisburg"

    assert result.prediction == 21.2


    session.close()