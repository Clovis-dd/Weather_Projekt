import pandas as pd
import pytest


from training.pipeline import TrainingPipeline

from shared.feature_schema import (
    FEATURES,
)


def create_weather_dataframe():

    return pd.DataFrame(
        [
            {
                "temperature": 20.0,
                "feels_like": 19.0,
                "humidity": 60,
                "pressure": 1015,
                "wind_speed": 10,
                "clouds": 50,
                "visibility": 10000,
            }
        ]
    )


def test_pipeline_creates_expected_features():

    dataframe = create_weather_dataframe()

    pipeline = TrainingPipeline()

    result = pipeline.prepare_features(
        dataframe
    )

    assert list(result.columns) == list(
        FEATURES
    )


def test_pipeline_does_not_modify_input():

    dataframe = create_weather_dataframe()

    original = dataframe.copy()

    pipeline = TrainingPipeline()

    pipeline.prepare_features(
        dataframe
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_pipeline_calculates_engineered_features():

    dataframe = create_weather_dataframe()

    pipeline = TrainingPipeline()

    result = pipeline.prepare_features(
        dataframe
    )


    assert result.loc[
        0,
        "temperature_difference"
    ] == 1.0


    assert result.loc[
        0,
        "wind_factor"
    ] == 5.0


    assert result.loc[
        0,
        "humidity_factor"
    ] == 0.6



def test_pipeline_detects_missing_columns():

    dataframe = pd.DataFrame(
        [
            {
                "temperature": 20,
            }
        ]
    )


    pipeline = TrainingPipeline()


    with pytest.raises(
        ValueError
    ):

        pipeline.prepare_features(
            dataframe
        )