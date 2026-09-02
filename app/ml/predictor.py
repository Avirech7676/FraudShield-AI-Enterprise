import os
import time
import joblib
import pandas as pd
import numpy as np

from app.config.settings import settings
from app.config.logging_config import logger
from app.ml.model_registry import ModelRegistry
from app.ml.version_manager import VersionManager
class FraudPredictor:

    def __init__(self):

        self.registry = ModelRegistry()

        self.model = None
        self.preprocessor = None

        self.model_path = None
        self.preprocessor_path = settings.PREPROCESSOR

        self.model_version = "Development"

        self.load()
    ############################################################

    def load(self):

        logger.info("=" * 60)
        logger.info("Loading Enterprise Prediction Engine")
        logger.info("=" * 60)

        try:

            production = None
            try:
                production = self.registry.production_model()
            except Exception as reg_err:
                logger.warning(
                    f"Model registry query skipped (using default best model): {reg_err}"
                )

            if production:

                self.model_path = production["model_path"]
                self.model_version = production["version"]

                logger.info(
                    f"Using Production Model : {self.model_version}"
                )

            else:

                logger.info(
                    "Using Default Production Artifacts"
                )

                self.model_path = settings.BEST_MODEL

            if not os.path.exists(self.model_path):

                raise FileNotFoundError(
                    f"Model not found : {self.model_path}"
                )

            if not os.path.exists(self.preprocessor_path):

                raise FileNotFoundError(
                    f"Preprocessor not found : {self.preprocessor_path}"
                )

            self.model = joblib.load(
                self.model_path
            )

            self.preprocessor = joblib.load(
                self.preprocessor_path
            )

            logger.info(
                "Prediction Engine Loaded Successfully"
            )

        except Exception as e:

            logger.exception(
                f"Unable to load prediction engine : {e}"
            )

            raise

    ############################################################

    def preprocess(self, transaction):

        try:

            if isinstance(transaction, dict):

                transaction = pd.DataFrame([transaction])

            elif isinstance(transaction, pd.Series):

                transaction = pd.DataFrame([transaction])

            elif not isinstance(transaction, pd.DataFrame):

                raise ValueError(
                    "Input must be DataFrame, Series or Dictionary."
                )

            from app.features.feature_pipeline import FeaturePipeline
            enriched_df = FeaturePipeline.process(transaction)
            if "Class" in enriched_df.columns:
                enriched_df = enriched_df.drop(columns=["Class"])

            # Use DataPreprocessor wrapper instance to handle feature column casting
            from app.ml.preprocessing import DataPreprocessor
            dp = DataPreprocessor()
            dp.preprocessor = self.preprocessor

            transformed = dp.transform(enriched_df)

            return transformed

            return transformed

        except Exception as e:

            logger.exception(
                f"Preprocessing Failed : {e}"
            )
            raise ValueError(f"Preprocessing internal error: {e}") from e
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

    def calculate_risk_tier(self, probability):
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

    def predict(self, transaction):

        start = time.perf_counter()

        try:
            # Ensure float conversion errors are caught with explicit diagnostic
            try:
                X = self.preprocess(transaction)
            except ValueError as ve:
                logger.error(f"Preprocess ValueError: {ve}")
                raise

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

            latency = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            logger.info(
                f"Prediction completed in {latency} ms"
            )

            return {

                "Prediction":
                    "Fraud"
                    if prediction == 1
                    else "Legitimate",

                "Fraud_Probability":
                    round(probability, 4),

                "Risk_Score":
                    risk_score,

                "Risk_Tier":
                    tier,

                "Confidence":
                    confidence,

                "Recommended_Action":
                    self.recommended_action(tier),

                "Model_Version":
                    self.model_version,

                "Latency_ms":
                    latency

            }

        except Exception as e:

            logger.exception(
                f"Prediction Failed : {e}"
            )

            raise ValueError(f"Predict internal error: {e}") from e

    ############################################################

    def batch_predict(self, dataframe):

        start = time.perf_counter()

        try:

            X = self.preprocessor.transform(dataframe)

            probabilities = self.model.predict_proba(X)[:, 1]

            predictions = self.model.predict(X)

            output = dataframe.copy()

            output["Prediction"] = np.where(
                predictions == 1,
                "Fraud",
                "Legitimate"
            )

            output["Fraud_Probability"] = probabilities

            output["Risk_Score"] = probabilities * 100

            output["Risk_Tier"] = output[
                "Fraud_Probability"
            ].apply(
                self.calculate_risk_tier
            )

            output["Recommended_Action"] = output[
                "Risk_Tier"
            ].apply(
                self.recommended_action
            )

            output["Model_Version"] = self.model_version

            latency = round(
                (time.perf_counter() - start) * 1000,
                2
            )

            logger.info(
                f"Batch Prediction Completed ({len(output)} records) in {latency} ms"
            )

            return output

        except Exception as e:

            logger.exception(
                f"Batch Prediction Failed : {e}"
            )

            raise    
        
if __name__ == "__main__":
    ...
