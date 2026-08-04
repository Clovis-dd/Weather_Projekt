"""
backend/models.py

SQLAlchemy ORM-Modelle.

Verantwortlich für:

- Definition aller Datenbanktabellen
- Datenbankschema
- Typdefinitionen
- Beziehungen zwischen Tabellen

Architektur:

SQLite
    ↑
SQLAlchemy ORM
    ↑
Repository
    ↑
API
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.database import Base


# ======================================================
# Tabellen
# ======================================================

class WeatherHistory(Base):
    """
    Speichert alle Wetteranfragen inklusive Vorhersage.
    """

    __tablename__ = "weather_history"

    # ==================================================
    # Primärschlüssel
    # ==================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # ==================================================
    # Standort
    # ==================================================

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ==================================================
    # Wetterdaten
    # ==================================================

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    feels_like: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    humidity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pressure: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    wind_speed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ==================================================
    # ML-Vorhersage
    # ==================================================

    prediction: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ==================================================
    # Zeitstempel
    # ==================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # ==================================================
    # Darstellung
    # ==================================================

    def __repr__(self) -> str:
        """
        Lesbare Darstellung eines Datensatzes.
        """

        return (
            "WeatherHistory("
            f"id={self.id}, "
            f"city='{self.city}', "
            f"country='{self.country}', "
            f"temperature={self.temperature:.1f}, "
            f"prediction={self.prediction:.2f}"
            ")"
        )


    def to_dict(
            self,
    ) -> dict[str, Any]:
        return {

            "id": self.id,

            "city": self.city,

            "country": self.country,

            "temperature": self.temperature,

            "feels_like": self.feels_like,

            "humidity": self.humidity,

            "pressure": self.pressure,

            "wind_speed": self.wind_speed,

            "prediction": self.prediction,

            "created_at": self.created_at,

        }