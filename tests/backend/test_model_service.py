import joblib
import pytest

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

from backend.model_registry import ModelRegistry
from backend.model_service import ModelService



def create_model_file(
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



def prepare_service(
    tmp_path,
):

    model_file = (
        tmp_path / "model.pkl"
    )

    create_model_file(
        model_file
    )


    registry = ModelRegistry(
        tmp_path
    )


    info = registry.register_model(

        model_file,

        "RandomForestRegressor",

        {
            "r2":0.8
        },

    )


    registry.activate(
        info.name
    )


    service = ModelService(
        tmp_path
    )


    return service, info



def test_get_model_loads_champion(
    tmp_path,
):

    service, _ = prepare_service(
        tmp_path
    )


    model = service.get_model()


    assert isinstance(
        model,
        RandomForestRegressor,
    )



def test_get_model_uses_cache(
    tmp_path,
    monkeypatch,
):

    service, _ = prepare_service(
        tmp_path
    )


    calls = []


    original = (
        service.loader.load_active_model
    )


    def wrapper():

        calls.append(1)

        return original()


    monkeypatch.setattr(

        service.loader,

        "load_active_model",

        wrapper,

    )


    service.get_model()

    service.get_model()


    assert len(calls) == 1



def test_reload_model_forces_new_loading(
    tmp_path,
    monkeypatch,
):

    service, _ = prepare_service(
        tmp_path
    )


    calls = []


    original = (
        service.loader.load_active_model
    )


    def wrapper():

        calls.append(1)

        return original()


    monkeypatch.setattr(

        service.loader,

        "load_active_model",

        wrapper,

    )


    service.get_model()

    service.reload_model()


    assert len(calls) == 2



def test_get_champion_returns_registry_model(
    tmp_path,
):

    service, info = prepare_service(
        tmp_path
    )


    champion = service.get_champion()


    assert champion is not None

    assert champion.name == info.name