"""
model_loader.py

Production Model Loader.

Verantwortlich für:

- Champion Modell aus Registry laden
- Registry bleibt einzige Quelle der Wahrheit
- keine direkten pkl Pfade in Inference
"""

from __future__ import annotations


from pathlib import Path


import joblib


from sklearn.ensemble import RandomForestRegressor


from backend.model_registry import ModelRegistry


from shared.logger import get_logger



logger = get_logger(
    __name__
)



class ModelLoader:
    """
    Lädt das aktuell aktive Produktionsmodell.
    """


    def __init__(
        self,
        models_dir: Path,
    ) -> None:


        self.models_dir = models_dir


        self.registry = ModelRegistry(
            models_dir
        )



    def load_active_model(
        self,
    ) -> RandomForestRegressor:
        """
        Lädt das Champion Modell aus der Registry.
        """


        champion = self.registry.get_champion()



        if champion is None:

            raise RuntimeError(
                "No champion model available."
            )



        model_path = (
            self.models_dir
            /
            champion.filename
        )



        if not model_path.exists():

            raise FileNotFoundError(
                f"Champion model missing: {model_path}"
            )



        logger.info(
            "Loading champion model=%s",
            champion.name,
        )



        model = joblib.load(
            model_path
        )



        if not isinstance(
            model,
            RandomForestRegressor,
        ):

            raise TypeError(
                "Loaded model type mismatch."
            )



        logger.info(
            "Champion model loaded successfully"
        )


        return model