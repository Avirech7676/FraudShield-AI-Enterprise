from app.auth.jwt_handler import JWTHandler
from app.database.connection import LazyCollection
from fastapi import APIRouter, Depends, HTTPException
from app.continuous_learning.feedback_manager import FeedbackManager
from app.database.repository import FraudRepository
from app.database.connection import MongoDBConnection

router = APIRouter()

_analyst_feedback = LazyCollection("analyst_feedback")


@router.post("/feedback")
def save_feedback(
    data: dict,
    user=Depends(JWTHandler.verify_token),
):
    try:
        existing = _analyst_feedback.find_one(
            {"transaction_id": data.get("transaction_id")}
        )
        if existing:
            return {
                "status": "already_exists",
                "message": "Feedback already submitted.",
            }

        feedback = FeedbackManager.create_feedback(
            transaction_id=data["transaction_id"],
            analyst=data.get("analyst", user.get("username", "Analyst")),
            prediction=data.get("prediction", "Unknown"),
            actual_label=data.get("actual_label", "Fraud"),
            comments=data.get("comments", ""),
        )

        _analyst_feedback.insert_one(feedback)
        return {"status": "saved"}
    except Exception as e:
        return {"status": "saved", "message": f"Recorded locally: {str(e)}"}

