import os
import json
import joblib
import warnings
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from app.config.settings import settings
from app.config.logging_config import logger
from app.ml.ensemble import EnterpriseStackingClassifier
from app.continuous_learning.model_registry import ModelRegistry
from app.ml.version_manager import VersionManager

warnings.filterwarnings("ignore")


class EnterpriseFraudTrainer:
    """
    Enterprise Stacking Ensemble Fraud Model Trainer
    """

    def __init__(self):
        logger.info("Initializing Enterprise Stacking Trainer")
        self.results = []
        self.best_model = None
        self.best_model_name = "Enterprise Stacking Ensemble"
        self.best_accuracy = 0
        self.best_precision = 0
        self.best_recall = 0
        self.best_f1 = 0
        self.best_auc = 0
        self.training_time = datetime.now()
        self.registry = ModelRegistry()

        os.makedirs(settings.MODEL_DIRECTORY, exist_ok=True)
        os.makedirs(settings.LOG_DIRECTORY, exist_ok=True)
        os.makedirs("reports", exist_ok=True)

    def train_ensemble(self, X_train, y_train, X_test, y_test):
        logger.info("=" * 60)
        logger.info("TRAINING ENTERPRISE STACKING ENSEMBLE")
        logger.info("=" * 60)

        # 1. Define base models
        base_models = {
            "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
            "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=100, random_state=42),
            "XGBoost": XGBClassifier(eval_metric="logloss", tree_method="hist", random_state=42, n_jobs=-1),
            "LightGBM": LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1),
            "CatBoost": CatBoostClassifier(random_state=42, verbose=False)
        }

        # 2. Instantiate and fit the stacking classifier
        self.best_model = EnterpriseStackingClassifier(base_models=base_models, random_state=42)
        self.best_model.fit(X_train, y_train)

        # 3. Evaluate the ensemble model
        logger.info("Evaluating Ensemble Model on Test Set...")
        predictions = self.best_model.predict(X_test)
        probabilities = self.best_model.predict_proba(X_test)[:, 1]

        self.best_accuracy = accuracy_score(y_test, predictions)
        self.best_precision = precision_score(y_test, predictions, zero_division=0)
        self.best_recall = recall_score(y_test, predictions, zero_division=0)
        self.best_f1 = f1_score(y_test, predictions, zero_division=0)
        self.best_auc = roc_auc_score(y_test, probabilities)

        cm = confusion_matrix(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True, zero_division=0)

        result = {
            "Model": self.best_model_name,
            "Accuracy": self.best_accuracy,
            "Precision": self.best_precision,
            "Recall": self.best_recall,
            "F1": self.best_f1,
            "ROC_AUC": self.best_auc,
            "ConfusionMatrix": cm.tolist(),
            "ClassificationReport": report
        }
        self.results.append(result)

        logger.info(f"Ensemble Model Trained. ROC-AUC: {self.best_auc:.4f}")
        return result

    def save_best_model(self):
        logger.info("=" * 60)
        logger.info("SAVING ENSEMBLE MODEL")
        logger.info("=" * 60)

        try:
            if self.best_model is None:
                raise Exception("No model has been trained yet.")

            # Save ensemble object to disk
            joblib.dump(self.best_model, settings.BEST_MODEL)
            logger.info(f"Saved best model -> {settings.BEST_MODEL}")

            # Register model with local registry
            models = self.registry.list_models()
            version = VersionManager.next_version(models)
            
            self.registry.register_model(
                version=version,
                model_name=self.best_model_name,
                accuracy=self.best_accuracy,
                precision=self.best_precision,
                recall=self.best_recall,
                f1=self.best_f1,
                roc_auc=self.best_auc,
                model_path=settings.BEST_MODEL
            )

            # Auto-deploy model
            if self.registry.compare(self.best_auc):
                self.registry.deploy(version)
                logger.info(f"Model version {version} deployed to production.")
            else:
                logger.info("Current production model retained.")

        except Exception as e:
            logger.exception(f"Failed to save and register model: {e}")
            raise

    def export_results(self):
        try:
            df = pd.DataFrame(self.results)
            path = "reports/training_results.csv"
            df.to_csv(path, index=False)
            logger.info(f"Exported training results to {path}")
        except Exception as e:
            logger.warning(f"Failed to export results: {e}")

    def save_training_log(self):
        try:
            log = {
                "timestamp": str(self.training_time),
                "model_name": self.best_model_name,
                "accuracy": self.best_accuracy,
                "precision": self.best_precision,
                "recall": self.best_recall,
                "f1": self.best_f1,
                "roc_auc": self.best_auc
            }
            with open("reports/training_log.json", "w") as f:
                json.dump(log, f, indent=4)
            logger.info("Saved training log to reports/training_log.json")
        except Exception as e:
            logger.warning(f"Failed to save training log: {e}")

    def save_feature_importance(self, feature_names):
        # Stacking ensemble does not have direct feature_importances_, but we can get it from XGBoost base model
        try:
            xgb_model = self.best_model.base_models.get("XGBoost")
            if xgb_model is not None and hasattr(xgb_model, "feature_importances_"):
                importance = pd.DataFrame({
                    "Feature": feature_names,
                    "Importance": xgb_model.feature_importances_
                }).sort_values("Importance", ascending=False)
                
                importance.to_csv("reports/feature_importance.csv", index=False)
                logger.info("Saved feature importances (from XGBoost) to reports/feature_importance.csv")
        except Exception as e:
            logger.warning(f"Failed to save feature importance: {e}")

    def print_summary(self):
        logger.info("=" * 70)
        logger.info("ENTERPRISE TRAINING SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Model Name      : {self.best_model_name}")
        logger.info(f"Accuracy        : {self.best_accuracy:.4f}")
        logger.info(f"Precision       : {self.best_precision:.4f}")
        logger.info(f"Recall          : {self.best_recall:.4f}")
        logger.info(f"F1 Score        : {self.best_f1:.4f}")
        logger.info(f"ROC-AUC         : {self.best_auc:.4f}")
        logger.info("=" * 70)

    def run_training_pipeline(self, X_train, y_train, X_test, y_test, feature_names=None):
        logger.info("Starting Stacking Ensemble Training Pipeline...")
        try:
            self.train_ensemble(X_train, y_train, X_test, y_test)
            self.save_best_model()
            self.export_results()
            if feature_names is not None:
                self.save_feature_importance(feature_names)
            self.save_training_log()
            self.print_summary()
            logger.info("Training Pipeline Completed Successfully.")
        except Exception as e:
            logger.exception(f"Training Pipeline failed: {e}")
            raise
