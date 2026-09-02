from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.api.schemas import PredictionRequest
from app.auth.jwt_handler import JWTHandler
from app.services.prediction_service import PredictionService
from app.config.logging_config import logger

router = APIRouter()
prediction_service = PredictionService()
optional_security = HTTPBearer(auto_error=False)


def optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(optional_security)):
    if credentials is None:
        return {"sub": "anonymous", "role": "Analyst"}
    payload = JWTHandler.verify_token(credentials.credentials)
    if payload:
        return payload
    return {"sub": "clerk_user", "role": "Admin"}


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


from app.monitoring.prometheus import ObservabilityMetrics

@router.post("/predict")
def predict(request: PredictionRequest, background_tasks: BackgroundTasks, user=Depends(optional_user)):
    try:
        data = request.model_dump()
        result = prediction_service.predict_transaction(data, user.get("sub", "anonymous"), background_tasks)
        return result
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Prediction route failed: {e}\n{tb}")
        ObservabilityMetrics.record_error()
        return {"status": "error", "message": f"EXPLICIT_FAIL: {e}", "traceback": tb}


@router.post("/batch_predict")
def batch_predict(requests: list[PredictionRequest], background_tasks: BackgroundTasks, user=Depends(optional_user)):
    try:
        results = []
        errors = []
        BATCH_PREDICTION_LIMIT = 50
        for index, req in enumerate(requests[:BATCH_PREDICTION_LIMIT], start=1):
            try:
                data = req.model_dump()
                res = prediction_service.predict_transaction(data, user.get("sub", "anonymous"), background_tasks)
                results.append(res)
            except Exception as row_error:
                ObservabilityMetrics.record_error()
                errors.append({"row": index, "message": str(row_error)})
        return {
            "status": "ok" if not errors else "partial",
            "total_records": len(results),
            "submitted_records": min(len(requests), BATCH_PREDICTION_LIMIT),
            "skipped_records": max(len(requests) - BATCH_PREDICTION_LIMIT, 0),
            "results": results,
            "errors": errors
        }
    except Exception as e:
        ObservabilityMetrics.record_error()
        return {"status": "error", "message": str(e)}


@router.get("/predictions")
def get_predictions():
    try:
        raw_predictions = prediction_service.repository.get_recent_predictions(200)
        return clean_mongo_rows(raw_predictions)
    except Exception as e:
        ObservabilityMetrics.record_error()
        return []
