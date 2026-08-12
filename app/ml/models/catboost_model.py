import catboost
from catboost import CatBoostClassifier

class CatBoostModel:
    """Simple wrapper around CatBoostClassifier for binary fraud detection.
    """
    def __init__(self, **params):
        # Default parameters can be tuned later
        self.model = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            loss_function='Logloss',
            eval_metric='AUC',
            random_seed=42,
            verbose=False,
            **params
        )
        self.fitted = False

    def fit(self, X, y):
        self.model.fit(X, y)
        self.fitted = True
        return self

    def predict_proba(self, X):
        if not self.fitted:
            raise RuntimeError("CatBoostModel not fitted.")
        # Returns shape (n_samples, 2); we take probability of class 1
        return self.model.predict_proba(X)
