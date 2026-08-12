import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from app.ml.ensemble import EnterpriseStackingClassifier

def test_enterprise_stacking_classifier():
    np.random.seed(42)
    X_train = np.random.normal(0, 1, size=(200, 10))
    y_train = np.random.choice([0, 1], size=200, p=[0.9, 0.1])
    
    X_test = np.random.normal(0, 1, size=(20, 10))
    
    base_models = {
        "RF": RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42),
        "LR": LogisticRegression(random_state=42)
    }
    
    clf = EnterpriseStackingClassifier(base_models=base_models, random_state=42)
    clf.fit(X_train, y_train)
    
    probs = clf.predict_proba(X_test)
    preds = clf.predict(X_test)
    
    assert probs.shape == (20, 2)
    assert preds.shape == (20,)
    assert set(preds).issubset({0, 1})
    
    anomaly_scores = clf.get_anomaly_scores(X_test)
    assert "autoencoder" in anomaly_scores
    assert "isolation_forest" in anomaly_scores
    assert "lof" in anomaly_scores
    assert len(anomaly_scores["autoencoder"]) == 20
