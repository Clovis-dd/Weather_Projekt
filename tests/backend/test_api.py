import joblib

from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from sklearn.ensemble import RandomForestRegressor

from backend import api

from backend.api import (
    app,
)



from backend.model_registry import (
    ModelRegistry,
)
from backend.model_service import ModelService
from backend.predictor import WeatherPredictor
from shared.feature_schema import FEATURE_SCHEMA


def create_model_file(
    path: Path,
) -> None:

    X = pd.DataFrame(
        [[
            20,
            20,
            50,
            1015,
            5,
            20,
            10000,
            0,
            1,
            0.5,
        ]],
        columns=FEATURE_SCHEMA,
    )

    y = [0.8]

    model = RandomForestRegressor(
        n_estimators=2,
        random_state=42,
    )

    model.fit(
        X,
        y,
    )

    joblib.dump(
        model,
        path,
    )



def valid_weather_payload():

    return {

        "city": "Berlin",

        "language": "de",

        "temperature":20,

        "feels_like":20,

        "humidity":50,

        "pressure":1015,

        "wind_speed":5,

        "clouds":20,

        "visibility":10000,

    }



def prepare_model(
    tmp_path,
):

    model_file = (
        tmp_path / "model.pkl"
    )


    create_model_file(
        model_file
    )


    test_registry = ModelRegistry(
        tmp_path
    )


    info = test_registry.register_model(

        model_file,

        "RandomForestRegressor",

        {
            "r2":0.9
        },

    )


    test_registry.activate(
        info.name
    )


    return info



def test_root_endpoint():

    client = TestClient(
        app
    )


    response = client.get(
        "/"
    )


    assert response.status_code == 200


    body = response.json()


    assert body["service"] == (
        "Weather ML API"
    )


    assert body["status"] == (
        "running"
    )


def test_metrics_endpoint():

    client = TestClient(
        app
    )

    response = client.get(
        "/metrics"
    )

    assert response.status_code == 200

    body = response.json()

    assert "predictions_total" in body

    assert "prediction_errors" in body

    assert "average_latency_ms" in body


def test_health_endpoint(
    tmp_path,
):
    """
    Der Health-Endpoint soll den Status
    eines geladenen Champion-Modells korrekt
    zurückgeben.
    """

    prepare_model(
        tmp_path
    )

    api.model_service = ModelService(
        tmp_path
    )

    client = TestClient(
        api.app
    )

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["model_loaded"] is True

    assert data["active_model"] is not None

    assert data["feature_schema_version"] is not None


def test_prediction_endpoint(tmp_path):

    info = prepare_model(
        tmp_path
    )

    api.predictor = WeatherPredictor(
        tmp_path
    )

    client = TestClient(
        api.app
    )

    response = client.post(
        "/predict",
        json=valid_weather_payload(),
    )

    print(response.json())

    assert response.status_code == 200

    body = response.json()

    assert "prediction" in body
    assert body["model"] == info.name


def test_model_endpoint_without_champion():

    client = TestClient(
        app
    )


    response = client.get(
        "/model"
    )


    assert response.status_code in [
        200,
        503,
    ]


def test_request_id_header():

    client = TestClient(
        app
    )

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        "X-Request-ID"
        in response.headers
    )

    assert (
        len(
            response.headers["X-Request-ID"]
        )
        > 0
    )

