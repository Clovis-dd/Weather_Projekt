# Projektarchitektur

## Gesamtübersicht

```
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
                 Feature Engineering
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
             ┌─────────────┴──────────────┐
             ▼                            ▼
      Model Loader                 Model Service
             │                            │
             └─────────────┬──────────────┘
                           ▼
                    Weather Predictor
                           │
                           ▼
                      FastAPI Backend
                           │
                           ▼
                   Streamlit Frontend
```

---

# Komponenten

## training/

Verantwortlich für

- Datensatz laden
- Feature Engineering
- Training
- Evaluation
- Registrierung neuer Modelle

---

## backend/

Verantwortlich für

- REST API
- Prediction
- Model Cache
- Registry Zugriff
- Wetterservice

---

## shared/

Gemeinsame Komponenten

- Konfiguration
- Logger
- Feature Engineering
- Feature Schema
- Validierung
- Pydantic Modelle

---

## frontend/

Benutzeroberfläche

- Streamlit
- Backend Kommunikation
- Darstellung der Vorhersagen

---

## models/

Enthält ausschließlich

- trainierte Modelle
- Registry
- Reports
- Backups

---

## data/

Persistente Trainingsdaten

---

## tests/

Unit Tests

---

## Designprinzipien

- Single Responsibility
- Dependency Injection
- Registry als Single Source of Truth
- Lose Kopplung
- Hohe Kohäsion
- Wiederverwendbarkeit