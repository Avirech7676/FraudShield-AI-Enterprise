from datetime import datetime


class FeedbackManager:

    @staticmethod
    def create_feedback(

        transaction_id,

        analyst,

        prediction,

        actual_label,

        comments

    ):

        return {

            "transaction_id": transaction_id,

            "analyst": analyst,

            "prediction": prediction,

            "actual_label": actual_label,

            "comments": comments,

            "created_at": datetime.utcnow()

        }