from app.continuous_learning.retraining_engine import RetrainingEngine

engine = RetrainingEngine()

print(

    "Feedback Records :",

    engine.feedback_count()

)

engine.retrain()
