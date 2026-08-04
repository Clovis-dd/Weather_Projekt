"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Module:
    backend.services.model_service

Description:
    Service Layer für Modellinformationen.

Responsibilities:

    - Champion Modell verwalten
    - Modellstatus liefern
    - Modellinformationen bereitstellen


Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations


# ======================================================
# Standard Library
# ======================================================

from pathlib import Path
from typing import Any


# ======================================================
# Project Imports
# ======================================================

from backend.model_service import (
    ModelService as CoreModelService,
)

from shared.logger import get_logger


# ======================================================
# Logger
# ======================================================

logger = get_logger(
    __name__
)


# ======================================================
# Service
# ======================================================


class ModelInformationService:
    """
    Wrapper Service für das zentrale ModelService.
    """


    def __init__(
        self,
        models_directory: str | Path = "models",
    ) -> None:
        """
        Initialisiert den Model Service.
        """

        self.model_service = CoreModelService(
            Path(models_directory)
        )


    # ==================================================
    # Champion
    # ==================================================

    def get_champion(
        self,
    ):
        """
        Liefert das aktuell aktive Champion Modell.
        """

        return self.model_service.get_champion()



    def is_loaded(
        self,
    ) -> bool:
        """
        Prüft ob ein Champion Modell geladen ist.
        """

        return (
            self.get_champion()
            is not None
        )



    # ==================================================
    # Information
    # ==================================================

    def get_model_information(
        self,
    ) -> dict[str, Any]:
        """
        Liefert Informationen über das aktive Modell.
        """


        champion = self.get_champion()


        if champion is None:

            return self._fallback_information()



        return {

            "name": champion.name,

            "filename": getattr(
                champion,
                "filename",
                None,
            ),

            "algorithm": getattr(
                champion,
                "algorithm",
                None,
            ),

            "metrics": getattr(
                champion,
                "metrics",
                None,
            ),

            "status": "active",

        }



    # ==================================================
    # Compatibility
    # ==================================================

    def is_model_loaded(
        self,
    ) -> bool:
        """
        Kompatibilitätsmethode.
        """

        return self.is_loaded()



    # ==================================================
    # Fallback
    # ==================================================

    @staticmethod
    def _fallback_information() -> dict[str, Any]:
        """
        Information ohne geladenes Modell.
        """

        return {

            "name": None,

            "filename": None,

            "algorithm": None,

            "metrics": None,

            "status": "unknown",

        }