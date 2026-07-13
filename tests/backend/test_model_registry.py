from pathlib import Path

import joblib

from backend.model_registry import (
    ModelRegistry,
)


def create_dummy_model(
    tmp_path: Path,
) -> Path:
    """
    Erstellt Dummy-Modell-Datei.
    """

    model_file = tmp_path / "dummy.pkl"

    joblib.dump(
        {
            "model": "dummy"
        },
        model_file,
    )

    return model_file



def test_registry_creates_empty_registry(
    tmp_path,
):

    registry = ModelRegistry(
        tmp_path
    )


    assert registry.data["version"] == 3

    assert registry.data["models"] == []

    assert registry.data["champion"] is None



def test_register_model(
    tmp_path,
):

    model_file = create_dummy_model(
        tmp_path
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        model_path=model_file,

        algorithm="RandomForestRegressor",

        metrics={
            "r2": 0.8
        },

    )


    assert info.filename.endswith(
        ".pkl"
    )


    assert len(
        registry.data["models"]
    ) == 1


    assert (
        tmp_path / info.filename
    ).exists()



def test_activate_sets_champion(
    tmp_path,
):

    model_file = create_dummy_model(
        tmp_path
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        model_path=model_file,

        algorithm="RandomForestRegressor",

        metrics={
            "r2": 0.5
        },

    )


    registry.activate(
        info.name
    )


    champion = registry.get_champion()


    assert champion is not None

    assert champion.name == info.name

    assert champion.status == "champion"



def test_activate_archives_old_champion(
    tmp_path,
):

    model_file = create_dummy_model(
        tmp_path
    )


    registry = ModelRegistry(
        tmp_path
    )


    first = registry.register_model(

        model_path=model_file,

        algorithm="RandomForest",

        metrics={
            "r2":0.4
        },

    )


    second = registry.register_model(

        model_path=model_file,

        algorithm="RandomForest",

        metrics={
            "r2":0.8
        },

    )


    registry.activate(
        first.name
    )

    registry.activate(
        second.name
    )


    models = registry.list_models()


    first_model = next(
        m for m in models
        if m.name == first.name
    )


    second_model = next(
        m for m in models
        if m.name == second.name
    )


    assert first_model.status == "archived"

    assert second_model.status == "champion"



def test_promote_best_uses_highest_r2(
    tmp_path,
):

    model_file = create_dummy_model(
        tmp_path
    )


    registry = ModelRegistry(
        tmp_path
    )


    low = registry.register_model(

        model_file,

        "RandomForest",

        {
            "r2":0.2
        },

    )


    high = registry.register_model(

        model_file,

        "RandomForest",

        {
            "r2":0.9
        },

    )


    result = registry.promote_best()


    assert result.name == high.name


    assert registry.get_champion().name == high.name