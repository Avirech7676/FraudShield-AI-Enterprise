import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.linear_model import LogisticRegression

class AutoencoderAnomalyDetector:
    def __init__(self, hidden_layer_sizes=(32, 16, 32), random_state=42):
        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layer_sizes,
            activation='relu',
            solver='adam',
            max_iter=30,  # fast training
            random_state=random_state,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.max_val = 1.0

    def fit(self, X):
        # Fit only on normal data
        self.model.fit(X, X)
        reconstruction = self.model.predict(X)
        errors = np.mean((X - reconstruction) ** 2, axis=1)
        self.max_val = np.percentile(errors, 99) + 1e-8
        return self

    def score_anomaly(self, X):
        reconstruction = self.model.predict(X)
        errors = np.mean((X - reconstruction) ** 2, axis=1)
        scores = (errors / self.max_val) * 50
        return np.clip(scores, 0, 100)


class IsolationForestAnomaly:
    def __init__(self, random_state=42):
        self.model = IsolationForest(n_estimators=100, random_state=random_state, n_jobs=-1)

    def fit(self, X):
        # Downsample if dataset is too large to fit fast
        if len(X) > 50000:
            idx = np.random.choice(len(X), 50000, replace=False)
            self.model.fit(X[idx])
        else:
            self.model.fit(X)
        return self

    def score_anomaly(self, X):
        scores = -self.model.decision_function(X)
        min_val = -0.3
        max_val = 0.3
        norm_scores = ((scores - min_val) / (max_val - min_val + 1e-8)) * 100
        return np.clip(norm_scores, 0, 100)


class LOFAnomaly:
    def __init__(self):
        self.model = LocalOutlierFactor(n_neighbors=20, novelty=True, n_jobs=-1)

    def fit(self, X):
        # LOF is O(N^2) complexity, downsample to fit fast
        if len(X) > 15000:
            idx = np.random.choice(len(X), 15000, replace=False)
            self.model.fit(X[idx])
        else:
            self.model.fit(X)
        return self

    def score_anomaly(self, X):
        scores = -self.model.decision_function(X)
        min_val = -1.5
        max_val = 1.5
        norm_scores = ((scores - min_val) / (max_val - min_val + 1e-8)) * 100
        return np.clip(norm_scores, 0, 100)


class EnterpriseStackingClassifier:
    """
    Ensemble Meta-Learner
    Combines predictions from LightGBM, CatBoost, XGBoost, RandomForest, and HistGradientBoosting
    with unsupervised anomaly scores (Autoencoder, Isolation Forest, LOF)
    using a Logistic Regression meta-learner.
    """
    def __init__(self, base_models, random_state=42):
        self.base_models = base_models
        self.meta_learner = LogisticRegression(random_state=random_state)
        
        # Anomaly detectors
        self.ae_detector = AutoencoderAnomalyDetector(random_state=random_state)
        self.if_detector = IsolationForestAnomaly(random_state=random_state)
        self.lof_detector = LOFAnomaly()

    def fit(self, X_train, y_train):
        # 1. Fit anomaly detectors on normal data only (y_train == 0)
        X_normal = X_train[y_train == 0]
        print(f"Fitting Autoencoder on {len(X_normal)} normal samples...")
        self.ae_detector.fit(X_normal)
        
        print(f"Fitting Isolation Forest on {len(X_normal)} normal samples...")
        self.if_detector.fit(X_normal)
        
        print(f"Fitting Local Outlier Factor on {len(X_normal)} normal samples...")
        self.lof_detector.fit(X_normal)

        # 2. Fit all supervised base models on the full dataset
        for name, model in self.base_models.items():
            print(f"Fitting base model: {name}...")
            model.fit(X_train, y_train)

        # 3. Create training set for the meta-learner
        meta_features = []
        for name, model in self.base_models.items():
            meta_features.append(model.predict_proba(X_train)[:, 1])

        # Add anomaly scores
        meta_features.append(self.ae_detector.score_anomaly(X_train) / 100.0)
        meta_features.append(self.if_detector.score_anomaly(X_train) / 100.0)
        meta_features.append(self.lof_detector.score_anomaly(X_train) / 100.0)

        X_meta = np.column_stack(meta_features)

        # 4. Fit the meta-learner
        print("Fitting meta-learner...")
        self.meta_learner.fit(X_meta, y_train)
        return self

    def predict_proba(self, X):
        meta_features = []
        for name, model in self.base_models.items():
            meta_features.append(model.predict_proba(X)[:, 1])

        meta_features.append(self.ae_detector.score_anomaly(X) / 100.0)
        meta_features.append(self.if_detector.score_anomaly(X) / 100.0)
        meta_features.append(self.lof_detector.score_anomaly(X) / 100.0)

        X_meta = np.column_stack(meta_features)
        return self.meta_learner.predict_proba(X_meta)

    def predict(self, X):
        probs = self.predict_proba(X)[:, 1]
        return (probs >= 0.5).astype(int)

    def get_anomaly_scores(self, X):
        """
        Returns a dict of anomaly scores for inspection
        """
        return {
            "autoencoder": self.ae_detector.score_anomaly(X),
            "isolation_forest": self.if_detector.score_anomaly(X),
            "lof": self.lof_detector.score_anomaly(X)
        }
