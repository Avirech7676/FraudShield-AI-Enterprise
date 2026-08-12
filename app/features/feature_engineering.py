import pandas as pd
import numpy as np
from app.features.feature_pipeline import FeaturePipeline

class FeatureEngineering:
    """
    Enterprise Feature Engineering Pipeline

    Supports:

    • Batch Training
    • Batch Prediction
    • Real-time Prediction

    Converts raw credit-card transaction records into
    enterprise fraud detection features.

    IMPORTANT:

    This version intentionally removes ALL target leakage.

    The feature engineering process NEVER uses the target
    variable (Class) to generate features.

    Therefore the trained model generalizes correctly.
    """

    ##########################################################

    def __init__(self, dataframe):

        self.df = dataframe.copy()

        np.random.seed(42)

    ##########################################################

    def handle_missing_values(self):

        self.df = self.df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        for column in self.df.columns:

            if self.df[column].dtype == object:

                self.df[column] = (
                    self.df[column]
                    .replace("", np.nan)
                )

        numeric = self.df.select_dtypes(
            include=[np.number]
        ).columns

        if len(numeric):

            self.df[numeric] = (
                self.df[numeric]
                .fillna(
                    self.df[numeric].median()
                )
                .fillna(0)
            )

        categorical = self.df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        ).columns

        for column in categorical:

            mode = self.df[column].mode(
                dropna=True
            )

            value = (
                mode.iloc[0]
                if not mode.empty
                else "Unknown"
            )

            self.df[column] = (
                self.df[column]
                .fillna(value)
            )

        return self.df

    ##########################################################

    def remove_duplicates(self):

        object_columns = self.df.select_dtypes(include=["object"]).columns

        for col in object_columns:
            self.df[col] = self.df[col].apply(
                lambda x: str(x) if isinstance(x, (dict, list, set)) else x
            )

        self.df = self.df.drop_duplicates()

        return self

    ##########################################################

    def enrich_dataset(self):
        """
        Enterprise Feature Enrichment

        Uses the modular FeaturePipeline instead of
        generating features inside this class.
        """

        required = [

            "Device_Trust_Score",

            "VPN_Detection",

            "IP_Reputation"

        ]

        if all(

            column in self.df.columns

            for column in required

        ):

            return self.df

        print(

            "Running Enterprise Feature Pipeline..."

        )

        pipeline = FeaturePipeline()

        self.df = pipeline.run(self.df)

        print("\nColumns after FeaturePipeline:")
        print(self.df.columns.tolist())

        print("\nShape after FeaturePipeline:")
        print(self.df.shape)

        return self.df

    def select_ml_features(self):
            """
            Select features for ML.
            Keep the original credit card dataset features (V1-V28,
            Time, Amount) along with engineered features.
            Only remove high-cardinality identifiers that are not
            useful for training.
            """

            cols_to_drop = [

                "Device_Fingerprint",

                "ASN",

                "City",

                "ISP"

            ]

            clean_df = self.df.drop(

                columns=[

                    col

                    for col in cols_to_drop

                    if col in self.df.columns

                ],

                errors="ignore"

            )

            return clean_df


    def run_pipeline(self):
        print("=" * 60)
        print("RUNNING FEATURE PIPELINE")
        print("=" * 60)
        print("\nInitial Columns")
        print(self.df.columns.tolist())

        self.handle_missing_values()
        print("\nAfter handle_missing_values")
        print(self.df.columns.tolist())

        self.remove_duplicates()
        print("\nAfter Remove_duplicates")
        print(self.df.columns.tolist())

        self.enrich_dataset()
        print("\nAfter enrich_dataset")
        print(self.df.columns.tolist())
        
        print("\nColumns before select_ml_features():")
        print(self.df.columns.tolist())

        self.handle_missing_values()
        self.df = self.select_ml_features()
        self.handle_missing_values()
        print(f"Feature Pipeline Completed. Output shape: {self.df.shape}")
        return self.df
