import os
from datetime import datetime
from app.database.connection import MongoDBConnection

class MagicMockCursor:
    def __init__(self):
        self.data = []
    def sort(self, *a, **kw):
        return self
    def limit(self, *a, **kw):
        return self
    def __iter__(self):
        return iter(self.data)

class MagicMockCollection:
    def insert_one(self, data): return type("Result", (), {"inserted_id": "mock_id"})()
    def find_one(self, *args, **kwargs): return None
    def find(self, *args, **kwargs): return MagicMockCursor()
    def count_documents(self, *args, **kwargs): return 0
    def aggregate(self, *args, **kwargs): return []
    def delete_one(self, *args, **kwargs): return None
    def delete_many(self, *args, **kwargs): return None
    def update_one(self, *args, **kwargs): return None


class ModelRegistry:
    """
    Model Registry (Machine Learning Layer)
    Manages loading, saving, and querying model artifacts and metadata.
    """

    def __init__(self):
        self.db = MongoDBConnection().connect()
        has_collections = self.db is not None and not isinstance(self.db, dict)
        self.collection = self.db["model_registry"] if has_collections else MagicMockCollection()
        os.makedirs("models", exist_ok=True)

    def register_model_metadata(self, version, model_name, metrics, model_path):
        document = {
            "version": version,
            "model_name": model_name,
            **metrics,
            "model_path": model_path,
            "status": "REGISTERED",
            "created_at": datetime.utcnow()
        }
        self.collection.insert_one(document)
        print(f"Registered model metadata for version {version}")

    def list_models(self):
        return list(self.collection.find({}, {"_id": 0}))

    def latest_model(self):
        return self.collection.find_one(sort=[("created_at", -1)])

    def production_model(self):
        return self.collection.find_one({"status": "PRODUCTION"})