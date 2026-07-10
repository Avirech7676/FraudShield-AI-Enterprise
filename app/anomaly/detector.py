import joblib
import numpy as np
import os

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class EnterpriseAnomalyDetector:

    def __init__(self):

        self.model_path = "models/isolation_forest.joblib"
        self.lof_model_path = "models/local_outlier_factor.joblib"

        self.model = None
        self.lof_model = None

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

    def train_lof(self, X):

        print("Training Local Outlier Factor...")

        self.lof_model = LocalOutlierFactor(

            n_neighbors=35,

            contamination=0.002,

            novelty=True

        )

        self.lof_model.fit(X)

        joblib.dump(

            self.lof_model,

            self.lof_model_path

        )

        print("Local Outlier Factor Saved.")

    ##################################################

    def load(self):

        if not os.path.exists(self.model_path):

            raise FileNotFoundError(

                "Isolation Forest model not found."

            )

        self.model = joblib.load(

            self.model_path

        )

        if os.path.exists(self.lof_model_path):

            self.lof_model = joblib.load(

                self.lof_model_path

            )

    ##################################################

    def anomaly_score(self, X):

        scores = self.model.decision_function(X)

        scores = (1 - scores) * 100

        scores = np.clip(scores, 0, 100)

        return scores

    ##################################################

    def lof_score(self, X):

        if self.lof_model is None:

            raise FileNotFoundError(

                "Local Outlier Factor model not loaded."

            )

        scores = self.lof_model.decision_function(X)

        scores = (1 - scores) * 100

        scores = np.clip(scores, 0, 100)

        return scores

    ##################################################

    def predict(self, X):

        prediction = self.model.predict(X)

        score = self.anomaly_score(X)

        return prediction, score
