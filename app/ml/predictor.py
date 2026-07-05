import os
import joblib
import numpy as np
import pandas as pd


class FraudPredictor:

    def __init__(
        self,
        model_path="models/best_model.joblib",
        preprocessor_path="models/preprocessor.joblib"
    ):

        self.model = None
        self.preprocessor = None

        self.model_path = model_path
        self.preprocessor_path = preprocessor_path

        self.load()

    ############################################################

    def load(self):

        if not os.path.exists(self.model_path):

            raise FileNotFoundError(
                f"Model not found : {self.model_path}"
            )

        if not os.path.exists(self.preprocessor_path):

            raise FileNotFoundError(
                f"Preprocessor not found : {self.preprocessor_path}"
            )

        self.model = joblib.load(self.model_path)

        self.preprocessor = joblib.load(
            self.preprocessor_path
        )

        print("Enterprise Prediction Engine Loaded")

    ############################################################

    def preprocess(self, transaction):

        if isinstance(transaction, dict):

            transaction = pd.DataFrame([transaction])

        elif isinstance(transaction, pd.Series):

            transaction = pd.DataFrame([transaction])

        elif not isinstance(transaction, pd.DataFrame):

            raise Exception("Input must be DataFrame or Dictionary")

        return self.preprocessor.transform(transaction)

    ############################################################

    def calculate_risk_tier(
        self,
        probability
    ):

        score = probability * 100

        if score < 20:

            return "Very Low"

        elif score < 40:

            return "Low"

        elif score < 60:

            return "Medium"

        elif score < 80:

            return "High"

        else:

            return "Critical"

    ############################################################

    def recommended_action(
        self,
        tier
    ):

        actions = {

            "Very Low":"Approve",

            "Low":"Approve & Monitor",

            "Medium":"Manual Review",

            "High":"Trigger MFA",

            "Critical":"Block Transaction"

        }

        return actions[tier]

    ############################################################

    def confidence_score(
        self,
        probability
    ):

        probability = float(probability)

        confidence = max(

            probability,

            1 - probability

        )

        return round(confidence * 100,2)

    ############################################################

    def predict(
        self,
        transaction
    ):

        X = self.preprocess(transaction)

        probability = float(

            self.model.predict_proba(X)[0][1]

        )

        prediction = int(

            self.model.predict(X)[0]

        )

        risk_score = round(

            probability * 100,

            2

        )

        tier = self.calculate_risk_tier(

            probability

        )

        confidence = self.confidence_score(

            probability

        )

        result = {

            "Prediction":

                "Fraud"

                if prediction == 1

                else "Legitimate",

            "Fraud_Probability":

                round(probability,4),

            "Risk_Score":

                risk_score,

            "Risk_Tier":

                tier,

            "Confidence":

                confidence,

            "Recommended_Action":

                self.recommended_action(tier)

        }

        return result

    ############################################################

    def batch_predict(
        self,
        dataframe
    ):

        X = self.preprocessor.transform(

            dataframe

        )

        probabilities = self.model.predict_proba(X)[:,1]

        predictions = self.model.predict(X)

        output = dataframe.copy()

        output["Prediction"] = predictions

        output["Fraud_Probability"] = probabilities

        output["Risk_Score"] = probabilities * 100

        output["Risk_Tier"] = output["Fraud_Probability"].apply(

            self.calculate_risk_tier

        )

        output["Recommended_Action"] = output["Risk_Tier"].apply(

            self.recommended_action

        )

        return output