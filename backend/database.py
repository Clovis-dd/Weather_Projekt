"""
backend/database.py

Zentrale Datenbankkonfiguration.

Verantwortlich für:

- Datenbankpfad
- SQLAlchemy Engine
- SessionFactory
- ORM Basisklasse

Architektur:

FastAPI
    │
    ▼
Repository
    │
    ▼
Session
    │
    ▼
SQLite
"""

from __future__ import annotations

import os
from pathlib import Path
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


# ======================================================
# Datenbankpfad
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "weather.db"
)

DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(DEFAULT_DATABASE_PATH),
    )
)

# Datenbankordner automatisch anlegen
DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ======================================================
# Datenbank Engine
# ======================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    pool_pre_ping=True,
    future=True,
)


# ======================================================
# Session Factory
# ======================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


# ======================================================
# ORM Basisklasse
# ======================================================

class Base(DeclarativeBase):
    """
    Basisklasse aller SQLAlchemy-Modelle.
    """

    pass


# ======================================================
# Session Helper
# ======================================================

def get_session() -> Generator[Session, None, None]:
    """
    Erstellt eine Datenbanksitzung.

    Wird später von FastAPI als Dependency verwendet.

    Yields:
        Session: Aktive SQLAlchemy-Session.
    """

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()