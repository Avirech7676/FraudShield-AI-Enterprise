from datetime import datetime

from bson import ObjectId
from fastapi.testclient import TestClient

import app.api.dashboard_routes as routes
from app.api.main import app


client = TestClient(app)


class FakeRepository:
    def get_recent_predictions(self, limit=200):
        return [
            {
                "_id": ObjectId("64f000000000000000000001"),
                "transaction_id": "txn-1",
                "Prediction": "Fraud",
                "Fraud_Probability": "0.91",
                "Risk_Score": "88",
                "Risk_Tier": "Critical",
                "created_at": datetime(2026, 7, 11, 10, 30),
                "request": {
                    "_id": ObjectId("64f000000000000000000002")
                },
            }
        ][:limit]

    def count_transactions(self, query=None):
        return 1

    def count_predictions(self, query=None):
        return 1

    def count_alerts(self, query=None):
        return 1

    def average_prediction_value(self, field):
        return 88

    def count_predictions_by_fields(self, primary_field, fallback_field):
        return [
            {
                "label": "Fraud",
                "count": 1
            }
        ]


from app.api.prediction_routes import prediction_service
from app.api.dashboard_routes import analytics_service

def test_predictions_route_returns_json():
    fake = FakeRepository()
    routes.repository = fake
    prediction_service.repository = fake
    analytics_service.repository = fake

    response = client.get("/predictions")

    assert response.status_code == 200
    assert response.json()[0]["prediction"] == "Fraud"
    assert response.json()[0]["risk_score"] == 88
    assert "_id" not in response.json()[0]


def test_dashboard_summary_route_returns_json():
    fake = FakeRepository()
    routes.repository = fake
    prediction_service.repository = fake
    analytics_service.repository = fake

    response = client.get("/dashboard/summary")

    assert response.status_code == 200
    assert response.json()["kpis"]["predictions"] == 1
    assert response.json()["recent_predictions"][0]["created_at"] == "2026-07-11T10:30:00"
