# 🌤️ Weather App (OpenWeatherMap)

Eine Python-basierte Streamlit-Webanwendung zur Anzeige aktueller Wetterdaten über die OpenWeatherMap API.

Die Anwendung ermöglicht Wetterabfragen über:

- 🌍 Stadtname
- 📍 geografische Koordinaten (Breiten- und Längengrad)

Die Wetterdaten werden übersichtlich dargestellt und unterstützen mehrere Sprachen.

---

## 🚀 Features

- Aktuelle Wetterdaten über OpenWeatherMap API
- Suche über:
  - Stadtname
  - Latitude / Longitude
- Mehrsprachige Oberfläche:
  - 🇩🇪 Deutsch
  - 🇬🇧 Englisch
  - 🇫🇷 Französisch
- Temperaturanzeige in Celsius
- Wetterbeschreibung
- Wetter-Icon
- Luftfeuchtigkeit
- Luftdruck
- Windgeschwindigkeit
- Validierung von Koordinaten
- Fehlerbehandlung bei API-Problemen

---

## 🛠️ Technologien

- Python
- Streamlit
- OpenWeatherMap API
- Requests
- python-dotenv

---

## 📦 Installation# Weather ML Projekt

Ein produktionsnahes Machine-Learning-Projekt zur Wettervorhersage mit vollständiger Trennung von Training, Inference und API.

## Projektziele

- Wetterdaten über OpenWeatherMap abrufen
- Machine-Learning-Modell trainieren
- Modellverwaltung über Model Registry
- REST API mit FastAPI
- Streamlit Frontend
- Produktionsnahe Projektstruktur

---

## Architektur

OpenWeatherMap
        │
        ▼
Weather Collector
        │
        ▼
weather_history.csv
        │
        ▼
Training Pipeline
        │
        ▼
RandomForest Training
        │
        ▼
Model Registry
        │
        ▼
Champion Model
        │
        ▼
FastAPI Backend
        │
        ▼
Streamlit Frontend

---

## Projektstruktur

```
backend/
frontend/
training/
shared/
models/
data/
tests/
logs/
```

---

## Backend starten

```bash
uvicorn backend.api:app --reload --port 9000
```

Swagger

```
http://127.0.0.1:9000/docs
```

---

## Frontend starten

```bash
streamlit run frontend/app.py
```

---

## Modell trainieren

```bash
python -m training.train_weather_model
```

---

## Verwendete Technologien

- Python
- FastAPI
- Streamlit
- scikit-learn
- Pandas
- Joblib
- Pydantic
- OpenWeatherMap API

---

## Architekturprinzipien

- Single Responsibility Principle
- Registry als Single Source of Truth
- Kein direkter Modellzugriff außerhalb des Loaders
- Feature Engineering zentralisiert
- Typisierte Requests und Responses
- Produktionsnahe Projektstruktur

---

## Projektstatus

✔ Training

✔ Model Registry

✔ Champion Model

✔ Backend API

✔ Frontend

✔ Prediction Pipeline

✔ Monitoring

✔ Feature Validation

✔ Feature Schema

---

## Nächste Schritte

- Docker
- CI/CD
- MLflow
- Model Drift Monitoring
- Prometheus
- Grafana

Repository klonen:

```bash
git clone <repository-url>