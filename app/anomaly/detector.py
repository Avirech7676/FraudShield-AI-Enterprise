import joblib
import numpy as np
import os

from sklearn.ensemble import IsolationForest


class EnterpriseAnomalyDetector:

    def __init__(self):

        self.model_path = "models/isolation_forest.joblib"

        self.model = None

    ##################################################

    def train(self, X):

        print("Training Isolation Forest...")

        self.model = IsolationForest(

            n_estimators=100,

            contamination=0.002,

            random_state=42,

            n_jobs=-1

        )

        self.model.fit(X)

        joblib.dump(

            self.model,

            self.model_path

        )

        print("Isolation Forest Saved.")

    ##################################################

    def load(self):

        if not os.path.exists(self.model_path):

            raise FileNotFoundError(

                "Isolation Forest model not found."

            )

        self.model = joblib.load(

            self.model_path

        )

    ##################################################

    def anomaly_score(self, X):

        scores = self.model.decision_function(X)

        scores = (1 - scores) * 100

        scores = np.clip(scores, 0, 100)

        return scores

    ##################################################

    def predict(self, X):

        prediction = self.model.predict(X)

        score = self.anomaly_score(X)

        return prediction, score