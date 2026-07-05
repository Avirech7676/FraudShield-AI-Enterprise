import os
import joblib
import numpy as np
import pandas as pd

from app.features.feature_engineering import FeatureEngineering


class EnterpriseFraudPredictor:

    def __init__(self):

        self.model_path = "models/best_model.joblib"
        self.preprocessor_path = "models/preprocessor.joblib"

        self.model = None
        self.preprocessor = None

        self.load_artifacts()

    #########################################################

    def load_artifacts(self):

        print("=" * 60)
        print("LOADING TRAINED ARTIFACTS")
        print("=" * 60)

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                "best_model.joblib not found."
            )

        if not os.path.exists(self.preprocessor_path):
            raise FileNotFoundError(
                "preprocessor.joblib not found."
            )

        self.model = joblib.load(self.model_path)

        self.preprocessor = joblib.load(self.preprocessor_path)

        print("Model Loaded Successfully")

        print("Preprocessor Loaded Successfully")

    #########################################################

    def preprocess(self, dataframe):

      engineer = FeatureEngineering(dataframe)

      dataframe = engineer.run_pipeline()

      if "Class" in dataframe.columns:
        dataframe = dataframe.drop(columns=["Class"])

      transformed = self.preprocessor.transform(dataframe)

      return transformed

    #########################################################

    def calculate_risk(self, probability):

        score = probability * 100

        if score < 20:
            tier = "Very Low"

        elif score < 40:
            tier = "Low"

        elif score < 60:
            tier = "Medium"

        elif score < 80:
            tier = "High"

        else:
            tier = "Critical"

        return score, tier

    #########################################################

    def predict_single(self, dataframe):

        processed = self.preprocess(
            dataframe
        )

        probability = self.model.predict_proba(
            processed
        )[0][1]

        prediction = self.model.predict(
            processed
        )[0]

        score, tier = self.calculate_risk(
            probability
        )

        result = {

            "Prediction":
                "Fraud"
                if prediction == 1
                else "Genuine",

            "Fraud_Probability":
                round(float(probability), 4),

            "Risk_Score":
                round(float(score), 2),

            "Risk_Tier":
                tier

        }

        return result

    #########################################################

    def predict_batch(self, dataframe):

        processed = self.preprocess(
            dataframe
        )

        probabilities = self.model.predict_proba(
            processed
        )[:, 1]

        predictions = self.model.predict(
            processed
        )

        results = []

        for pred, prob in zip(
            predictions,
            probabilities
        ):

            score, tier = self.calculate_risk(prob)

            results.append({

                "Prediction":
                    "Fraud"
                    if pred == 1
                    else "Genuine",

                "Fraud_Probability":
                    round(float(prob), 4),

                "Risk_Score":
                    round(float(score), 2),

                "Risk_Tier":
                    tier

            })

        return pd.DataFrame(results)