"""
=========================================================
Weather Analytics & Machine Learning Platform
=========================================================

Script:
    train_weather_model.py

Description:
    Starts the complete machine learning training pipeline.

The complete training implementation resides in:

    training/train_weather_model.py

This script serves as the official project entry point
for model training.

Author:
    Clovis Wassom Leugoué
"""

from __future__ import annotations

import subprocess
import sys

from scripts.bootstrap import initialize

PROJECT_ROOT = initialize()

from shared.logger import get_logger


logger = get_logger(__name__)


def train_weather_model() -> None:
    """
    Execute the complete machine learning training pipeline.
    """

    logger.info(
        "Starting machine learning training..."
    )

    print()

    print("========================================")
    print(" Weather Analytics Platform")
    print(" Machine Learning Training")
    print("========================================")

    print()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "training.train_weather_model",
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print()

    print("========================================")
    print(" Training completed successfully")
    print("========================================")

    print()


if __name__ == "__main__":
    train_weather_model()