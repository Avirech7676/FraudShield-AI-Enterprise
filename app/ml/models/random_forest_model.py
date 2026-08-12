import numpy as np
from sklearn.ensemble import RandomForestClassifier


class RandomForestModel:
    """Simple wrapper around sklearn's RandomForestClassifier for binary fraud detection."""

    def __init__(self, **params):
        # Default parameters can be overridden via params
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            random_state=42,
            **params
        )
        self.fitted = False

    def fit(self, X, y):
        self.model.fit(X, y)
        self.fitted = True
        return self

    def predict_proba(self, X):
        if not self.fitted:
            raise RuntimeError("RandomForestModel not fitted.")
        # Returns probability for both classes; shape (n_samples, 2)
        return self.model.predict_proba(np.asarray(X))
