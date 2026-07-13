import pandas as pd
import pytest


from shared.feature_validator import (
    validate_features,
    validate_feature_names,
    expected_features,
)


def test_validate_dataframe_with_valid_features():

    dataframe = pd.DataFrame(
        columns=expected_features()
    )

    validate_features(
        dataframe
    )


def test_validate_dict_with_valid_features():

    data = {
        feature: 0.0
        for feature in expected_features()
    }

    validate_features(
        data
    )


def test_validate_features_detects_wrong_order():

    features = expected_features()

    wrong_order = features[::-1]

    with pytest.raises(
        ValueError
    ):
        validate_feature_names(
            wrong_order
        )


def test_validate_features_detects_missing_feature():

    features = expected_features()

    features.remove(
        "humidity_factor"
    )

    with pytest.raises(
        ValueError
    ):
        validate_feature_names(
            features
        )


def test_validate_features_rejects_invalid_type():

    with pytest.raises(
        TypeError
    ):
        validate_features(
            ["temperature"]
        )


def test_expected_features_returns_schema():

    features = expected_features()

    assert isinstance(
        features,
        list,
    )

    assert len(
        features
    ) == 10