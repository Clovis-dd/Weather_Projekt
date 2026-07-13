import joblib
import pandas as pd

import pytest

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor


from backend.model_registry import ModelRegistry

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



def prepare_predictor(
    tmp_path,
):

    model_file = (
        tmp_path / "model.pkl"
    )

    create_model_file(
        model_file
    )

    registry = ModelRegistry(
        tmp_path
    )

    info = registry.register_model(

        model_file,

        "RandomForestRegressor",

        {
            "r2": 0.9,
        },

    )

    registry.activate(
        info.name
    )

    predictor = WeatherPredictor(
        tmp_path
    )

    return (
        predictor,
        info,
    )



def valid_weather():

    return {

        "temperature":20,

        "feels_like":20,

        "humidity":50,

        "pressure":1015,

        "wind_speed":5,

        "clouds":20,

        "visibility":10000,

    }



def test_predict_returns_prediction(
    tmp_path,
):

    predictor, info = prepare_predictor(
        tmp_path
    )


    result = predictor.predict(
        valid_weather()
    )


    assert isinstance(
        result["prediction"],
        float,
    )


    assert result["model"] == info.name


    assert (
        result["feature_schema_version"]
        ==
        "1.0"
    )



def test_predict_detects_missing_features(
    tmp_path,
):

    predictor, _ = prepare_predictor(
        tmp_path
    )


    with pytest.raises(
        ValueError
    ):

        predictor.predict(
            {
                "temperature":20
            }
        )



def test_predict_without_champion_fails(
    tmp_path,
):

    predictor = WeatherPredictor(
        tmp_path
    )


    with pytest.raises(
        RuntimeError
    ):

        predictor.predict(
            valid_weather()
        )