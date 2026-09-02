from app.ml.model_registry import ModelRegistry
from app.ml.version_manager import VersionManager

registry = ModelRegistry()

models = registry.list_models()

version = VersionManager.next_version(models)

registry.register_model(

    version=version,

    model_name="Random Forest",

    accuracy=0.991,

    precision=0.988,

    recall=0.985,

    f1=0.986,

    roc_auc=0.998,

    model_path="models/best_model.joblib"

)

print()

print(registry.list_models())