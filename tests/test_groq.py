from app.ai.groq_report import EnterpriseFraudReporter


def test_enterprise_fraud_reporter_health():
    reporter = EnterpriseFraudReporter()
    health = reporter.health()
    assert "provider" in health or "status" in health
    assert "connected" in health or "api_configured" in health



def test_enterprise_fraud_reporter_fallback():
    reporter = EnterpriseFraudReporter()
    features = {"amount": 500, "merchant": "Online Store", "V1": 0.5}
    prediction = {"Prediction": "Fraud", "Fraud_Probability": 0.88, "Risk_Tier": "HIGH"}
    report = reporter.generate_report(features, prediction)
    assert isinstance(report, str)
    assert len(report) > 0
