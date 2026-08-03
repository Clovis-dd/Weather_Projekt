"""
tests/backend/test_repository.py

Tests für die Repository-Schicht.

Testet:

- Speichern von Wetterdaten
- Laden aller Einträge
- Laden per ID
- Umgang mit unbekannten IDs
- Zählen von Datensätzen
"""


from __future__ import annotations


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from backend.database import Base
from backend.models import WeatherHistory
from backend.repository import WeatherRepository


# ======================================================
# Testdatenbank
# ======================================================


def create_test_session():
    """
    Erstellt eine temporäre SQLite-Testdatenbank.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False
        },
    )

    Base.metadata.create_all(
        bind=engine
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return SessionLocal()


# ======================================================
# Testdaten
# ======================================================


def create_weather_entry(
    city: str = "Duisburg",
) -> WeatherHistory:
    """
    Erstellt einen Test-Wetterdatensatz.
    """

    return WeatherHistory(
        city=city,
        country="Germany",
        temperature=24.5,
        feels_like=25.1,
        humidity=60,
        pressure=1015,
        wind_speed=12.3,
        prediction=7.8,
    )


# ======================================================
# Tests
# ======================================================


def test_repository_saves_weather():
    """
    Prüft das Speichern eines Wetterdatensatzes.
    """

    session = create_test_session()

    repository = WeatherRepository(
        session
    )

    weather = create_weather_entry()

    saved = repository.save(
        weather
    )

    assert saved.id is not None
    assert saved.city == "Duisburg"



def test_repository_returns_all_weather_entries():
    """
    Prüft das Laden aller Wetterdaten.
    """

    session = create_test_session()

    repository = WeatherRepository(
        session
    )

    repository.save(
        create_weather_entry("Duisburg")
    )

    repository.save(
        create_weather_entry("Essen")
    )

    entries = repository.get_all()

    assert len(entries) == 2



def test_repository_get_by_id_returns_entry():
    """
    Prüft das Laden eines Eintrags über die ID.
    """

    session = create_test_session()

    repository = WeatherRepository(
        session
    )

    saved = repository.save(
        create_weather_entry()
    )

    result = repository.get_by_id(
        saved.id
    )

    assert result is not None
    assert result.id == saved.id
    assert result.city == "Duisburg"



def test_repository_get_by_id_returns_none():
    """
    Prüft unbekannte IDs.
    """

    session = create_test_session()

    repository = WeatherRepository(
        session
    )

    result = repository.get_by_id(
        999
    )

    assert result is None



def test_repository_count_returns_number_of_entries():
    """
    Prüft die Anzahl gespeicherter Datensätze.
    """

    session = create_test_session()

    repository = WeatherRepository(
        session
    )

    repository.save(
        create_weather_entry()
    )

    repository.save(
        create_weather_entry()
    )

    repository.save(
        create_weather_entry()
    )

    assert repository.count() == 3