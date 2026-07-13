# Projektdokumentation

## Ziel

Entwicklung einer produktionsnahen Machine-Learning-Anwendung zur Wetteranalyse.

Die Anwendung demonstriert den vollständigen Lebenszyklus eines ML-Modells:

- Datenerfassung
- Feature Engineering
- Modelltraining
- Modellverwaltung
- Inferenz
- API
- Frontend

---

# Komponenten

## Weather Collector

Sammelt Wetterdaten von OpenWeatherMap und erzeugt Trainingsdaten.

---

## Feature Engineering

Berechnet zusätzliche ML-Features

- temperature_difference
- wind_factor
- humidity_factor

---

## Feature Validation

Prüft

- Reihenfolge
- Datentypen
- Vollständigkeit

---

## Model Registry

Verwaltet sämtliche Modelle.

Speichert

- Modellname
- Version
- Feature Schema
- Trainingsmetriken
- Champion Status

---

## Model Loader

Lädt ausschließlich das Champion Modell.

Keine direkten Dateizugriffe innerhalb der Prediction Pipeline.

---

## Model Service

Verwaltet den Cache des Produktionsmodells.

Verhindert mehrfaches Laden bei jeder Prediction.

---

## Predictor

Produktions-Inferenz

Ablauf

Request

↓

Feature Engineering

↓

Feature Validation

↓

Model Service

↓

Prediction

↓

Response

---

## FastAPI

REST API

Endpoints

GET /health

GET /model

POST /predict

Swagger

/docs

---

## Streamlit

Frontend

Kommuniziert ausschließlich mit der REST API.

---

# Aktuelle Architektur

OpenWeatherMap

↓

WeatherService

↓

Feature Pipeline

↓

Prediction

↓

FastAPI

↓

Streamlit

---

# Produktionsmodell

RandomForestRegressor

Feature Schema Version

1.0

Modellverwaltung

Registry

Champion Modell

Caching

---

# Logging

Zentrale Logger

- Backend
- Training
- Frontend

Logdateien

- app.log
- warning.log
- error.log

---

# Monitoring

Prediction Monitor

Erfasst

- Prediction Count
- Fehler
- Durchschnittslatenz
- Letztes Modell

---

# Nächste Entwicklungsschritte

- Docker
- CI/CD
- Unit Tests
- Integration Tests
- Prometheus
- Grafana
- Kubernetes Deployment
- MLflow