"""
model_service.py

Production Model Service.

Verantwortlichkeiten:

- hält geladenes Champion Modell im Speicher
- verhindert mehrfaches Laden
- liefert aktives Modell an Predictor
- kann Reload unterstützen
"""


from __future__ import annotations


from pathlib import Path


from sklearn.ensemble import RandomForestRegressor


from backend.model_loader import ModelLoader


from shared.logger import get_logger


logger = get_logger(
    __name__
)



class ModelService:
    """
    Service für das Laden und Cachen
    des aktiven Champion Modells.
    """



    def __init__(
        self,
        models_dir: Path,
    ) -> None:


        self.loader = ModelLoader(
            models_dir
        )


        self._model: RandomForestRegressor | None = None



    def get_model(
        self,
    ) -> RandomForestRegressor:
        """
        Liefert das aktive Modell.

        Das Modell wird nur einmal geladen
        und anschließend gecached.
        """


        if self._model is None:

            logger.info(
                "Loading champion model"
            )


            self._model = (
                self.loader.load_active_model()
            )


            logger.info(
                "Champion model cached"
            )


        return self._model

    def get_model_information(
            self,
    ) -> dict:

        champion = self.get_champion()

        if champion is None:
            return {
                "model": None,
                "status": "no champion available",
            }

        return {
            "name": champion.name,
            "filename": champion.filename,
            "algorithm": champion.algorithm,
            "metrics": champion.metrics,
            "features": champion.features,
            "feature_schema_version":
                champion.feature_schema_version,
            "status": champion.status,
        }


    def get_champion(
        self,
    ):
        """
        Liefert Metadaten des aktiven Champion Modells.
        """


        return (
            self.loader.registry.get_champion()
        )



    def reload_model(
        self,
    ) -> RandomForestRegressor:
        """
        Erzwingt erneutes Laden des Champion Modells.
        """


        logger.info(
            "Reloading champion model"
        )


        self._model = (
            self.loader.load_active_model()
        )


        logger.info(
            "Model reload completed"
        )


        return self._model



    def is_loaded(
        self,
    ) -> bool:
        """
        Prüft, ob ein Modell bereits geladen wurde.
        """


        return self._model is not None

    def ensure_loaded(
            self,
    ) -> bool:
        """
        Lädt Champion Modell falls nötig.

        Gibt zurück,
        ob ein Modell verfügbar ist.
        """

        if self._model is None:
            self.get_model()

        return self._model is not None