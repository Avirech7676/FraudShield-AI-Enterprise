from fastapi import APIRouter

from app.database.connection import MongoDBConnection

from app.database.repository import FraudRepository

from app.continuous_learning.feedback_manager import FeedbackManager

router = APIRouter()

db = MongoDBConnection().connect()

repository = FraudRepository(db)


@router.post("/feedback")
def save_feedback(data: dict):
      existing = db.analyst_feedback.find_one(
           {
                "transaction_id": data["transaction_id"]
            }
      )
      if existing:
           return {
            "status": "already_exists",
            "message": "Feedback already submitted."
      }
      feedback = FeedbackManager.create_feedback(

        transaction_id=data["transaction_id"],

        analyst=data["analyst"],

        prediction=data["prediction"],

        actual_label=data["actual_label"],
        comments=data["comments"]
    )
      repository.save_feedback(
        feedback
    )
      return {
        "status": "saved"
    }
