"""
feature_schema.py

Zentrale Definition des ML Feature Schemas.

Wird verwendet von:

- Training
- Inference
- Model Registry

Damit Training und Produktion
denselben Feature-Vertrag verwenden.
"""


from __future__ import annotations


from collections.abc import Iterable


from shared.logger import get_logger



logger = get_logger(
    __name__
)



# ======================================================
# Schema Definition
# ======================================================


FEATURE_SCHEMA_VERSION = "1.0"



FEATURE_SCHEMA: tuple[str, ...] = (

    "temperature",

    "feels_like",

    "humidity",

    "pressure",

    "wind_speed",

    "clouds",

    "visibility",

    "temperature_difference",

    "wind_factor",

    "humidity_factor",

)



# Kompatibilität für bestehende Importe

FEATURES = FEATURE_SCHEMA



# ======================================================
# Public API
# ======================================================


def get_feature_schema() -> dict[str, object]:
    """
    Liefert die vollständige Schema-Information.
    """

    return {

        "version": FEATURE_SCHEMA_VERSION,

        "features": list(
            FEATURE_SCHEMA
        ),

    }



def get_feature_names() -> list[str]:
    """
    Liefert die erwartete Feature-Reihenfolge.
    """

    return list(
        FEATURE_SCHEMA
    )



def validate_feature_schema(
    features: Iterable[str],
) -> None:
    """
    Prüft Feature Reihenfolge und Inhalt.
    """

    incoming: list[str] = list(
        features
    )


    expected: list[str] = list(
        FEATURE_SCHEMA
    )


    if incoming != expected:

        logger.error(

            "Feature schema mismatch expected=%s received=%s",

            expected,

            incoming,

        )


        raise ValueError(
            "Feature schema mismatch."
        )


    logger.debug(

        "Feature schema validation successful version=%s",

        FEATURE_SCHEMA_VERSION,

    )