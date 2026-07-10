import os
from uuid import uuid4

import pandas as pd
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.jwt_handler import JWTHandler
from app.api.schemas import PredictionRequest
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.inference.predictor import EnterpriseFraudPredictor
from app.rules.risk_engine import EnterpriseRiskEngine
from app.logging.logger import EnterpriseLogger
from app.notifications.notification_manager import NotificationManager
from app.case_management.case_manager import CaseManager
from app.monitoring.prometheus import ObservabilityMetrics, time_prediction
from app.xai.shap_explainer import SHAPExplainer
from app.ai.groq_report import EnterpriseFraudReporter

router = APIRouter()
FEATURE_NAMES = ["Time", "Amount"] + [f"V{index}" for index in range(1, 29)]
RICH_FEATURE_NAMES = [
    "Amount", "Currency", "Merchant", "Merchant_Category", "Payment_Type",
    "Card_Present", "Chip_Used", "Contactless", "International",
    "Customer_Age", "Customer_Segment", "KYC_Level", "Customer_Lifetime",
    "Avg_Spend", "Monthly_Spend", "Credit_Limit", "Device_Fingerprint",
    "Device_Trust_Score", "Browser", "Operating_System", "Emulator_Detection",
    "Rooted_Device", "Jailbreak_Detection", "IP_Reputation", "VPN_Detection",
    "TOR_Detection", "ASN", "Country", "City", "ISP",
    "Transactions_Last_Hour", "Transactions_Last_Day", "Velocity",
    "Time_Since_Last_Transaction", "Merchant_Diversity", "Location_Jump",
    "Device_Change", "Password_Reset", "Login_Failure_Count",
    "Merchant_Risk", "Merchant_Chargeback_Rate", "Merchant_Country",
    "Previous_Fraud",
]
PREDICTION_LIMIT = 200
optional_security = HTTPBearer(auto_error=False)


def clean_mongo_rows(rows):

    for item in rows:
        item.pop("_id", None)
        item.setdefault("prediction", item.get("Prediction"))
        item.setdefault("fraud_probability", item.get("Fraud_Probability"))
        item.setdefault("risk_score", item.get("Risk_Score"))
        item.setdefault("risk_tier", item.get("Risk_Tier"))

    return rows


def optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(optional_security)):
    if credentials is None:
        return {
            "sub": "anonymous",
            "role": "Analyst"
        }

    payload = JWTHandler.verify_token(credentials.credentials)
    if payload:
        return payload

    return {
        "sub": "clerk_user",
        "role": "Admin"
    }


def build_model_payload(data):
    amount = float(data.get("Amount") or 0)
    payload = {
        "Time": float(data.get("Time") or 0),
        "Amount": amount,
    }

    for index in range(1, 29):
        key = f"V{index}"
        payload[key] = float(data.get(key) or 0)

    if not any(payload[f"V{index}"] for index in range(1, 29)):
        payload["V1"] = amount / 10000
        payload["V2"] = float(data.get("Transactions_Last_Hour") or 0) / 10
        payload["V3"] = float(data.get("Merchant_Risk") or 0) / 100
        payload["V4"] = (100 - float(data.get("Device_Trust_Score") or 80)) / 100
        payload["V5"] = float(data.get("IP_Reputation") or 0) / 100
        payload["V6"] = 1.0 if data.get("International") else 0.0
        payload["V7"] = 1.0 if data.get("VPN_Detection") or data.get("TOR_Detection") else 0.0
        payload["V8"] = 1.0 if data.get("Location_Jump") else 0.0
        payload["V9"] = 1.0 if data.get("Device_Change") else 0.0
        payload["V10"] = float(data.get("Login_Failure_Count") or 0) / 10

    return payload


def build_risk_inputs(data, prediction):
    amount = float(data.get("Amount") or 0)
    rule_score = min(
        100,
        (25 if amount >= 1000 else 0)
        + (20 if data.get("International") else 0)
        + (20 if data.get("VPN_Detection") or data.get("TOR_Detection") else 0)
        + (15 if data.get("Card_Present") is False else 0)
        + min(float(data.get("Login_Failure_Count") or 0) * 5, 20)
    )
    behavior_score = min(
        100,
        float(data.get("Velocity") or 0)
        + float(data.get("Transactions_Last_Hour") or 0) * 8
        + float(data.get("Transactions_Last_Day") or 0) * 1.5
        + (20 if data.get("Location_Jump") else 0)
        + (15 if data.get("Device_Change") else 0)
    )
    anomaly_score = max(
        float(data.get("IP_Reputation") or 0),
        70 if data.get("Emulator_Detection") or data.get("Rooted_Device") or data.get("Jailbreak_Detection") else 0
    )
    geo_risk = 65 if data.get("International") or data.get("Country") not in (None, "", "US", "IN") else 10

    return {
        "ml_probability": prediction["Fraud_Probability"],
        "rule_score": rule_score,
        "behavior_score": behavior_score,
        "anomaly_score": anomaly_score,
        "device_trust": float(data.get("Device_Trust_Score") or 80),
        "geo_risk": geo_risk,
        "merchant_risk": float(data.get("Merchant_Risk") or 20),
        "fraud_history": min(float(data.get("Previous_Fraud") or 0) * 25, 100),
    }

# =====================================================
# Load Services Once
# =====================================================

predictor = EnterpriseFraudPredictor()
risk_engine = EnterpriseRiskEngine()
shap_explainer = SHAPExplainer()
llm_reporter = EnterpriseFraudReporter()

db = MongoDBConnection().connect()
repository = FraudRepository(db)

# =====================================================
# Health Check
# =====================================================

@router.get("/health")
def health():

    return {

        "status": "healthy",

        "model": "Loaded"

    }


# =====================================================
# Single Prediction
# =====================================================

@router.post("/predict")
def predict(request: PredictionRequest, user = Depends(optional_user)):

    try:
        # ------------------------------------------
        # Transaction ID
        # ------------------------------------------
        transaction_id = str(uuid4())

        # ------------------------------------------
        # Request
        # ------------------------------------------
        data = request.model_dump()
        df = pd.DataFrame([data])

        # ------------------------------------------
        # Prediction
        # ------------------------------------------
        prediction = time_prediction(predictor.predict_single, df)

        # ------------------------------------------
        # SHAP Explanation & Top Factors
        # ------------------------------------------
        shap_explanation = shap_explainer.explain_transaction(df)
        top_factors = shap_explanation.get("top_factors", [])

        EnterpriseLogger.info(
            f"Prediction Generated | "
            f"Transaction={transaction_id} | "
            f"Prediction={prediction['Prediction']} | "
            f"Risk={prediction['Risk_Score']}"
        )

        # ------------------------------------------
        # Risk Engine
        # ------------------------------------------
        risk = risk_engine.evaluate(**build_risk_inputs(data, prediction))

        # ------------------------------------------
        # LLM Flag Explanation
        # ------------------------------------------
        llm_explanation = llm_reporter.explain_flag(data, prediction, risk, top_factors)

        # ------------------------------------------
        # Database
        # ------------------------------------------
        repository.save_transaction({
            "transaction_id": transaction_id,
            "request": data,
            "model_features": data
        })

        repository.save_prediction({
            "transaction_id": transaction_id,
            "prediction": prediction["Prediction"],
            "fraud_probability": prediction["Fraud_Probability"],
            "risk_score": prediction["Risk_Score"],
            "risk_tier": prediction["Risk_Tier"],
            "enterprise_risk_score": risk["Risk Score"],
            "enterprise_risk_tier": risk["Risk Tier"],
            "Latency_ms": prediction["Latency_ms"],
            "merchant": data.get("Merchant"),
            "country": data.get("Country"),
            "llm_explanation": llm_explanation
        })

        repository.save_audit_log({
            "transaction_id": transaction_id,
            "action": "Prediction Requested",
            "user": user.get("sub", "anonymous") if isinstance(user, dict) else "anonymous"
        })

        # ------------------------------------------
        # Alerts & Case Management
        # ------------------------------------------
        if risk["Risk Score"] >= 80:
            repository.save_alert({
                "transaction_id": transaction_id,
                "priority": risk["Priority"],
                "status": "OPEN",
                "risk_score": risk["Risk Score"]
            })
            case = CaseManager.create_case(transaction_id, risk["Priority"])
            # Set the case fields
            case["status"] = "OPEN"
            case["explanation"] = llm_explanation
            case["risk_score"] = risk["Risk Score"]
            repository.save_case(case)
            
            NotificationManager.notify({
                "transaction_id": transaction_id,
                "prediction": prediction["Prediction"],
                "risk_score": risk["Risk Score"],
                "priority": risk["Priority"]
            })

            EnterpriseLogger.warning(
                f"High Risk Alert | "
                f"Transaction={transaction_id} | "
                f"Risk={risk['Risk Score']}"
            )

        EnterpriseLogger.info(
            f"/predict completed successfully | "
            f"Transaction={transaction_id}"
        )

        return {
            "transaction_id": transaction_id,
            "fraud_probability": round(float(prediction["Fraud_Probability"]), 4),
            "risk_score": float(risk["Risk Score"]),
            "tier": risk["Risk Tier"],
            "top_factors": top_factors,
            "llm_explanation": llm_explanation
        }

    except Exception as e:
        ObservabilityMetrics.record_error()
        EnterpriseLogger.error(f"Prediction Failed | {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/batch_predict")
def batch_predict(requests: list[PredictionRequest], user=Depends(optional_user)):

    try:
        results = []

        for request in requests:
            transaction_id = str(uuid4())
            data = request.model_dump()
            df = pd.DataFrame([data])

            prediction = time_prediction(predictor.predict_single, df)

            EnterpriseLogger.info(
                f"Batch Prediction | "
                f"Transaction={transaction_id} | "
                f"Prediction={prediction['Prediction']} | "
                f"Risk={prediction['Risk_Score']}"
            )

            risk = risk_engine.evaluate(**build_risk_inputs(data, prediction))

            repository.save_transaction({
                "transaction_id": transaction_id,
                "request": data,
                "model_features": data
            })

            repository.save_prediction({
                "transaction_id": transaction_id,
                "prediction": prediction["Prediction"],
                "fraud_probability": prediction["Fraud_Probability"],
                "risk_score": prediction["Risk_Score"],
                "risk_tier": prediction["Risk_Tier"],
                "enterprise_risk_score": risk["Risk Score"],
                "enterprise_risk_tier": risk["Risk Tier"],
                "Latency_ms": prediction.get("Latency_ms"),
                "merchant": data.get("Merchant"),
                "country": data.get("Country")
            })

            case = CaseManager.create_case(transaction_id, "P1")
            repository.save_case(case)

            repository.save_audit_log({
                "transaction_id": transaction_id,
                "user": user.get("sub", "anonymous") if isinstance(user, dict) else "anonymous",
                "action": "Batch Prediction Requested"
            })

            if prediction["Risk_Score"] >= 80:
                repository.save_alert({
                    "transaction_id": transaction_id,
                    "priority": "P1",
                    "status": "OPEN",
                    "assigned_to": None,
                    "risk_score": prediction["Risk_Score"],
                    "risk_tier": prediction["Risk_Tier"],
                    "prediction": prediction["Prediction"]
                })

                EnterpriseLogger.warning(
                    f"High Risk Alert | "
                    f"Transaction={transaction_id}"
                )

            results.append({
                "transaction_id": transaction_id,
                "prediction": prediction,
                "risk_analysis": risk,
                "fraud_probability": prediction["Fraud_Probability"],
                "risk_score": risk["Risk Score"],
                "tier": risk["Risk Tier"]
            })

        EnterpriseLogger.info(
            f"Batch Prediction Completed | Records={len(results)}"
        )

        return {
            "total_records": len(results),
            "results": results
        }

    except Exception as e:
        ObservabilityMetrics.record_error()
        EnterpriseLogger.error(f"Batch Prediction Failed | {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/predictions")
def get_predictions():
    return clean_mongo_rows(repository.get_recent_predictions(PREDICTION_LIMIT))


@router.get("/dashboard/summary")
def dashboard_summary():
    total_transactions = repository.count_transactions()
    total_predictions = repository.count_predictions()
    total_alerts = repository.count_alerts()
    fraud_cases = repository.count_predictions({"$or": [{"prediction": "Fraud"}, {"Prediction": "Fraud"}]})
    critical_alerts = repository.count_predictions({"$or": [{"risk_score": {"$gte": 80}}, {"Risk_Score": {"$gte": 80}}]})
    average_risk = repository.average_prediction_value("risk_score")

    return {
        "kpis": {
            "transactions": total_transactions,
            "predictions": total_predictions,
            "fraud_cases": fraud_cases,
            "alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "average_risk": round(average_risk, 2),
            "features_used": len(RICH_FEATURE_NAMES),
            "models_loaded": 1 if predictor.model is not None else 0,
        },
        "risk_tiers": repository.count_predictions_by_fields("risk_tier", "Risk_Tier"),
        "prediction_distribution": repository.count_predictions_by_fields("prediction", "Prediction"),
        "recent_predictions": clean_mongo_rows(repository.get_recent_predictions(12)),
        "model": model_metadata(),
        "features": RICH_FEATURE_NAMES,
    }


@router.get("/model/metadata")
def model_metadata():
    model = predictor.model
    preprocessor = predictor.preprocessor

    return {
        "model_name": type(model).__name__ if model is not None else "Unavailable",
        "preprocessor": type(preprocessor).__name__ if preprocessor is not None else "Unavailable",
        "model_path": predictor.model_path,
        "model_file": os.path.basename(predictor.model_path) if predictor.model_path else "Unavailable",
        "feature_count": len(RICH_FEATURE_NAMES),
        "features": RICH_FEATURE_NAMES,
        "status": "Loaded" if model is not None and preprocessor is not None else "Unavailable",
    }
