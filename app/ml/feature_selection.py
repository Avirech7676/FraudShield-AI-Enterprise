from sklearn.feature_selection import SelectKBest, mutual_info_classif
import joblib
import pandas as pd
import os


class FeatureSelector:

    def __init__(self, k=20):
        self.k = k
        self.selector = None
        self.selected_features = None

    def fit(self, X, y):

        self.selector = SelectKBest(
            score_func=mutual_info_classif,
            k=min(self.k, X.shape[1])
        )

        X_selected = self.selector.fit_transform(X, y)

        if isinstance(X, pd.DataFrame):
            mask = self.selector.get_support()
            self.selected_features = X.columns[mask].tolist()

        return X_selected

    def transform(self, X):

        return self.selector.transform(X)

    def fit_transform(self, X, y):

        return self.fit(X, y)

    def save(self, path="models/feature_selector.joblib"):

        os.makedirs("models", exist_ok=True)

        joblib.dump(self.selector, path)

    def load(self, path="models/feature_selector.joblib"):

        self.selector = joblib.load(path)

        return self.selector

    def get_selected_features(self):

        return self.selected_features
