import sys
import json
import pandas as pd
from app.inference.predictor import EnterpriseFraudPredictor
from app.rules.risk_engine import EnterpriseRiskEngine

def main():
    print("=" * 60)
    print(" FRAUDSHIELD AI ENTERPRISE CLI PREDICTOR ")
    print("=" * 60)

    # Default payload
    default_payload = {
        "Amount": 1200.0,
        "Merchant": "Amazon",
        "Country": "US",
        "VPN_Detection": True,
        "Device_Trust_Score": 25.0
    }

    # Load custom input if provided
    if len(sys.argv) > 1:
        try:
            payload = json.loads(sys.argv[1])
            print("Loaded custom payload from CLI.")
        except Exception as e:
            print(f"Failed to parse JSON argument: {e}. Using default.")
            payload = default_payload
    else:
        print("No input provided. Running with default payload:")
        print(json.dumps(default_payload, indent=4))
        payload = default_payload

    # Initialize predictor
    try:
        predictor = EnterpriseFraudPredictor()
        risk_engine = EnterpriseRiskEngine()
        
        df = pd.DataFrame([payload])
        prediction = predictor.predict_single(df)
        
        # Calculate risk scores
        amount = float(payload.get("Amount") or 0)
        rule_score = min(
            100,
            (25 if amount >= 1000 else 0)
            + (20 if payload.get("International") else 0)
            + (20 if payload.get("VPN_Detection") or payload.get("TOR_Detection") else 0)
            + (15 if payload.get("Card_Present") is False else 0)
            + min(float(payload.get("Login_Failure_Count") or 0) * 5, 20)
        )
        behavior_score = min(
            100,
            float(payload.get("Velocity") or 0)
            + float(payload.get("Transactions_Last_Hour") or 0) * 8
            + (20 if payload.get("Location_Jump") else 0)
        )
        anomaly_score = max(
            float(payload.get("IP_Reputation") or 0),
            70 if payload.get("Emulator_Detection") or payload.get("Rooted_Device") else 0
        )
        geo_risk = 65 if payload.get("International") or payload.get("Country") not in (None, "", "US", "IN") else 10

        risk = risk_engine.evaluate(
            ml_probability=prediction["Fraud_Probability"],
            rule_score=rule_score,
            behavior_score=behavior_score,
            anomaly_score=anomaly_score,
            device_trust=float(payload.get("Device_Trust_Score") or 80),
            geo_risk=geo_risk,
            merchant_risk=float(payload.get("Merchant_Risk") or 20),
            fraud_history=min(float(payload.get("Previous_Fraud") or 0) * 25, 100),
        )

        print("\n" + "=" * 60)
        print(" PREDICTION RESULTS ")
        print("=" * 60)
        print(f"ML Class            : {prediction['Prediction']}")
        print(f"ML Fraud Probability: {prediction['Fraud_Probability'] * 100:.2f}%")
        print(f"Enterprise Risk Score: {risk['Risk Score']}/100")
        print(f"Risk Tier           : {risk['Risk Tier']}")
        print(f"Recommended Action  : {risk['Recommended Action']}")
        print(f"Priority            : {risk['Priority']}")
        print("=" * 60)

    except Exception as e:
        print(f"\nPrediction failed: {e}")
        print("Make sure you have trained a model first by running: python train.py")

if __name__ == "__main__":
    main()
