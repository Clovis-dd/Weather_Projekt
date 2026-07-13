import pandas as pd

from shared.feature_engineering import (
    engineer_features,
)



def test_engineer_features_creates_expected_features():

    dataframe = pd.DataFrame(
        [
            {
                "temperature": 20.0,
                "feels_like": 18.0,
                "humidity": 50,
                "pressure": 1015,
                "wind_speed": 10,
                "clouds": 20,
                "visibility": 10000,
            }
        ]
    )


    result = engineer_features(
        dataframe
    )


    assert isinstance(
        result,
        pd.DataFrame,
    )


    assert (
        result.loc[0, "temperature_difference"]
        ==
        2.0
    )


    assert (
        result.loc[0, "wind_factor"]
        ==
        10.0
    )


    assert (
        result.loc[0, "humidity_factor"]
        ==
        0.5
    )



def test_engineer_features_does_not_modify_input():

    dataframe = pd.DataFrame(
        [
            {
                "temperature": 20.0,
                "feels_like": 18.0,
                "humidity": 50,
                "wind_speed": 10,
            }
        ]
    )


    original_columns = list(
        dataframe.columns
    )


    engineer_features(
        dataframe
    )


    assert list(
        dataframe.columns
    ) == original_columns



def test_engineer_features_requires_dataframe():

    try:

        engineer_features(
            {
                "temperature": 20
            }
        )

    except TypeError:

        assert True

    else:

        assert False