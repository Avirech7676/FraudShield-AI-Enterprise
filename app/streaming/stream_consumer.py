import pandas as pd

from app.inference.predictor import EnterpriseFraudPredictor

from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository


class StreamConsumer:

    def __init__(self):

        self.predictor = EnterpriseFraudPredictor()
        db = MongoDBConnection().connect()
        self.repository = FraudRepository(db)

    def consume(self, transaction):

        df = pd.DataFrame([transaction])
        prediction = self.predictor.predict_single(df)

        self.repository.save_transaction(transaction)

        self.repository.save_prediction({
            "transaction_id": transaction["transaction_id"],
            "prediction": prediction["Prediction"],
            "fraud_probability": prediction["Fraud_Probability"],
            "risk_score": prediction["Risk_Score"],
            "risk_tier": prediction["Risk_Tier"]
        })

        if prediction["Risk_Score"] >= 80:
            self.repository.save_alert({
                "transaction_id": transaction["transaction_id"],
                "priority": "P1",
                "status": "OPEN"
            })

        self.repository.save_audit_log({
            "transaction_id": transaction["transaction_id"],
            "action": "Streaming Prediction"
        })

        return prediction