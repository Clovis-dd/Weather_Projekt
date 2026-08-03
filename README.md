# Weather Analytics & Machine Learning Platform

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/License-MIT-success)


A production-oriented end-to-end platform for weather analytics, machine learning, prediction services and interactive visualization.

The project demonstrates the complete lifecycle of a modern machine learning application—from external data acquisition and feature engineering to model training, deployment through REST services, prediction, persistence and visualization.

---

# Overview

The platform combines modern software engineering principles with machine learning techniques in a modular architecture.

It is designed as a portfolio-quality project demonstrating professional backend development, clean architecture and production-oriented ML workflows.

Current capabilities include:

- Weather data retrieval via OpenWeatherMap
- Feature Engineering
- Model Training
- Model Registry
- Champion Model Management
- Machine Learning Prediction
- FastAPI Backend
- Streamlit Dashboard
- SQLite Persistence
- Prediction History
- Structured Logging
- Monitoring
- Docker Support

---

# Architecture

```
                    OpenWeatherMap API
                             │
                             ▼
                    Weather Service Layer
                             │
                             ▼
                  Feature Engineering Layer
                             │
          ┌──────────────────┴──────────────────┐
          ▼                                     ▼
   Machine Learning Layer                 SQLite Database
          │                                     │
   ┌──────┴────────┐                     Repository Pattern
   │               │
Model Registry  Champion Model
          │
          ▼
    Prediction Service
          │
          ▼
      FastAPI Backend
          │
          ▼
    Streamlit Dashboard
```

---

# Key Features

## Weather Analytics

- Current weather retrieval
- Multilingual support
- Weather normalization
- Structured weather responses

## Machine Learning

- Feature Engineering
- Automated Model Training
- Random Forest Regression
- Model Evaluation
- Champion Model
- Model Registry
- Model Versioning
- Training Reports

## Backend

- FastAPI REST API
- Repository Pattern
- Pydantic Validation
- Prediction Service
- Health Monitoring
- Metrics Endpoint
- Structured Logging

## Database

- SQLite
- Persistent Prediction History
- Historical Queries
- Repository Abstraction

## Frontend

- Streamlit Dashboard
- Weather Visualization
- Prediction Display
- Interactive User Interface

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Requests

## Machine Learning

- Pandas
- NumPy
- Scikit-Learn
- Joblib

## Frontend

- Streamlit

## Database

- SQLite

## DevOps

- Docker
- Docker Compose
- GitHub
- Pytest

---

# Project Structure

```
weather-analytics-platform/

├── backend/
├── frontend/
├── training/
├── shared/
├── database/
├── models/
├── scripts/
├── tests/
├── docs/
├── data/
├── logs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Quick Start

Clone the repository

```bash
git clone https://github.com/Clovis-dd/weather-analytics-platform.git

cd weather-analytics-platform
```

Create virtual environment

macOS / Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

```env
OWM_API_KEY=YOUR_API_KEY

HOST=127.0.0.1

PORT=9000

LOG_LEVEL=INFO
```

---

# Running the Project

## Backend

```bash
python scripts/start_backend.py
```

```bash
python scripts/stop_backend.py
```

Backend:

```
http://127.0.0.1:9000
```

---

## Frontend

```bash
python scripts/start_streamlit.py
```

```bash
python scripts/stop_streamlit.py
```

Dashboard:

```
http://localhost:8501
```

---

# Project Management

## Status

```bash
python scripts/status.py
```

## Start all services

```bash
python scripts/start_all.py
```

## Stop all services

```bash
python scripts/stop_all.py
```

---

# REST API

## Interactive Documentation

Swagger

```
http://127.0.0.1:9000/docs
```

ReDoc

```
http://127.0.0.1:9000/redoc
```

---

## System

| Method | Endpoint | Description                |
|--------|----------|----------------------------|
| GET    | /        | API Information            |
| GET    | /health  | Health Status              |
| GET    | /metrics | Runtime Metrics            |
| GET    | /model   | Champion Model Information |

---

## Weather

| Method | Endpoint | Description                     |
|--------|----------|---------------------------------|
| POST   | /weather | Current Weather + ML Prediction |

---

## Machine Learning

| Method | Endpoint | Description             |
|--------|----------|-------------------------|
| POST   | /predict | Direct Model Prediction |

---

## Prediction History

| Method | Endpoint        | Description                 |
|--------|-----------------|-----------------------------|
| GET    | /history        | Complete Prediction History |
| GET    | /history/latest | Latest Prediction           |
| GET    | /history/{id}   | Prediction by ID            |

---

# Machine Learning Pipeline

```
Weather Data
      │
      ▼
Feature Engineering
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
Model Registry
      │
      ▼
Champion Model
      │
      ▼
Prediction Service
```

Train a new model

```bash
python scripts/train_weather_model.py
```

---

# Database

SQLite is used as the persistence layer.

Current functionality:

- Prediction Storage
- Historical Queries
- Backup
- Reset
- Automatic Initialization

Database helper scripts:

```bash
python scripts/create_database.py
```

```bash
python scripts/backup_database.py
```

```bash
python scripts/reset_database.py
```

---

# Testing

Run all tests

```bash
pytest
```

Current test coverage includes:

- Repository Layer
- Database
- Backend Components
- Prediction Pipeline

---

# Project Status

## Completed

- FastAPI Backend
- Streamlit Dashboard
- SQLite Integration
- Prediction History
- Model Registry
- Champion Model
- Feature Engineering
- Monitoring
- Docker Foundation

---

# Roadmap

Upcoming features

- MLflow Integration
- Prometheus Monitoring
- Grafana Dashboard
- CI/CD Pipeline
- Cloud Deployment
- PostgreSQL Support
- Model Drift Detection

---

# Documentation

Detailed project documentation is available in the `docs/` directory.

Topics include:

- Software Architecture
- Architecture Decision Records (ADR)
- Deployment Guide
- Terminal Commands
- Lessons Learned
- Development Workflow

---

# Project Philosophy

This project follows professional software engineering principles:

- Quality over Speed
- Clean Architecture
- Separation of Concerns
- Single Responsibility Principle
- Documentation First
- Production-Oriented Design
- Testability
- Maintainability
- Continuous Improvement

---

# Author

**Clovis Wassom Leugoué**

Bachelor of Science in Business Information Systems

Focus Areas:

- Python
- Data Science
- Machine Learning
- Software Architecture
- Backend Development
- IT Service Management

---

# License

This project is released under the MIT License.