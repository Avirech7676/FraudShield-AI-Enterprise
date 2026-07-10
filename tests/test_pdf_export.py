import os
import pytest
from app.exports.pdf_export import PDFExporter

def test_pdf_export(tmp_path):
    filename = os.path.join(tmp_path, "test_report.pdf")
    
    transaction = {
        "transaction_id": "tx_test_123",
        "Merchant": "Target",
        "Country": "US"
    }
    
    prediction = {
        "Prediction": "Fraud",
        "Fraud_Probability": 0.95,
        "Risk_Score": 95.0,
        "Risk_Tier": "Critical",
        "Latency_ms": 1.5
    }
    
    risk = {
        "Risk Score": 95.0,
        "Risk Tier": "Critical",
        "Recommended Action": "Block Transaction",
        "Priority": "P1",
        "Components": {
            "ML Probability": 95.0,
            "Rule Engine": 80.0,
            "Behavior Engine": 75.0,
            "Anomaly Score": 90.0,
            "Device Trust": 15.0,
            "Geo Risk": 10.0,
            "Merchant Risk": 85.0,
            "Fraud History": 0.0
        }
    }
    
    explanation = {
        "top_factors": [
            {"feature": "Device_Trust_Score", "impact": -0.45},
            {"feature": "VPN_Detection", "impact": 0.35}
        ],
        "explanation_text": "The transaction was flagged due to extremely low device trust score and active VPN routing."
    }
    
    PDFExporter.export_investigation_report(
        transaction=transaction,
        prediction=prediction,
        risk=risk,
        explanation=explanation,
        filename=filename
    )
    
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
