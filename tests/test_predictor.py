from app.ml.predictor import FraudPredictor


def test_prediction(sample_transaction):

    predictor = FraudPredictor()

    result = predictor.predict(

        sample_transaction

    )

    assert "Prediction" in result

    assert "Risk_Score" in result

    assert "Risk_Tier" in result

    assert "Confidence" in result

    assert "Recommended_Action" in result
