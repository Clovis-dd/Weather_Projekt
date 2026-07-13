"""
weather_model.py

Zentrale Definition des Machine-Learning-Modells.

Wird verwendet von:

- Training
- Backend
- Model Loader

Definiert ausschließlich:
- Modellname
- Modellversion
- Dateien
- Trainingsparameter
"""

from typing import Final


# ======================================================
# Modell Identität
# ======================================================


MODEL_NAME: Final[str] = (
    "weather_model_v1"
)


MODEL_VERSION: Final[str] = (
    "1.0.0"
)



# ======================================================
# Target
# ======================================================


TARGET_NAME: Final[str] = (
    "weather_score"
)



# ======================================================
# Algorithmus
# ======================================================


ALGORITHM: Final[str] = (
    "RandomForestRegressor"
)



# ======================================================
# Training Parameter
# ======================================================


RANDOM_STATE: Final[int] = 42


TEST_SIZE: Final[float] = 0.2


N_ESTIMATORS: Final[int] = 300


MAX_DEPTH: Final[int | None] = None


MIN_SAMPLES_SPLIT: Final[int] = 2


MIN_SAMPLES_LEAF: Final[int] = 1