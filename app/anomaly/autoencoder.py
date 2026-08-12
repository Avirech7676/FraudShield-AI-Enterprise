import os

import joblib
import numpy as np
from sklearn.neural_network import MLPRegressor


class AutoencoderAnomalyDetector:
    def __init__(self, model_path="models/autoencoder_anomaly.joblib"):
        self.model_path = model_path
        self.model = None
        self.threshold = None

    def train(self, X):
        self.model = MLPRegressor(
            hidden_layer_sizes=(32, 12, 32),
            activation="relu",
            random_state=42,
            max_iter=300
        )
        self.model.fit(X, X)
        errors = self.reconstruction_error(X)
        self.threshold = float(np.percentile(errors, 99.8))
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(
            {
                "model": self.model,
                "threshold": self.threshold
            },
            self.model_path
        )

    def load(self):
        artifact = joblib.load(self.model_path)
        self.model = artifact["model"]
        self.threshold = artifact["threshold"]
        return self

    def reconstruction_error(self, X):
        reconstructed = self.model.predict(X)
        return np.mean(np.square(X - reconstructed), axis=1)

    def anomaly_score(self, X):
        errors = self.reconstruction_error(X)
        if not self.threshold:
            return np.zeros(len(errors))
        return np.clip((errors / self.threshold) * 100, 0, 100)

    def predict(self, X):
        scores = self.anomaly_score(X)
        return np.where(scores >= 100, -1, 1), scores
