import os
import time
import joblib
import pandas as pd

from app.features.feature_engineering import FeatureEngineering
from app.config.settings import settings
from app.config.logging_config import logger


class EnterpriseFraudPredictor:

    def __init__(self):

        self.model_path = settings.PRODUCTION_MODEL

        self.preprocessor_path = settings.PREPROCESSOR

        self.model = None

        self.preprocessor = None

        self.load_artifacts()

    #########################################################

    def load_artifacts(self):

        logger.info("=" * 60)
        logger.info("LOADING TRAINED ARTIFACTS")
        logger.info("=" * 60)

        try:

            if not os.path.exists(self.model_path):

                logger.warning(

                    "Production model not found. Trying best model."

                )

                self.model_path = settings.BEST_MODEL

            if not os.path.exists(self.model_path):

                raise FileNotFoundError(

                    f"Model file not found : {self.model_path}"

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

                "Model Loaded Successfully"

            )

            logger.info(

                "Preprocessor Loaded Successfully"

            )

        except Exception as e:

            logger.exception(

                f"Unable to load artifacts : {e}"

            )

            raise

    #########################################################

    def preprocess(self, dataframe):

        try:

            engineer = FeatureEngineering(dataframe)

            dataframe = engineer.run_pipeline()

            if "Class" in dataframe.columns:

                dataframe = dataframe.drop(

                    columns=["Class"]

                )

            transformed = self.preprocessor.transform(

                dataframe

            )

            return transformed

        except Exception as e:

            logger.exception(

                f"Preprocessing Failed : {e}"

            )

            raise

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

        start = time.perf_counter()

        try:

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

            latency = round(

                (time.perf_counter() - start) * 1000,

                2

            )

            logger.info(

                f"Prediction Completed in {latency} ms"

            )

            return {

                "Prediction":

                    "Fraud"

                    if prediction == 1

                    else "Genuine",

                "Fraud_Probability":

                    round(

                        float(probability),

                        4

                    ),

                "Risk_Score":

                    round(

                        float(score),

                        2

                    ),

                "Risk_Tier":

                    tier,

                "Latency_ms":

                    latency

            }

        except Exception as e:

            logger.exception(

                f"Prediction Failed : {e}"

            )

            raise

    #########################################################

    def predict_batch(self, dataframe):

        start = time.perf_counter()

        try:

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

                results.append(

                    {

                        "Prediction":

                            "Fraud"

                            if pred == 1

                            else "Genuine",

                        "Fraud_Probability":

                            round(

                                float(prob),

                                4

                            ),

                        "Risk_Score":

                            round(

                                float(score),

                                2

                            ),

                        "Risk_Tier":

                            tier

                    }

                )

            latency = round(

                (time.perf_counter() - start) * 1000,

                2

            )

            logger.info(

                f"Batch Prediction Completed in {latency} ms"

            )

            return pd.DataFrame(results)

        except Exception as e:

            logger.exception(

                f"Batch Prediction Failed : {e}"
            )
            raise