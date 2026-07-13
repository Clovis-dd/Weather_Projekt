"""
feature_validator.py

Validierung der ML Features.

Verhindert Feature Drift zwischen:

- Training
- Inference
- gespeichertem Modell
"""


from __future__ import annotations


from collections.abc import Iterable

from typing import TypeGuard


import pandas as pd


from shared.feature_schema import (
    validate_feature_schema,
    get_feature_names,
    FEATURE_SCHEMA_VERSION,
)


from shared.logger import get_logger



logger = get_logger(
    __name__
)



FeatureInput = pd.DataFrame | dict[str, float]



# ======================================================
# Type Helpers
# ======================================================


def is_dataframe(
    data: FeatureInput,
) -> TypeGuard[pd.DataFrame]:
    """
    Type-Narrowing für PyCharm/Pyright.
    """

    return isinstance(
        data,
        pd.DataFrame,
    )



def is_feature_dict(
    data: FeatureInput,
) -> TypeGuard[dict[str, float]]:
    """
    Type-Narrowing für Dictionaries.
    """

    return isinstance(
        data,
        dict,
    )



# ======================================================
# Public API
# ======================================================


def validate_features(
    data: FeatureInput,
) -> None:
    """
    Prüft Feature-Struktur.
    """


    logger.debug(

        "Validating feature schema=%s",

        FEATURE_SCHEMA_VERSION,

    )


    if is_dataframe(data):

        features: list[str] = list(
            data.columns
        )


    elif is_feature_dict(data):

        features = list(
            data.keys()
        )


    else:

        raise TypeError(
            "Features must be DataFrame or dict[str,float]."
        )


    validate_feature_schema(
        features
    )


    logger.debug(
        "Feature validation successful."
    )



def validate_feature_names(
    features: Iterable[str],
) -> None:
    """
    Validiert Feature Namen.
    """

    validate_feature_schema(
        features
    )



def expected_features() -> list[str]:
    """
    Liefert erwartete Features.
    """

    return get_feature_names()