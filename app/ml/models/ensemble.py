import joblib
import os
from pathlib import Path

from .lightgbm_model import LightGBMModel
from .catboost_model import CatBoostModel
from .xgboost_model import XGBoostModel
from .random_forest_model import RandomForestModel
from .isolation_forest_model import IsolationForestModel
from .autoencoder_model import AutoEncoderModel

class EnsembleModel:
    """Orchestrates training and prediction across multiple models.

    Each model class implements `fit(X, y)` and `predict_proba(X)` returning
    probability of the positive class.
    """

    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.models = {
            "lightgbm": LightGBMModel(),
            "catboost": CatBoostModel(),
            "xgboost": XGBoostModel(),
            "random_forest": RandomForestModel(),
            "isolation_forest": IsolationForestModel(),
            "autoencoder": AutoEncoderModel(),
        }
        self.fitted = False

    def fit(self, X, y):
        """Fit all constituent models and persist them.

        Parameters
        ----------
        X: pandas.DataFrame or np.ndarray
        y: array‑like
        """
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X, y)
            model_path = self.model_dir / f"{name}.pkl"
            joblib.dump(model, model_path)
        self.fitted = True
        return self

    def predict_proba(self, X):
        """Return a dict of probability arrays from each model.
        """
        if not self.fitted:
            raise RuntimeError("Ensemble not fitted. Call .fit() first.")
        probs = {}
        for name, model in self.models.items():
            probs[name] = model.predict_proba(X)[:, 1]
        return probs

    def average_score(self, X):
        """Simple average of positive‑class probabilities across models."""
        probs = self.predict_proba(X)
        avg = sum(probs.values()) / len(probs)
        return avg

    def load_models(self):
        """Load persisted model objects from disk.
        """
        for name in self.models.keys():
            model_path = self.model_dir / f"{name}.pkl"
            if model_path.exists():
                self.models[name] = joblib.load(model_path)
        self.fitted = True
        return self
