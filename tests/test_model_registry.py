from app.ml.test_model_registry import ModelRegistry


def test_registry():

    registry = ModelRegistry()

    models = registry.list_models()

    assert isinstance(

        models,

        list

    )