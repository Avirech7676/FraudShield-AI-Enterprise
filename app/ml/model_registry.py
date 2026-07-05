import os
import joblib


class ModelRegistry:

    def __init__(self):

        self.models = {}

    ######################################################

    def load_models(self):

        model_folder = "models"

        for file in os.listdir(model_folder):

            if file.endswith(".pkl"):

                name = file.replace(".pkl","")

                self.models[name] = joblib.load(

                    os.path.join(
                        model_folder,
                        file
                    )

                )

        print(f"{len(self.models)} Models Loaded")

        return self.models

    ######################################################

    def get_model(
        self,
        model_name="best_model"
    ):

        return self.models.get(model_name)

    ######################################################

    def list_models(self):

        return list(self.models.keys())