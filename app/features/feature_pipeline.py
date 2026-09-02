import pandas as pd
from app.features.feature_engineering import FeatureEngineering


class FeaturePipeline:
    """
    Unified entry point for feature engineering and enrichment.
    Ensures both retraining and inference pipelines transform raw data identically.
    """

    @staticmethod
    def process(df: pd.DataFrame) -> pd.DataFrame:
        pipeline = FeatureEngineering(df)
        return pipeline.run_pipeline()
