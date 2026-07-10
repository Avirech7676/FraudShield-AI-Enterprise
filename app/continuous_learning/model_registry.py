import os
import shutil
from datetime import datetime

from app.database.connection import MongoDBConnection


class ModelRegistry:

    def __init__(self):

        self.db = MongoDBConnection().connect()

        self.registry = self.db["model_registry"]

    #########################################################

    def register_model(

        self,

        version,

        accuracy,

        precision,

        recall,

        f1,

        roc_auc,

        model_path

    ):

        model = {

            "version": version,

            "accuracy": accuracy,

            "precision": precision,

            "recall": recall,

            "f1_score": f1,

            "roc_auc": roc_auc,

            "model_path": model_path,

            "status": "REGISTERED",

            "created_at": datetime.utcnow()

        }

        self.registry.insert_one(model)

        print(f"Model {version} Registered")

    #########################################################

    def get_models(self):

        return list(

            self.registry.find({}, {"_id": 0})

        )

    #########################################################

    def latest_model(self):

        return self.registry.find_one(

            sort=[("created_at", -1)]

        )

    #########################################################

    def deploy_model(self, version):

        model = self.registry.find_one(

            {

                "version": version

            }

        )

        if model is None:

            print("Model Not Found")

            return

        ssource = model["model_path"]

        destination = "models/production_model.joblib"

        if not os.path.exists(ssource):
            print(f"Model file not found: {ssource}")
            return
        shutil.copy(ssource, destination)

        self.registry.update_many(

            {},

            {

                "$set": {

                    "status": "REGISTERED"

                }

            }

        )

        self.registry.update_one(

            {

                "version": version

            },

            {

                "$set": {

                    "status": "PRODUCTION"

                }

            }

        )

        print(f"{version} deployed successfully")