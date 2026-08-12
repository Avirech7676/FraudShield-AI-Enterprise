import os
import shutil
from datetime import datetime, UTC
from typing import List, Dict, Any

from pymongo.errors import PyMongoError
from app.config.logging_config import logger
from app.database.connection import MongoDBConnection

class AsyncModelRegistry:
    """Async version of ModelRegistry using Motor for non‑blocking MongoDB operations."""

    def __init__(self):
        self.db = None
        self.collection = None
        self._initialized = False

    async def _ensure_connection(self):
        if not self._initialized:
            # Establish async connection via MongoDBConnection
            self.db = await MongoDBConnection().connect()
            self.collection = self.db["model_registry"]
            os.makedirs("models", exist_ok=True)
            self._initialized = True

    async def register_model(
        self,
        version: str,
        model_name: str,
        accuracy: float,
        precision: float,
        recall: float,
        f1: float,
        roc_auc: float,
        model_path: str,
    ) -> None:
        await self._ensure_connection()
        document = {
            "version": str(version),
            "model_name": str(model_name),
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "roc_auc": float(roc_auc),
            "model_path": str(os.path.abspath(model_path)),
            "status": "REGISTERED",
            "created_at": datetime.now(UTC),
        }
        try:
            await self.collection.insert_one(document)
            logger.info(f"Registered model version {version} for {model_name}")
        except PyMongoError as e:
            logger.exception(f"MongoDB registration failed: {e}")
            raise

    async def list_models(self) -> List[Dict[str, Any]]:
        await self._ensure_connection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def latest_model(self) -> Dict[str, Any] | None:
        await self._ensure_connection()
        return await self.collection.find_one(sort=[("created_at", -1)])

    async def production_model(self) -> Dict[str, Any] | None:
        await self._ensure_connection()
        return await self.collection.find_one({"status": "PRODUCTION"})

    async def deploy(self, version: str) -> bool:
        """Promote the given version to PRODUCTION.
        Returns True on success, False if the version does not exist.
        """
        await self._ensure_connection()
        model = await self.collection.find_one({"version": version})
        if model is None:
            logger.warning(f"Model version {version} not found for deployment")
            return False
        source = str(model["model_path"])
        destination = os.path.join("models", "production_model.joblib")
        if not os.path.exists(source):
            logger.error(f"Model file {source} missing; cannot deploy")
            return False
        try:
            shutil.copy(source, destination)
        except Exception as e:
            logger.exception(f"Failed to copy model file during deploy: {e}")
            return False
        await self.collection.update_many({}, {"$set": {"status": "REGISTERED"}})
        await self.collection.update_one({"version": version}, {"$set": {"status": "PRODUCTION"}})
        logger.info(f"Model version {version} deployed as production")
        return True

    async def rollback(self) -> bool:
        """Rollback to the previously deployed model version.
        Returns True if rollback succeeded, False otherwise.
        """
        await self._ensure_connection()
        versions = await self.collection.find().sort("created_at", -1).to_list(length=None)
        if len(versions) < 2:
            logger.warning("No previous model version available for rollback")
            return False
        previous_version = versions[1]["version"]
        return await self.deploy(previous_version)

    async def compare(self, new_auc: float) -> bool:
        """Return True if the new AUC is better than the current production model's AUC."""
        current = await self.production_model()
        if current is None:
            return True
        return new_auc > current.get("roc_auc", 0)
