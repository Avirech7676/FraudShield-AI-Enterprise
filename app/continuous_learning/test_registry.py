from app.continuous_learning.model_registry import ModelRegistry
from app.continuous_learning.version_manager import VersionManager

registry = ModelRegistry()

models = registry.get_models()

version = VersionManager.next_version(models)

registry.register_model(
    version=version,
    accuracy=0.998,
    precision=0.995,
    recall=0.992,
    f1=0.993,
    roc_auc=0.999,
    model_path="models/retrained_model.pkl"
)
registry.deploy_model(version)
print(registry.get_models())

