from uuid import uuid4

import pandas as pd
from fastapi import APIRouter
from fastapi import Depends
from app.auth.jwt_dependency import verify_token
from app.api.schemas import PredictionRequest
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.inference.predictor import EnterpriseFraudPredictor
from app.rules.risk_engine import EnterpriseRiskEngine
from app.logging.logger import EnterpriseLogger
from app.notifications.notification_manager import NotificationManager

router = APIRouter()

# =====================================================
# Load Services Once
# =====================================================

predictor = EnterpriseFraudPredictor()
risk_engine = EnterpriseRiskEngine()

db = MongoDBConnection().connect()
repository = FraudRepository(db)

# =====================================================
# Health Check
# =====================================================

@router.get("/health")
def health():

    return {

        "status": "Healthy",

        "model": "Loaded"

    }


# =====================================================
# Single Prediction
# =====================================================

@router.post("/predict")
def predict(request: PredictionRequest, user = Depends(verify_token)):

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

        prediction = predictor.predict_single(df)

        EnterpriseLogger.info(

            f"Prediction Generated | "
            f"Transaction={transaction_id} | "
            f"Prediction={prediction['Prediction']} | "
            f"Risk={prediction['Risk_Score']}"

        )

        # ------------------------------------------
        # Risk Engine
        # ------------------------------------------

        risk = risk_engine.evaluate(

            ml_probability=prediction["Fraud_Probability"],

            rule_score=40,

            anomaly_score=30,

            device_trust=80,

            velocity_score=20,

            fraud_history=0

        )

        # ------------------------------------------
        # Database
        # ------------------------------------------

        repository.save_transaction({

            "transaction_id": transaction_id,

            "request": data

        })

        repository.save_prediction({

            "transaction_id": transaction_id,

            "prediction": prediction["Prediction"],

            "fraud_probability": prediction["Fraud_Probability"],

            "risk_score": prediction["Risk_Score"],

            "risk_tier": prediction["Risk_Tier"]

        })

        repository.save_audit_log({
            "transaction_id": transaction_id,
          #  "action": "Prediction Requested"
        })

        # ------------------------------------------
        # Alerts
        # ------------------------------------------

        if prediction["Risk_Score"] >= 80:

            repository.save_alert({

                "transaction_id": transaction_id,

                "priority": "P1",

                "status": "OPEN"

            })
            NotificationManager.notify({

                "transaction_id": transaction_id,

                "prediction": prediction["Prediction"],

                "risk_score": prediction["Risk_Score"]

            })

            EnterpriseLogger.warning(

                f"High Risk Alert | "
                f"Transaction={transaction_id} | "
                f"Risk={prediction['Risk_Score']}"

            )

        EnterpriseLogger.info(

            f"/predict completed successfully | "
            f"Transaction={transaction_id}"

        )

        # ------------------------------------------
        # Response
        # ------------------------------------------

        return {

            "transaction_id": transaction_id,

            "prediction": prediction,

            "risk_analysis": risk

        }

    except Exception as e:

        EnterpriseLogger.error(

            f"Prediction Failed | {str(e)}"

        )

        return {

            "status": "error",

            "message": str(e)

        }


# =====================================================
# Batch Prediction
# =====================================================

@router.post("/batch_predict")
def batch_predict(requests: list[PredictionRequest], user=Depends(verify_token)):

    try:

        results = []

        for request in requests:

            transaction_id = str(uuid4())

            data = request.model_dump()

            df = pd.DataFrame([data])

            prediction = predictor.predict_single(df)

            EnterpriseLogger.info(

                f"Batch Prediction | "
                f"Transaction={transaction_id} | "
                f"Prediction={prediction['Prediction']} | "
                f"Risk={prediction['Risk_Score']}"

            )

            risk = risk_engine.evaluate(

                ml_probability=prediction["Fraud_Probability"],

                rule_score=40,

                anomaly_score=30,

                device_trust=80,

                velocity_score=20,

                fraud_history=0

            )

            repository.save_transaction({

                "transaction_id": transaction_id,

                "request": data

            })

            repository.save_prediction({

                "transaction_id": transaction_id,

                "prediction": prediction["Prediction"],

                "fraud_probability": prediction["Fraud_Probability"],

                "risk_score": prediction["Risk_Score"],

                "risk_tier": prediction["Risk_Tier"]

            })

            repository.save_audit_log({

                "transaction_id": transaction_id,
                "user": user["sub"],
                "role": user["role"],
                "action": "Prediction Requested"
            })

            if prediction["Risk_Score"] >= 80:

                repository.save_alert({
                    "transaction_id": transaction_id,
                    "priority": "P1",
                    "status": "OPEN",
                    "assigned_to:": None,
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

                "risk_analysis": risk

            })

        EnterpriseLogger.info(

            f"Batch Prediction Completed | "
            f"Records={len(results)}"

        )

        return {

            "total_records": len(results),

            "results": results

        }

    except Exception as e:

        EnterpriseLogger.error(

            f"Batch Prediction Failed | {str(e)}"

        )

        return {

            "status": "error",

            "message": str(e)

        }

@router.get("/predictions")
def get_predictions():

    predictions = repository.get_all_predictions()

    for item in predictions:

        item.pop("_id", None)

    return predictions