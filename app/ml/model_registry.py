import os
import shutil
import joblib
from datetime import datetime

from app.database.connection import MongoDBConnection


class ModelRegistry:

    def __init__(self):

        self.db = MongoDBConnection().connect()

        self.collection = self.db["model_registry"]

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

            "version": version,

            "model_name": model_name,

            "accuracy": accuracy,

            "precision": precision,

            "recall": recall,

            "f1_score": f1,

            "roc_auc": roc_auc,

            "model_path": model_path,

            "status": "REGISTERED",

            "created_at": datetime.utcnow()

        }

        self.collection.insert_one(document)

        print(f"Registered {version}")

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

        source = model["model_path"]

        destination = "models/production_model.joblib"

        if not os.path.exists(source):

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