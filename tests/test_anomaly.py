import numpy as np
import pytest
from app.ml.ensemble import AutoencoderAnomalyDetector, IsolationForestAnomaly, LOFAnomaly

def test_anomaly_detectors():
    # Create mock data
    np.random.seed(42)
    X_train = np.random.normal(0, 1, size=(100, 10))
    X_normal_test = np.random.normal(0, 1, size=(20, 10))
    X_anomaly_test = np.random.normal(5, 2, size=(5, 10))
    
    # 1. Autoencoder Anomaly Detector
    ae = AutoencoderAnomalyDetector(hidden_layer_sizes=(8, 4, 8), random_state=42)
    ae.fit(X_train)
    scores_normal = ae.score_anomaly(X_normal_test)
    scores_anomaly = ae.score_anomaly(X_anomaly_test)
    assert len(scores_normal) == 20
    assert len(scores_anomaly) == 5
    assert all(0 <= s <= 100 for s in scores_normal)
    
    # 2. Isolation Forest Anomaly
    iforest = IsolationForestAnomaly(random_state=42)
    iforest.fit(X_train)
    scores_if_normal = iforest.score_anomaly(X_normal_test)
    scores_if_anomaly = iforest.score_anomaly(X_anomaly_test)
    assert len(scores_if_normal) == 20
    assert len(scores_if_anomaly) == 5
    
    # 3. LOF Anomaly
    lof = LOFAnomaly()
    lof.fit(X_train)
    scores_lof_normal = lof.score_anomaly(X_normal_test)
    scores_lof_anomaly = lof.score_anomaly(X_anomaly_test)
    assert len(scores_lof_normal) == 20
    assert len(scores_lof_anomaly) == 5
