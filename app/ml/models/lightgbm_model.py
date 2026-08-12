import lightgbm as lgb
import numpy as np

class LightGBMModel:
    """Simple wrapper for LightGBM binary classification."""

    def __init__(self, params=None):
        self.params = params or {
            "objective": "binary",
            "metric": "binary_logloss",
            "verbosity": -1,
        }
        self.model = None

    def fit(self, X, y):
        dtrain = lgb.Dataset(X, label=y)
        self.model = lgb.train(self.params, dtrain)
        return self

    def predict_proba(self, X):
        if self.model is None:
            raise RuntimeError("Model not trained")
        # LightGBM returns probability of positive class directly
        proba = self.model.predict(X)
        # Ensure shape (n_samples, 2)
        proba = np.vstack([1 - proba, proba]).T
        return proba
