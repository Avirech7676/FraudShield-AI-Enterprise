import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

from app.continuous_learning.model_registry import ModelRegistry
from app.continuous_learning.version_manager import VersionManager
from app.database.connection import LazyCollection, MongoDBConnection
from app.features.feature_engineering import FeatureEngineering
from app.ml.preprocessing import DataPreprocessor
from app.ml.trainer import EnterpriseFraudTrainer


class RetrainingEngine:
    """
    Continuous Learning Retraining Engine
    Pulls feedback, joins it with raw transaction parameters, and refits the ensemble model.
    """
    def __init__(self):
        self._feedback = LazyCollection("analyst_feedback")
        self._transactions = LazyCollection("transactions")

    def feedback_count(self):
        return self._feedback.count_documents({})

    def should_retrain(self, threshold=10):
        # We allow a lower threshold (e.g. 10) for continuous trigger
        return self.feedback_count() >= threshold

    def load_feedback_dataset(self):
        # 1. Fetch analyst feedback records
        feedback_records = list(self._feedback.find({}, {"_id": 0}))

        if not feedback_records:
            return pd.DataFrame()
            
        # 2. For each feedback, fetch the corresponding transaction features from 'transactions' collection
        rows = []
        for fb in feedback_records:
            tx_id = fb.get("transaction_id")
            actual_label = fb.get("actual_label")
            
            tx = self._transactions.find_one({"transaction_id": tx_id}, {"_id": 0})
            if tx and "request" in tx:
                # Merge transaction features with the actual label
                data = tx["request"].copy()
                data["Class"] = 1 if actual_label in ["Fraud", "fraud", 1] else 0
                rows.append(data)
                
        return pd.DataFrame(rows)

    def retrain(self):
        print("Checking retraining conditions...")
        # For demonstration/UI triggering, we allow training if there is at least 1 record in feedback
        if not self.should_retrain(threshold=1):
            print("Retraining threshold not reached (needs at least 1 feedback record).")
            return False

        print("=" * 60)
        print("STARTING MODEL RETRAINING WITH ANALYST FEEDBACK")
        print("=" * 60)

        # 1. Load feedback-enriched transactions
        feedback_df = self.load_feedback_dataset()
        if feedback_df.empty:
            print("No matching transaction records found in database for current feedback.")
            return False

        # 2. Load the base historical dataset (fraud.csv)
        base_path = "data/fraud.csv"
        if not os.path.exists(base_path):
            print(f"Base dataset not found at {base_path}. Retraining solely on feedback data.")
            full_df = feedback_df
        else:
            print("Loading historical dataset for reference...")
            base_df = pd.read_csv(base_path)
            
            # Enrich base_df using FeatureEngineering
            engineer = FeatureEngineering(base_df)
            enriched_base = engineer.run_pipeline()
            
            # Prepare feedback df to match the exact same feature pipeline format
            fb_engineer = FeatureEngineering(feedback_df)
            enriched_fb = fb_engineer.run_pipeline()
            
            # Ensure Class is present in feedback dataframe
            if "Class" not in enriched_fb.columns:
                enriched_fb["Class"] = feedback_df["Class"]
                
            # Align columns
            common_cols = [col for col in enriched_base.columns if col in enriched_fb.columns]
            full_df = pd.concat([enriched_base[common_cols], enriched_fb[common_cols]], ignore_index=True)

        print(f"Merged retraining dataset shape: {full_df.shape}")

        # 3. Preprocess and split
        prep = DataPreprocessor(target_column="Class")
        X_train, X_test, y_train, y_test = prep.split_dataset(full_df)
        
        prep.identify_columns(X_train)
        prep.build_pipeline()
        
        X_train = prep.fit_transform(X_train)
        X_test = prep.transform(X_test)
        
        # Balance dataset via SMOTE
        X_train, y_train = prep.balance_dataset(X_train, y_train)
        prep.save_preprocessor()

        # 4. Trigger training
        trainer = EnterpriseFraudTrainer()
        try:
            raw_feature_names = prep.preprocessor.get_feature_names_out()
            feature_names = [f.replace("numeric__", "").replace("categorical__", "") for f in raw_feature_names]
        except Exception:
            feature_names = None

        trainer.run_training_pipeline(
            X_train,
            y_train,
            X_test,
            y_test,
            feature_names=feature_names
        )

        print("=" * 60)
        print("CONTINUOUS LEARNING MODEL RETRAIN COMPLETED")
        print("=" * 60)
        return True
