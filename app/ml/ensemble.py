import os
import joblib
import pandas as pd

from sklearn.ensemble import VotingClassifier

class EnterpriseEnsemble:

    def __init__(self):
        self.ensemble = None

def build(
    self,
    trained_models
):

    estimators = []
    preferred_models = [
        "Random Forest",
        "XGBoost",
        "LightGBM",
        "CatBoost"

    ]

    for model_name in preferred_models:

        if model_name in trained_models:

            estimators.append(

                (
                    model_name,
                    trained_models[model_name]
                )
            )

    self.ensemble = VotingClassifier(
        estimators=estimators,
        voting="soft",
        n_jobs=-1
    )
    return self.ensemble

# Train Ensemble

def fit(
    self,
    X_train,
    y_train
):
    self.ensemble.fit(
        X_train,
        y_train
    )

    print("Enterprise Ensemble Trained")

    def save(self):

      os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        self.ensemble,
        "models/ensemble.joblib"
    )
    print("Saved Enterprise Ensemble")


    def load(self):
      self.ensemble = joblib.load(
        "models/ensemble.joblib"
    )
    return self.ensemble

def predict(
    self,
    X
):
    probability = self.ensemble.predict_proba(X)[:,1]
    prediction = self.ensemble.predict(X)
    return prediction, probability