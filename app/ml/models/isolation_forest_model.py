import numpy as np
from sklearn.ensemble import IsolationForest

class IsolationForestModel:
    """Wrapper around sklearn IsolationForest for binary fraud detection.
    Returns probability of being an outlier (potential fraud).
    """

    def __init__(self, **params):
        # Default parameters can be overridden via params
        self.model = IsolationForest(
            n_estimators=100,
            contamination='auto',
            random_state=42,
            **params
        )
        self.fitted = False

    def fit(self, X, y=None):
        # IsolationForest is unsupervised; y is ignored
        self.model.fit(X)
        self.fitted = True
        return self

    def predict_proba(self, X):
        if not self.fitted:
            raise RuntimeError("IsolationForestModel not fitted.")
        # Decision function: the lower, the more abnormal
        scores = self.model.decision_function(X)
        # Convert scores to [0,1] probability using min-max scaling
        min_score = np.min(scores)
        max_score = np.max(scores)
        # Avoid division by zero
        if max_score - min_score == 0:
            prob = np.ones_like(scores) * 0.5
        else:
            prob = (scores - min_score) / (max_score - min_score)
        # Return as (n_samples, 2) where column 1 is probability of positive class
        prob = np.vstack([1 - prob, prob]).T
        return prob
