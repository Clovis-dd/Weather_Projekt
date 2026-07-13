"""
model_registry.py

Production ML Model Registry.

Verantwortlichkeiten:

- Modelle registrieren
- Versionen verwalten
- Champion Modell verwalten
- Challenger Modelle verwalten
- Rollback ermöglichen
- Registry persistieren

Registry:

models/
    registry.json
"""

from __future__ import annotations


import json
import shutil

from dataclasses import (
    asdict,
    dataclass,
)

from datetime import (
    UTC,
    datetime,
)

from pathlib import Path

from typing import Any


from shared.feature_schema import (
    FEATURE_SCHEMA_VERSION,
    get_feature_names,
)

from shared.logger import get_logger


logger = get_logger(
    __name__
)


# ======================================================
# Defaults
# ======================================================

DEFAULT_MODELS_DIR = Path(
    "models"
)


REGISTRY_VERSION = 3


MODEL_PREFIX = (
    "weather_model"
)


# ======================================================
# Model Information
# ======================================================


@dataclass
class ModelInfo:
    """
    Beschreibung eines registrierten Modells.
    """

    name: str

    filename: str

    algorithm: str

    created_at: str

    metrics: dict[str, float]

    feature_schema_version: str = FEATURE_SCHEMA_VERSION

    features: list[str] | None = None

    status: str = "challenger"


    def __post_init__(self) -> None:

        if self.features is None:
            self.features = get_feature_names()


    def is_champion(self) -> bool:

        return self.status == "champion"



# ======================================================
# Registry
# ======================================================


class ModelRegistry:
    """
    Verwaltung aller ML Modelle.
    """


    def __init__(
        self,
        models_dir: Path | None = None,
    ):

        self.models_dir = (
            models_dir
            or DEFAULT_MODELS_DIR
        )


        self.registry_file = (
            self.models_dir
            /
            "registry.json"
        )


        self.models_dir.mkdir(
            exist_ok=True
        )


        self.data = (
            self._load()
        )



    # ==================================================
    # Persistence
    # ==================================================

    @staticmethod
    def _empty_registry(
    ) -> dict[str, Any]:

        return {

            "version":
                REGISTRY_VERSION,

            "champion":
                None,

            "models":
                [],

        }



    def _load(
        self,
    ) -> dict[str, Any]:


        if not self.registry_file.exists():

            return self._empty_registry()



        try:

            with self.registry_file.open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )


        except Exception as error:

            logger.exception(
                "Registry loading failed"
            )

            raise RuntimeError(
                "Invalid model registry"
            ) from error



        if isinstance(data, list):

            return self._migrate_old_registry(
                data
            )


        data.setdefault(
            "version",
            REGISTRY_VERSION,
        )


        data.setdefault(
            "champion",
            None,
        )


        data.setdefault(
            "models",
            [],
        )


        for model in data["models"]:

            model.setdefault(
                "feature_schema_version",
                FEATURE_SCHEMA_VERSION,
            )

            model.setdefault(
                "features",
                get_feature_names(),
            )


        return data


    # ==================================================
    # Migration
    # ==================================================

    def _migrate_old_registry(
        self,
        old_data: list[dict[str, Any]],
    ) -> dict[str, Any]:

        logger.warning(
            "Old registry format detected. Migrating."
        )


        backup = (
            self.registry_file.with_suffix(
                ".backup.json"
            )
        )


        shutil.copy2(
            self.registry_file,
            backup,
        )


        migrated_models = []


        for old_model in old_data:

            migrated_models.append(

                {

                    "name":
                        old_model.get(
                            "name",
                            old_model.get(
                                "model_name",
                                "unknown_model",
                            ),
                        ),


                    "filename":
                        old_model.get(
                            "filename",
                            old_model.get(
                                "file",
                                "",
                            ),
                        ),


                    "algorithm":
                        old_model.get(
                            "algorithm",
                            "unknown",
                        ),


                    "created_at":
                        old_model.get(
                            "created_at",
                            datetime.now(
                                UTC
                            ).isoformat(),
                        ),


                    "metrics":
                        old_model.get(
                            "metrics",
                            {},
                        ),


                    "feature_schema_version":
                        old_model.get(
                            "feature_schema_version",
                            FEATURE_SCHEMA_VERSION,
                        ),


                    "features":
                        old_model.get(
                            "features",
                            get_feature_names(),
                        ),


                    "status":
                        old_model.get(
                            "status",
                            "archived",
                        ),

                }

            )


        migrated = {

            "version":
                REGISTRY_VERSION,

            "champion":
                None,

            "models":
                migrated_models,

        }


        self._write(
            migrated
        )


        logger.info(
            "Registry migrated backup=%s",
            backup,
        )


        return migrated



    def _save(
        self,
    ) -> None:


        self.data["version"] = (
            REGISTRY_VERSION
        )


        self._write(
            self.data
        )



    def _write(
        self,
        data: dict[str, Any],
    ) -> None:


        with self.registry_file.open(
            "w",
            encoding="utf-8",
        ) as file:


            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False,

            )



    # ==================================================
    # Registration
    # ==================================================

    def register_model(
        self,
        model_path: Path,
        algorithm: str,
        metrics: dict[str, float],
        feature_schema_version: str = FEATURE_SCHEMA_VERSION,
        features: list[str] | None = None,
    ) -> ModelInfo:
        """
        Registriert neues Modell.
        """

        timestamp = datetime.now(
            UTC
        ).strftime(
            "%Y%m%d_%H%M%S_%f"
        )


        filename = (
            f"{MODEL_PREFIX}_"
            f"{timestamp}.pkl"
        )


        target_path = (
            self.models_dir
            /
            filename
        )


        shutil.copy2(
            model_path,
            target_path,
        )


        info = ModelInfo(

            name=filename.replace(
                ".pkl",
                "",
            ),

            filename=filename,

            algorithm=algorithm,

            created_at=datetime.now(
                UTC
            ).isoformat(),

            metrics=metrics,

            feature_schema_version=
                feature_schema_version,

            features=
                features
                or get_feature_names(),

            status="challenger",

        )


        self.data["models"].append(
            asdict(info)
        )


        self._save()


        logger.info(
            "Model registered=%s",
            info.name,
        )


        return info



    # ==================================================
    # Champion Handling
    # ==================================================

    def activate(
        self,
        model_name: str,
    ) -> None:


        found = False


        for model in self.data["models"]:

            if model["name"] == model_name:

                model["status"] = (
                    "champion"
                )


                self.data["champion"] = (
                    model_name
                )


                found = True


            elif model["status"] == "champion":

                model["status"] = (
                    "archived"
                )


        if not found:

            raise ValueError(
                f"Unknown model: {model_name}"
            )


        self._save()


        logger.info(
            "Champion activated=%s",
            model_name,
        )



    def get_champion(
        self,
    ) -> ModelInfo | None:


        champion_name = (
            self.data.get(
                "champion"
            )
        )


        if champion_name is None:

            return None


        for model in self.data["models"]:

            if model["name"] == champion_name:

                model_copy = dict(
                    model
                )


                model_copy.setdefault(
                    "feature_schema_version",
                    FEATURE_SCHEMA_VERSION,
                )


                model_copy.setdefault(
                    "features",
                    get_feature_names(),
                )


                return ModelInfo(
                    **model_copy
                )


        return None



    # ==================================================
    # Evaluation
    # ==================================================

    def promote_best(
        self,
    ) -> ModelInfo | None:


        candidates = [

            model

            for model in self.data["models"]

            if model.get(
                "status"
            )
            !=
            "archived"

        ]


        if not candidates:

            return None



        best = max(

            candidates,

            key=lambda item:

                item.get(
                    "metrics",
                    {},
                ).get(
                    "r2",
                    float("-inf"),
                ),

        )


        self.activate(
            best["name"]
        )


        return ModelInfo(
            **best
        )



    # ==================================================
    # Queries
    # ==================================================

    def list_models(
        self,
    ) -> list[ModelInfo]:


        return [

            ModelInfo(
                **model
            )

            for model in self.data["models"]

        ]



    def rollback(
        self,
        model_name: str,
    ) -> None:


        self.activate(
            model_name
        )


        logger.warning(
            "Rollback executed model=%s",
            model_name,
        )



    # ==================================================
    # Feature Metadata
    # ==================================================

    def get_champion_features(
        self,
    ) -> list[str]:


        champion = (
            self.get_champion()
        )


        if champion is None:

            return []


        return champion.features or []



    def get_feature_schema_version(
        self,
    ) -> str | None:


        champion = (
            self.get_champion()
        )


        if champion is None:

            return None


        return (
            champion.feature_schema_version
        )