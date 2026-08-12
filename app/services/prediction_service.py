import traceback
from uuid import uuid4
from datetime import datetime, UTC
import pandas as pd
from fastapi import HTTPException

from app.services.audit_log_service import AuditLogService, AuditAction
from app.case_management.case_manager import CaseManager
from app.notifications.notification_manager import NotificationManager
from app.monitoring.prometheus import async_time_prediction
from app.alerts.service import create_alert
from app.cases.service import create_case
from app.config.logging_config import logger

class PredictionService:

    def __init__(
        self,
        predictor,
        repository,
        risk_engine,
        shap_explainer,
        llm_reporter
    ):
        self.predictor = predictor
        self.repository = repository
        self.risk_engine = risk_engine
        self.shap_explainer = shap_explainer
        self.llm_reporter = llm_reporter

    async def predict(
        self,
        request_data,
        user,
        build_risk_inputs
    ):
        """Asynchronously process a prediction request."""
        try:
            transaction_id = str(uuid4())
            req_copy = dict(request_data)
            req_copy.pop("additionalProp1", None)
            dataframe = pd.DataFrame([req_copy])

            # Async prediction
            prediction = await async_time_prediction(
                self.predictor.async_predict_single, dataframe
            )

            # Async SHAP explanation
            shap = await self.shap_explainer.async_explain_transaction(dataframe)
            top_factors = shap.get("top_factors", []) if isinstance(shap, dict) else []

            risk = self.risk_engine.evaluate(
                **build_risk_inputs(
                    req_copy,
                    prediction
                )
            )

            explanation = self.llm_reporter.explain_flag(
                req_copy,
                prediction,
                risk,
                top_factors
            )

            # Persist transaction and prediction data
            self.repository.save_transaction({
                "transaction_id": transaction_id,
                "request": req_copy,
                "model_features": req_copy,
                "created_at": datetime.now(UTC)
            })

            self.repository.save_prediction({
                "transaction_id": transaction_id,
                "prediction": prediction.get("Prediction", "Genuine"),
                "fraud_probability": prediction.get("Fraud_Probability", 0),
                "risk_score": prediction.get("Risk_Score", 0),
                "risk_tier": prediction.get("Risk_Tier", "Low"),
                "enterprise_risk_score": risk.get("Risk Score", 0),
                "enterprise_risk_tier": risk.get("Risk Tier", "Low"),
                "Latency_ms": prediction.get("Latency_ms", 0),
                "merchant": req_copy.get("Merchant", ""),
                "country": req_copy.get("Country", ""),
                "llm_explanation": explanation,
                "created_at": datetime.now(UTC),
                "customer_id": req_copy.get("Customer_Id", ""),
                "amount": req_copy.get("Amount", 0)
            })

            # Alert and case creation for high-risk predictions
            try:
                pred_flag = prediction.get("Prediction") if isinstance(prediction, dict) else None
                risk_score_val = risk.get("Risk Score", 0)
                risk_tier = risk.get("Risk Tier", "")
                if pred_flag == "Fraud" or (isinstance(risk_score_val, (int, float)) and risk_score_val >= 50) or risk_tier in ["High", "Critical", "Medium"]:
                    alert_id = create_alert({
                        "transaction_id": transaction_id,
                        "prediction": pred_flag,
                        "risk_score": risk_score_val,
                        "risk_tier": risk.get("Risk Tier"),
                        "priority": risk.get("Priority", "P1"),
                        "assigned_to": "",
                        "status": "Open"
                    })
                    try:
                        create_case({
                            "case_id": f"CASE-{transaction_id}",
                            "transaction_id": transaction_id,
                            "alert_id": alert_id,
                            "prediction": pred_flag,
                            "risk_score": risk_score_val,
                            "risk_tier": risk.get("Risk Tier"),
                            "priority": risk.get("Priority", "P1")
                        })
                    except Exception:
                        logger.exception("Failed to create case for alert")
                    NotificationManager.notify({
                        "transaction_id": transaction_id,
                        "prediction": pred_flag,
                        "risk_score": risk_score_val,
                        "priority": risk.get("Priority", "P1")
                    })
            except Exception:
                logger.exception("Failed to create alert for prediction")

            try:
                await self.repository.save_audit_log({
                    "transaction_id": transaction_id,
                    "user": user,
                    "action": "Prediction Requested"
                })
            except Exception:
                pass

            return {
                "transaction_id": transaction_id,
                "prediction": prediction,
                "risk_analysis": risk,
                "top_factors": top_factors,
                "llm_explanation": explanation
            }
        except Exception as e:
            traceback.print_exc()
            logger.exception(f"Prediction Service Failed: {e}")
            raise
