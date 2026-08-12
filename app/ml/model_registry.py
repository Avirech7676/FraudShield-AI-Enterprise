import os
import shutil
from pathlib import Path
from datetime import datetime, UTC

from pymongo.errors import PyMongoError
from typing import List, Dict, Any
from app.config.logging_config import logger
from app.database.connection import MongoDBConnection


from app.database.connection import LazyCollection


class ModelRegistry:

    def __init__(self):

        self.collection = LazyCollection("model_registry")

        os.makedirs("models", exist_ok=True)


    #########################################################

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

        document = {

            "version": str(version),

            "model_name": str(model_name),

            "accuracy": float(accuracy),

            "precision": float(precision),

            "recall": float(recall),

            "f1_score": float(f1),

            "roc_auc": float(roc_auc),

            "model_path": str(Path(model_path)),

            "status": "REGISTERED",

            "created_at": datetime.now(UTC)

        }

        try:

            self.collection.insert_one(document)

            logger.info(f"Registered {version}"
)

        except PyMongoError as e:

            print(f"MongoDB Registration Failed : {e}")
    #########################################################

    def list_models(self):

        return list(

            self.collection.find(

                {},

                {"_id": 0}

            )

        )

    #########################################################

    def latest_model(self):

        return self.collection.find_one(

            sort=[

                ("created_at", -1)

            ]

        )

    #########################################################

    def production_model(self):

        return self.collection.find_one(

            {

                "status": "PRODUCTION"

            }

        )

    #########################################################

    def deploy(self, version):

        model = self.collection.find_one(

            {

                "version": version

            }

        )

        if model is None:

            print("Model Not Found")

            return False

        source = str(model["model_path"])

        destination = str(

            Path("models") /

            "production_model.joblib"

        )

        if not Path(source).exists():

            print(source)

            print("Model file missing")

            return False

        shutil.copy(

            source,

            destination

        )

        self.collection.update_many(

            {},

            {

                "$set": {

                    "status": "REGISTERED"

                }

            }

        )

        self.collection.update_one(

            {

                "version": version

            },

            {

                "$set": {

                    "status": "PRODUCTION"

                }

            }

        )

        print(f"{version} deployed")

        return True

    #########################################################

    def rollback(self):

        versions = list(

            self.collection.find().sort(

                "created_at",

                -1

            )

        )

        if len(versions) < 2:

            print("No rollback possible")

            return

        previous = versions[1]

        self.deploy(

            previous["version"]

        )

    #########################################################

    def compare(self, new_auc):

        current = self.production_model()

        if current is None:

            return True

        return new_auc > current["roc_auc"]
