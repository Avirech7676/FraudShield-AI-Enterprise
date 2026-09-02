from app.ml.predictor import FraudPredictor


class EnterpriseFraudPredictor(FraudPredictor):
    """
    Enterprise Fraud Predictor (Inference Shim)
    Extends FraudPredictor to support the legacy predict_single and predict_batch
    method interfaces while using the consolidated prediction logic under the hood.
    """

    def predict_single(self, transaction):
        # Delegate to unified predict logic
        return self.predict(transaction)

    def predict_batch(self, dataframe):
        # Delegate to unified batch_predict logic
        return self.batch_predict(dataframe)
