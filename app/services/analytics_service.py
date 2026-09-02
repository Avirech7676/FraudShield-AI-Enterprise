from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository


class AnalyticsService:
    """
    Analytics Service Layer
    Aggregates statistical metrics and dashboard counts from repositories.
    """

    def __init__(self):
        self.db = MongoDBConnection().connect()
        self.repository = FraudRepository(self.db)

    def get_dashboard_summary(self, limit=12) -> dict:
        total_transactions = self.repository.count_transactions()
        total_predictions = self.repository.count_predictions()
        total_alerts = self.repository.count_alerts()
        
        # Fraud cases query
        fraud_cases = self.repository.count_predictions({
            "$or": [{"prediction": "Fraud"}, {"Prediction": "Fraud"}]
        })
        
        # Critical alerts query (risk score >= 80)
        critical_alerts = self.repository.count_predictions({
            "$or": [{"risk_score": {"$gte": 80}}, {"Risk_Score": {"$gte": 80}}]
        })
        
        # Average risk
        average_risk = self.repository.average_prediction_value("risk_score")

        return {
            "transactions": total_transactions,
            "predictions": total_predictions,
            "fraud_cases": fraud_cases,
            "alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "average_risk": round(average_risk, 2),
            "risk_tiers": self.repository.count_predictions_by_fields("risk_tier", "Risk_Tier"),
            "prediction_distribution": self.repository.count_predictions_by_fields("prediction", "Prediction"),
            "recent_predictions": self.repository.get_recent_predictions(limit),
        }
