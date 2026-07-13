from pathlib import Path

import joblib
import pytest

from sklearn.ensemble import RandomForestRegressor

from backend.model_loader import (
    ModelLoader,
)

from backend.model_registry import (
    ModelRegistry,
)



def create_random_forest_model(
    path: Path,
):

    model = RandomForestRegressor(
        n_estimators=2,
        random_state=42,
    )

    joblib.dump(
        model,
        path,
    )


    return path



def test_load_active_model_success(
    tmp_path,
):

    model_file = (
        tmp_path / "model.pkl"
    )


    create_random_forest_model(
        model_file
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        model_file,

        "RandomForestRegressor",

        {
            "r2":0.9
        },

    )


    registry.activate(
        info.name
    )


    loader = ModelLoader(
        tmp_path
    )


    model = loader.load_active_model()


    assert isinstance(
        model,
        RandomForestRegressor,
    )



def test_loader_rejects_missing_champion(
    tmp_path,
):

    loader = ModelLoader(
        tmp_path
    )


    with pytest.raises(
        RuntimeError
    ):

        loader.load_active_model()



def test_loader_rejects_missing_file(
    tmp_path,
):

    model_file = (
        tmp_path / "model.pkl"
    )


    create_random_forest_model(
        model_file
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        model_file,

        "RandomForestRegressor",

        {
            "r2":0.5
        },

    )


    registry.activate(
        info.name
    )


    # Produktionsfehler simulieren:
    # registriertes Modell wurde gelöscht

    registered_model = (
        tmp_path /
        info.filename
    )


    registered_model.unlink()



    loader = ModelLoader(
        tmp_path
    )


    with pytest.raises(
        FileNotFoundError
    ):

        loader.load_active_model()



def test_loader_rejects_wrong_model_type(
    tmp_path,
):

    wrong_file = (
        tmp_path / "wrong.pkl"
    )


    joblib.dump(
        {
            "not": "model"
        },
        wrong_file,
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        wrong_file,

        "FakeModel",

        {
            "r2":0.1
        },

    )


    registry.activate(
        info.name
    )


    loader = ModelLoader(
        tmp_path
    )


    with pytest.raises(
        TypeError
    ):

        loader.load_active_model()