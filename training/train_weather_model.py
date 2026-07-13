"""
train_weather_model.py

Professioneller Trainingsprozess.

Ablauf:

Dataset laden
        |
        v
TrainingPipeline
        |
        v
RandomForest Training
        |
        v
Evaluation
        |
        v
Modell speichern
        |
        v
ModelRegistry aktualisieren
"""


from __future__ import annotations


import json

from datetime import (
    UTC,
    datetime,
)

from pathlib import Path


import joblib

import pandas as pd


from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from sklearn.model_selection import train_test_split


from shared.logger import get_logger


from shared.weather_model import (
    TARGET_NAME,
    RANDOM_STATE,
    TEST_SIZE,
    N_ESTIMATORS,
    MAX_DEPTH,
    MIN_SAMPLES_SPLIT,
    MIN_SAMPLES_LEAF,
)


from shared.feature_schema import (
    FEATURE_SCHEMA_VERSION,
    get_feature_names,
)


from training.pipeline import (
    TrainingPipeline,
)


from backend.model_registry import (
    ModelRegistry,
)



logger = get_logger(
    __name__
)



# ======================================================
# Configuration
# ======================================================


DATA_FILE = Path(
    "data/weather_history.csv"
)


MODELS_DIR = Path(
    "models"
)


TRAINED_MODEL_FILE = (
    MODELS_DIR /
    "latest_training_model.pkl"
)


REPORT_FILE = (
    MODELS_DIR /
    "training_report.json"
)



# ======================================================
# Dataset
# ======================================================


def load_dataset() -> pd.DataFrame:
    """
    Lädt Trainingsdaten.
    """

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"Dataset missing: {DATA_FILE}"
        )


    dataframe = pd.DataFrame(
        pd.read_csv(
            DATA_FILE
        )
    )


    logger.info(
        "Dataset loaded rows=%s",
        len(dataframe),
    )


    return dataframe



# ======================================================
# Training
# ======================================================


def train(
    dataframe: pd.DataFrame,
) -> tuple[
    RandomForestRegressor,
    dict[str, float],
]:
    """
    Trainiert Wettermodell
    und berechnet Metriken.
    """


    pipeline = TrainingPipeline()


    features = pipeline.prepare_features(
        dataframe
    )


    target = dataframe[
        TARGET_NAME
    ].astype(
        float
    )


    (
        x_train,
        x_test,
        y_train,
        y_test,
    ) = train_test_split(

        features,

        target,

        test_size=TEST_SIZE,

        random_state=RANDOM_STATE,

    )



    model = RandomForestRegressor(

        n_estimators=N_ESTIMATORS,

        max_depth=MAX_DEPTH,

        min_samples_split=MIN_SAMPLES_SPLIT,

        min_samples_leaf=MIN_SAMPLES_LEAF,

        random_state=RANDOM_STATE,

        n_jobs=-1,

    )



    logger.info(
        "Model training started"
    )



    model.fit(

        x_train,

        y_train,

    )



    prediction = model.predict(
        x_test
    )


    y_true = list(
        y_test
    )


    y_prediction = list(
        prediction
    )



    mse = mean_squared_error(

        y_true,

        y_prediction,

    )


    rmse = float(
        mse ** 0.5
    )



    metrics: dict[str, float] = {


        "r2":
            float(
                r2_score(
                    y_true,
                    y_prediction,
                )
            ),



        "mae":
            float(
                mean_absolute_error(
                    y_true,
                    y_prediction,
                )
            ),



        "rmse":
            rmse,


    }



    logger.info(
        "Model evaluation metrics=%s",
        metrics,
    )



    return (

        model,

        metrics,

    )



# ======================================================
# Model Save
# ======================================================


def save_model(
    model: RandomForestRegressor,
) -> Path:
    """
    Speichert trainiertes Modell.
    """


    MODELS_DIR.mkdir(
        exist_ok=True
    )


    joblib.dump(

        model,

        TRAINED_MODEL_FILE,

    )


    logger.info(
        "Model saved path=%s",
        TRAINED_MODEL_FILE,
    )


    return TRAINED_MODEL_FILE



# ======================================================
# Report
# ======================================================


def save_report(
    evaluation_metrics: dict[str, float],
) -> None:
    """
    Speichert Trainingsbericht.
    """


    REPORT_FILE.parent.mkdir(
        exist_ok=True
    )


    report = {


        "created_at":
            datetime.now(
                UTC
            ).isoformat(),



        "feature_schema_version":
            FEATURE_SCHEMA_VERSION,



        "metrics":
            evaluation_metrics,

    }



    with REPORT_FILE.open(

        "w",

        encoding="utf-8",

    ) as file:


        json.dump(

            report,

            file,

            indent=4,

            ensure_ascii=False,

        )



    logger.info(
        "Training report saved path=%s",
        REPORT_FILE,
    )



# ======================================================
# Main
# ======================================================


def main() -> None:
    """
    Führt kompletten Trainingsprozess aus.
    """


    dataframe = load_dataset()



    model, evaluation_metrics = train(
        dataframe
    )



    model_path = save_model(
        model
    )



    registry = ModelRegistry(
        MODELS_DIR
    )



    model_info = registry.register_model(

        model_path=model_path,

        algorithm=type(model).__name__,

        metrics=evaluation_metrics,

        feature_schema_version=FEATURE_SCHEMA_VERSION,

        features=get_feature_names(),

    )



    registry.activate(
        model_info.name
    )



    save_report(
        evaluation_metrics
    )



    logger.info(
        "Training completed successfully"
    )


    logger.info(
        "Champion model=%s",
        model_info.name,
    )



# ======================================================
# Entry Point
# ======================================================


if __name__ == "__main__":

    main()