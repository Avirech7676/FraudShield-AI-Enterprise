from fastapi import APIRouter
from app.services.analytics_service import AnalyticsService
from app.services.prediction_service import PredictionService
from app.monitoring.prometheus import ObservabilityMetrics

router = APIRouter()
analytics_service = AnalyticsService()
prediction_service = PredictionService()

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


def as_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def json_safe(value):
    from bson import ObjectId
    from datetime import date, datetime
    from decimal import Decimal
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def clean_mongo_rows(rows):
    cleaned_rows = []
    for item in rows:
        row = json_safe(dict(item))
        row.pop("_id", None)
        row.setdefault("prediction", row.get("Prediction"))
        row.setdefault("fraud_probability", row.get("Fraud_Probability"))
        row.setdefault("risk_score", row.get("Risk_Score"))
        row.setdefault("risk_tier", row.get("Risk_Tier"))
        row["fraud_probability"] = as_float(row.get("fraud_probability"))
        row["risk_score"] = as_float(row.get("risk_score"))
        cleaned_rows.append(row)
    return cleaned_rows


def empty_dashboard_summary():
    return {
        "kpis": {
            "transactions": 0,
            "predictions": 0,
            "fraud_cases": 0,
            "alerts": 0,
            "critical_alerts": 0,
            "average_risk": 0,
            "features_used": len(RICH_FEATURE_NAMES),
            "models_loaded": 1 if prediction_service.predictor.model is not None else 0,
        },
        "risk_tiers": [],
        "prediction_distribution": [],
        "recent_predictions": [],
        "model": prediction_service.get_model_metadata(),
        "features": RICH_FEATURE_NAMES,
    }


@router.get("/dashboard/summary")
def dashboard_summary():
    try:
        summary = analytics_service.get_dashboard_summary(12)
        model_meta = prediction_service.get_model_metadata()

        return {
            "kpis": {
                "transactions": summary["transactions"],
                "predictions": summary["predictions"],
                "fraud_cases": summary["fraud_cases"],
                "alerts": summary["alerts"],
                "critical_alerts": summary["critical_alerts"],
                "average_risk": summary["average_risk"],
                "features_used": len(RICH_FEATURE_NAMES),
                "models_loaded": 1 if prediction_service.predictor.model is not None else 0,
            },
            "risk_tiers": summary["risk_tiers"],
            "prediction_distribution": summary["prediction_distribution"],
            "recent_predictions": clean_mongo_rows(summary["recent_predictions"]),
            "model": model_meta,
            "features": RICH_FEATURE_NAMES,
        }
    except Exception as exc:
        ObservabilityMetrics.record_error()
        return empty_dashboard_summary()
