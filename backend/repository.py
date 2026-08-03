"""
backend/repository.py

Datenzugriffsschicht für Wetterdaten.

Verantwortlich für:

- Speichern von Wetterhistorie
- Laden gespeicherter Wetterdaten
- Abfragen einzelner Datensätze
- Datenbankoperationen kapseln

Architektur:

API
 |
 ▼
WeatherRepository
 |
 ▼
SQLAlchemy Session
 |
 ▼
SQLite
"""


from __future__ import annotations


from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session


from backend.models import WeatherHistory


# ======================================================
# Repository
# ======================================================


class WeatherRepository:
    """
    Repository für Wetterhistorie.

    Kapselt sämtliche Datenbankzugriffe
    auf die Tabelle weather_history.
    """


    def __init__(
        self,
        session: Session,
    ) -> None:
        """
        Erstellt ein Repository.

        Args:
            session:
                Aktive SQLAlchemy Datenbanksession.
        """

        self.session = session


    # ==================================================
    # Speichern
    # ==================================================


    def save(
        self,
        weather: WeatherHistory,
    ) -> WeatherHistory:
        """
        Speichert einen Wetterdatensatz.

        Args:
            weather:
                SQLAlchemy Wettermodell.

        Returns:
            Gespeicherter Datensatz.
        """

        self.session.add(
            weather
        )

        self.session.commit()

        self.session.refresh(
            weather
        )

        return weather


    



    # ==================================================
    # Alle Datensätze
    # ==================================================


    def get_all(
        self,
    ) -> Sequence[WeatherHistory]:
        """
        Liefert alle gespeicherten Wetterdaten.

        Returns:
            Liste aller Wetterdatensätze.
        """

        statement = select(
            WeatherHistory
        )

        result = self.session.execute(
            statement
        )

        return result.scalars().all()


    # ==================================================
    # Einzelner Datensatz
    # ==================================================


    def get_by_id(
        self,
        weather_id: int,
    ) -> WeatherHistory | None:
        """
        Liefert einen Datensatz anhand seiner ID.

        Args:
            weather_id:
                Primärschlüssel.

        Returns:
            Wetterdatensatz oder None.
        """

        statement = select(
            WeatherHistory
        ).where(
            WeatherHistory.id == weather_id
        )

        result = self.session.execute(
            statement
        )

        return result.scalar_one_or_none()


    # ==================================================
    # Anzahl
    # ==================================================


    def count(
        self,
    ) -> int:
        """
        Gibt die Anzahl gespeicherter Datensätze zurück.

        Returns:
            Anzahl der Einträge.
        """

        return self.session.query(
            WeatherHistory
        ).count()


    # ==================================================
    # Neuester Datensatz
    # ==================================================

    def get_latest(
        self,
    ) -> WeatherHistory | None:
        """
        Liefert den zuletzt gespeicherten Datensatz.

        Returns:
            Neuester Wetterdatensatz oder None.
        """

        statement = (
            select(WeatherHistory)
            .order_by(
                WeatherHistory.created_at.desc()
            )
            .limit(1)
        )

        result = self.session.execute(
            statement
        )

        return result.scalar_one_or_none()


    # ==================================================
    # Letzte N Datensätze
    # ==================================================

    def get_last(
        self,
        limit: int = 10,
    ) -> Sequence[WeatherHistory]:
        """
        Liefert die letzten gespeicherten Datensätze.

        Args:
            limit:
                Maximale Anzahl Einträge.

        Returns:
            Liste der neuesten Wetterdaten.
        """

        statement = (
            select(WeatherHistory)
            .order_by(
                WeatherHistory.created_at.desc()
            )
            .limit(limit)
        )

        result = self.session.execute(
            statement
        )

        return result.scalars().all()


    # ==================================================
    # Tabelle leeren
    # ==================================================

    def delete_all(
        self,
    ) -> None:
        """
        Löscht sämtliche Wetterdaten.
        """

        self.session.query(
            WeatherHistory
        ).delete()

        self.session.commit()