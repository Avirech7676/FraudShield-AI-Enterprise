import xgboost as xgb
import numpy as np

class XGBoostModel:
    """Simple wrapper around XGBClassifier for binary fraud detection."""

    def __init__(self, **params):
        # Default parameters can be tuned later
        self.model = xgb.XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            use_label_encoder=False,
            n_estimators=200,
            learning_rate=0.1,
            max_depth=6,
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
            raise RuntimeError("XGBoostModel not fitted.")
        # Returns shape (n_samples, 2) with probability of class 1 in column 1
        proba = self.model.predict_proba(X)
        return proba
