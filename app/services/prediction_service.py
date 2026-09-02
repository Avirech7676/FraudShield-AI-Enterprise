import os
import pandas as pd
from uuid import uuid4
from app.config.settings import settings
from app.config.logging_config import logger
from app.ml.predictor import FraudPredictor
from app.rules.risk_engine import EnterpriseRiskEngine
from app.xai.shap_explainer import SHAPExplainer
from app.ai.groq_report import EnterpriseFraudReporter
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.case_management.case_manager import CaseManager
from app.notifications.notification_manager import NotificationManager
from app.monitoring.prometheus import ObservabilityMetrics, time_prediction


def as_float(val, default=0.0):
    try:
        if val in (None, "", "Unknown"):
            return default
        return float(val)
    except (ValueError, TypeError):
        return default


class PredictionService:
    """
    Prediction Service Layer
    Orchestrates the entire end-to-end prediction workflow.
    """

    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.repository = FraudRepository(self.db)
        self.predictor = FraudPredictor()
        self.risk_engine = EnterpriseRiskEngine()
        self.shap_explainer = SHAPExplainer()
        self.llm_reporter = EnterpriseFraudReporter()

    def build_model_payload(self, data):
        amount = as_float(data.get("Amount") or 0)
        payload = {
            "Time": as_float(data.get("Time") or 0),
            "Amount": amount,
        }
        for index in range(1, 29):
            key = f"V{index}"
            payload[key] = as_float(data.get(key) or 0)

        if not any(payload[f"V{index}"] for index in range(1, 29)):
            payload["V1"] = amount / 10000
            payload["V2"] = as_float(data.get("Transactions_Last_Hour") or 0) / 10
            payload["V3"] = as_float(data.get("Merchant_Risk") or 0) / 100
            payload["V4"] = (100 - as_float(data.get("Device_Trust_Score") or 80)) / 100
            payload["V5"] = as_float(data.get("IP_Reputation") or 0) / 100
            payload["V6"] = 1.0 if data.get("International") else 0.0
            payload["V7"] = 1.0 if data.get("VPN_Detection") or data.get("TOR_Detection") else 0.0
            payload["V8"] = 1.0 if data.get("Location_Jump") else 0.0
            payload["V9"] = 1.0 if data.get("Device_Change") else 0.0
            payload["V10"] = as_float(data.get("Login_Failure_Count") or 0) / 10
        return payload

    def build_risk_inputs(self, data, prediction):
        amount = as_float(data.get("Amount") or 0)
        rule_score = min(
            100,
            (25 if amount >= 1000 else 0)
            + (20 if data.get("International") else 0)
            + (20 if data.get("VPN_Detection") or data.get("TOR_Detection") else 0)
            + (15 if data.get("Card_Present") is False else 0)
            + min(as_float(data.get("Login_Failure_Count") or 0) * 5, 20)
        )
        behavior_score = min(
            100,
            as_float(data.get("Velocity") or 0)
            + as_float(data.get("Transactions_Last_Hour") or 0) * 8
            + as_float(data.get("Transactions_Last_Day") or 0) * 1.5
            + (20 if data.get("Location_Jump") else 0)
            + (15 if data.get("Device_Change") else 0)
        )
        anomaly_score = max(
            as_float(data.get("IP_Reputation") or 0),
            70 if data.get("Emulator_Detection") or data.get("Rooted_Device") or data.get("Jailbreak_Detection") else 0
        )
        geo_risk = 65 if data.get("International") or data.get("Country") not in (None, "", "US", "IN") else 10

        return {
            "ml_probability": prediction["Fraud_Probability"],
            "rule_score": rule_score,
            "behavior_score": behavior_score,
            "anomaly_score": anomaly_score,
            "device_trust": as_float(data.get("Device_Trust_Score") or 80),
            "geo_risk": geo_risk,
            "merchant_risk": as_float(data.get("Merchant_Risk") or 20),
            "fraud_history": min(as_float(data.get("Previous_Fraud") or 0) * 25, 100),
        }

    def predict_transaction(self, request_data: dict, user_sub: str, background_tasks=None) -> dict:
        try:
            transaction_id = str(uuid4())
            df = pd.DataFrame([request_data])

            # 1. Run prediction via ML Predictor
            prediction = time_prediction(self.predictor.predict, df)

            # 2. SHAP Explanation & Top Factors
            shap_explanation = self.shap_explainer.explain_transaction(df)
            top_factors = shap_explanation.get("top_factors", [])

            logger.info(
                f"Prediction Generated | Transaction={transaction_id} | "
                f"Prediction={prediction['Prediction']} | Risk={prediction['Risk_Score']}"
            )

            # 3. Risk Engine evaluation
            risk_inputs = self.build_risk_inputs(request_data, prediction)
            risk = self.risk_engine.evaluate(**risk_inputs)

            # 4. Save initial prediction and spawn async flow if needed
            llm_explanation = "LLM explanation is pending."
            if background_tasks:
                # Save prediction first so API client gets immediate response
                self._save_prediction_results(
                    transaction_id, request_data, prediction, risk, llm_explanation, user_sub
                )
                background_tasks.add_task(
                    self._async_post_prediction_flow,
                    transaction_id, request_data, prediction, risk, top_factors, user_sub
                )
            else:
                # Synchronous flow
                llm_explanation = self.llm_reporter.explain_flag(request_data, prediction, risk, top_factors)
                self._save_prediction_results(
                    transaction_id, request_data, prediction, risk, llm_explanation, user_sub
                )
                self._handle_alerts_and_notifications(transaction_id, prediction, risk, llm_explanation)

            model_info = self.get_model_metadata()

            return {
                "transaction_id": transaction_id,
                "prediction": prediction,
                "risk_analysis": risk,
                "model": model_info,
                "features_used": self.build_model_payload(request_data),
                "fraud_probability": round(float(prediction["Fraud_Probability"]), 4),
                "risk_score": float(risk["Risk Score"]),
                "tier": risk["Risk Tier"],
                "top_factors": top_factors,
                "llm_explanation": llm_explanation
            }
        except Exception as e:
            raise ValueError(f"PredictionService error: {e}") from e

    def _async_post_prediction_flow(self, transaction_id, request_data, prediction, risk, top_factors, user_sub):
        try:
            llm_explanation = self.llm_reporter.explain_flag(request_data, prediction, risk, top_factors)
            # Update prediction record with LLM explanation
            self.repository.predictions.update_one(
                {"transaction_id": transaction_id},
                {"$set": {"llm_explanation": llm_explanation}}
            )
            self._handle_alerts_and_notifications(transaction_id, prediction, risk, llm_explanation)
        except Exception as e:
            logger.exception(f"Error in async post-prediction flow for transaction {transaction_id}: {e}")

    def _save_prediction_results(self, transaction_id, request_data, prediction, risk, llm_explanation, user_sub):
        self.repository.save_transaction({
            "transaction_id": transaction_id,
            "request": request_data,
            "model_features": request_data
        })

        self.repository.save_prediction({
            "transaction_id": transaction_id,
            "prediction": prediction["Prediction"],
            "fraud_probability": prediction["Fraud_Probability"],
            "risk_score": prediction["Risk_Score"],
            "risk_tier": prediction["Risk_Tier"],
            "enterprise_risk_score": risk["Risk Score"],
            "enterprise_risk_tier": risk["Risk Tier"],
            "Latency_ms": prediction["Latency_ms"],
            "merchant": request_data.get("Merchant"),
            "country": request_data.get("Country"),
            "llm_explanation": llm_explanation
        })

        self.repository.save_audit_log({
            "transaction_id": transaction_id,
            "action": "Prediction Requested",
            "user": user_sub
        })

    def _handle_alerts_and_notifications(self, transaction_id, prediction, risk, llm_explanation):
        if risk["Risk Score"] >= 80:
            self.repository.save_alert({
                "transaction_id": transaction_id,
                "priority": risk["Priority"],
                "status": "OPEN",
                "risk_score": risk["Risk Score"]
            })
            case = CaseManager.create_case(transaction_id, risk["Priority"])
            case["status"] = "OPEN"
            case["explanation"] = llm_explanation
            case["risk_score"] = risk["Risk Score"]
            self.repository.save_case(case)
            
            NotificationManager.notify({
                "transaction_id": transaction_id,
                "prediction": prediction["Prediction"],
                "risk_score": risk["Risk Score"],
                "priority": risk["Priority"]
            })

            logger.warning(
                f"High Risk Alert | Transaction={transaction_id} | Risk={risk['Risk Score']}"
            )

    def get_model_metadata(self):
        model = self.predictor.model
        preprocessor = self.predictor.preprocessor
        return {
            "model_name": type(model).__name__ if model is not None else "Unavailable",
            "preprocessor": type(preprocessor).__name__ if preprocessor is not None else "Unavailable",
            "model_path": self.predictor.model_path,
            "model_file": os.path.basename(self.predictor.model_path) if self.predictor.model_path else "Unavailable",
            "feature_count": 43,
            "status": "Loaded" if model is not None and preprocessor is not None else "Unavailable",
        }
