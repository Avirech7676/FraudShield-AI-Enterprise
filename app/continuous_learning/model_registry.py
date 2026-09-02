import os
import shutil
from app.ml.model_registry import ModelRegistry as MLModelRegistry


class ModelRegistry(MLModelRegistry):
    """
    Continuous Learning Model Registry
    Inherits core metadata operations from ML ModelRegistry and adds deployment,
    rollback, and version status management capabilities.
    """

    def register_model(
        self,
        version,
        model_name,
        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        model_path
    ):
        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc
        }
        self.register_model_metadata(version, model_name, metrics, model_path)

    def get_models(self):
        return self.list_models()

    def deploy(self, version):
        model = self.collection.find_one({"version": version})
        if model is None:
            print("Model Not Found")
            return False

        source = model["model_path"]
        destination = "models/production_model.joblib"

        if not os.path.exists(source):
            print(f"Model file missing: {source}")
            return False

        shutil.copy(source, destination)

        self.collection.update_many(
            {},
            {"$set": {"status": "REGISTERED"}}
        )

        self.collection.update_one(
            {"version": version},
            {"$set": {"status": "PRODUCTION"}}
        )

        print(f"Version {version} successfully deployed to production.")
        return True

    def deploy_model(self, version):
        return self.deploy(version)

    def rollback(self):
        versions = list(self.collection.find().sort("created_at", -1))
        if len(versions) < 2:
            print("No rollback possible")
            return
        previous = versions[1]
        self.deploy(previous["version"])

    def compare(self, new_auc):
        current = self.production_model()
        if current is None:
            return True
        return new_auc > current.get("roc_auc", 0)