
# Weather Analytics & Machine Learning Platform

## Professionelle README (Version Zwischenstand)

> Diese README beschreibt den aktuellen Entwicklungsstand eines produktionsnahen Machine-Learning-Projekts zur Wettervorhersage.

## Inhaltsverzeichnis
1. Projekt
2. Architektur
3. Features
4. Technologien
5. Projektstruktur
6. Installation
7. Konfiguration
8. Projektsteuerung
9. REST API
10. Machine Learning
11. Datenbank
12. Tests
13. Roadmap
14. Projektphilosophie

# Projekt

Das Weather ML Project demonstriert den vollständigen Lebenszyklus einer modernen ML-Anwendung:
- Datenerfassung über OpenWeatherMap
- Feature Engineering
- Modelltraining
- Model Registry
- Champion-Modell
- FastAPI Backend
- Streamlit Frontend
- SQLite Historie
- Monitoring und Logging

# Architektur

```text
OpenWeatherMap
      │
WeatherService
      │
Feature Engineering
      │
Model Registry
      │
Champion Model
      │
FastAPI
 ├── REST API
 ├── Prediction Service
 └── SQLite
      │
Streamlit Dashboard
```

# Features

- Wetterabfrage
- ML-Vorhersage
- Model Registry
- SQLite-Historie
- Monitoring
- Logging
- Start-/Stop-Skripte
- Trainingspipeline

# Technologien

Python · FastAPI · Streamlit · SQLAlchemy · SQLite · Pandas · NumPy · scikit-learn · Joblib · Pydantic

# Projektstruktur
```
backend/
frontend/
training/
shared/
database/
scripts/
models/
tests/
docs/
```


# Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

# Projektsteuerung

Backend:
``` bash
python scripts/start/run_backend.py
```

Frontend:
``` bash
python scripts/start/run_streamlit.py
```

Status:
``` bash
python scripts/status.py
```

Stop:
``` bash
python scripts/stop/stop_all.py
```


# REST API

Basis-URL:
http://127.0.0.1:9000

Swagger:
http://127.0.0.1:9000/docs

ReDoc:
http://127.0.0.1:9000/redoc

| Methode | Endpoint        | Beschreibung             |
|---------|-----------------|--------------------------|
| GET     | /               | API-Info                 |
| GET     | /health         | Gesundheitsstatus        |
| GET     | /metrics        | Monitoring               |
| GET     | /model          | Champion-Modell          |
| POST    | /weather        | Wetter inkl. ML-Prognose |
| POST    | /predict        | Direkte Modellvorhersage |
| GET     | /history        | Vorhersagehistorie       |
| GET     | /history/latest | Neueste Vorhersage       |
| GET     | /history/{id}   | Einzelne Vorhersage      |

# Machine Learning

- Feature Engineering
- Random Forest
- Champion Model
- Registry
- Automatische Versionierung
- Trainingsreport

Training:
```bash
python -m training.train_weather_model
```

# Datenbank

SQLite speichert jede Wettervorhersage dauerhaft.
Hilfsskripte:
- create_database.py
- backup_database.py
- reset_database.py

# Tests

pytest

# Roadmap

- Dashboard-Historie
- Docker
- Docker Compose
- CI/CD
- MLflow
- Prometheus
- Grafana
- Deployment

# Projektphilosophie

- Qualität vor Geschwindigkeit
- Produktionsnahe Architektur
- Keine Quick Fixes
- Dokumentation parallel zur Entwicklung
- Saubere Softwarearchitektur
- Wartbarer Code
