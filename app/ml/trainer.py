import os
import json
from pyexpat import model
import joblib
import warnings
import numpy as np
import pandas as pd
ENABLE_CROSS_VALIDATION = True
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    VotingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from sklearn.model_selection import (
    cross_val_score,
    StratifiedKFold
)

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from app.ml.hyperparameter import HyperParameterOptimizer

warnings.filterwarnings("ignore")


class EnterpriseFraudTrainer:

    """
    Enterprise Fraud Detection Trainer

    Trains multiple ML models

    Compares their performance

    Selects the best model

    Saves models and reports

    """

    def __init__(self):

        self.models = {}

        self.results = []

        self.best_model = None

        self.best_model_name = None

        self.best_auc = 0

        self.best_f1 = 0

        self.cv = StratifiedKFold(

            n_splits=4,

            shuffle=True,

            random_state=42

        )

        os.makedirs("models", exist_ok=True)

        os.makedirs("reports", exist_ok=True)

        os.makedirs("logs", exist_ok=True)

        self.training_time = datetime.now()


    def initialize_models(self):

        print("=" * 70)

        print("Initializing Enterprise ML Models")

        print("=" * 70)

        self.models = {

            "Logistic Regression":

                LogisticRegression(

                    max_iter=1000,

                    random_state=42

                ),

            "Random Forest":

                RandomForestClassifier(

                    n_estimators=300,

                    max_depth=15,

                    random_state=42,

                    n_jobs=-1

                ),

            "Extra Trees":

                ExtraTreesClassifier(
                    n_estimators=300,
                    random_state=42,
                    n_jobs=-1

                ),

            "Gradient Boosting":

                GradientBoostingClassifier(

                    random_state=42

                ),

            "AdaBoost":

                AdaBoostClassifier(

                    random_state=42

                ),

            "XGBoost":

                XGBClassifier(

                    random_state=42,

                    eval_metric="logloss",

                    tree_method="hist"

                ),

            "LightGBM":

                LGBMClassifier(

                    random_state=42,

                    verbose=-1

                ),

            "CatBoost":

                CatBoostClassifier(

                    verbose=False,

                    random_state=42

                )

        }

        print(f"\nLoaded {len(self.models)} Models\n")

    def print_separator(self):
        """Print separator line"""
        print("\n")
        print("=" * 70)
        print("\n")

    def train_single_model(self, model_name, model, X_train, y_train):
        """Train a single model"""
        print(f"Training {model_name}...")
        model.fit(X_train, y_train)
        return model

    def evaluate_model(self, model_name, model, X_test, y_test):
        """Evaluate model performance"""
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, zero_division=0)
        recall = recall_score(y_test, predictions, zero_division=0)
        f1 = f1_score(y_test, predictions, zero_division=0)
        auc = roc_auc_score(y_test, probabilities)
        cm = confusion_matrix(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)

        metrics = {
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1": f1,
            "ROC_AUC": auc
        }

        self.results.append(metrics)

        print("\nEvaluation Metrics")
        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print(f"ROC AUC  : {auc:.4f}")

        report_path = f"reports/{model_name.replace(' ', '_')}_classification_report.csv"
        pd.DataFrame(report).transpose().to_csv(report_path)
        print(f"Saved Report -> {report_path}")

        return auc, f1, cm

    def cross_validate(self, model_name, model, X_train, y_train):
        """Perform cross validation"""
        print("\nRunning Cross Validation...")

        scores = cross_val_score(
            model,
            X_train,
            y_train,
            cv=self.cv,
            scoring="roc_auc",
            n_jobs=-1
        )

        mean_score = scores.mean()
        print(f"Cross Validation ROC AUC : {mean_score:.4f}")

        return mean_score

    def save_model(self, model_name, model):
        """Save model to disk"""
        filename = model_name.replace(" ", "_")
        path = f"models/{filename}.joblib"

        joblib.dump(model, path)
        print(f"Saved Model -> {path}")

    def update_best_model(self, model_name, model, auc, f1):
        """Update best model if current is better"""
        if auc > self.best_auc:
            self.best_auc = auc
            self.best_f1 = f1
            self.best_model = model
            self.best_model_name = model_name

    def save_best_model(self):
        """Save the best model found during training"""
        if self.best_model is None:
            return

        joblib.dump(self.best_model, "models/best_model.joblib")

        metadata = {
            "Model": self.best_model_name,
            "ROC_AUC": self.best_auc,
            "F1": self.best_f1,
            "Saved_On": str(datetime.now())
        }

        with open("models/model_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        print("\nBest Model Saved Successfully")
        print(metadata)

    def generate_summary(self):
        """Generate and print model performance summary"""
        print("\n")
        print("=" * 80)
        print("MODEL PERFORMANCE SUMMARY")
        print("=" * 80)

        df = pd.DataFrame(self.results)
        df = df.sort_values(by="ROC_AUC", ascending=False)

        print(df)
        print("\n")
        print("Best Model")
        print(f"Model : {self.best_model_name}")
        print(f"ROC AUC : {self.best_auc:.4f}")
        print(f"F1 Score : {self.best_f1:.4f}")

        return df

    def export_results(self):
        """Export model comparison results to CSV"""
        df = pd.DataFrame(self.results)
        df = df.sort_values(by="ROC_AUC", ascending=False)

        df.to_csv("reports/model_comparison.csv", index=False)

        print("\nModel Comparison Saved")
        print("reports/model_comparison.csv")

    def save_feature_importance(self, feature_names):
        """Save feature importance from best model"""
        if self.best_model is None:
            return

        if not hasattr(self.best_model, "feature_importances_"):
            print("Best model has no feature importance.")
            return

        importance = pd.DataFrame({
            "Feature": feature_names,
            "Importance": self.best_model.feature_importances_
        })

        importance = importance.sort_values(by="Importance", ascending=False)
        importance.to_csv("reports/feature_importance.csv", index=False)
        print("\nFeature Importance Saved.")

    def save_training_log(self):
        """Save training log with metadata"""
        log = {
            "Training_Date": str(self.training_time),
            "Best_Model": self.best_model_name,
            "Best_ROC_AUC": float(self.best_auc),
            "Best_F1": float(self.best_f1)
        }
        with open("logs/training_log.json", "w") as f:
            json.dump(log, f, indent=4)
        print("\nTraining Log Saved")

    def train_all_models(self, X_train, y_train, X_test, y_test):
        """Train all models"""
        # trained_model = self.train_model(
        #     model_name,
        #     model,
        #     X_train,
        #     y_train
        # )

        # metrics = self.evaluate_model(
        #     model_name,
        #     trained_model,
        #     X_test,
        #     y_test
        # )

        self.models = {
            "Random Forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            n_jobs=-1
      ),

      "XGBoost": XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            tree_method="hist",
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1
      )
      }
        self.print_separator()
        print("Training Enterprise Fraud Detection Models...")
        self.print_separator()

        for model_name, model in self.models.items():
            print(f"\n{'=' * 70}")
            print(f"MODEL : {model_name}")
            print(f"{'=' * 70}")

            trained_model = self.train_single_model(
                model_name,
                model,
                X_train,
                y_train
            )

            auc, f1, cm = self.evaluate_model(
                model_name,
                trained_model,
                X_test,
                y_test
            )

            # cv_score = self.cross_validate(
            #     model_name,
            #     trained_model,
            #     X_train,
            #     y_train
            # )

            # self.results[-1]["CrossValidation"] = cv_score

            self.save_model(model_name, trained_model)

            self.update_best_model(
                model_name,
                trained_model,
                auc,
                f1
            )

        self.save_best_model()
        self.generate_summary()
        self.export_results()

    def run_training_pipeline(self, X_train, y_train, X_test, y_test, feature_names=None):
        """Run the complete training pipeline"""
        self.train_all_models(X_train, y_train, X_test, y_test)
        
        if feature_names is not None:
            self.save_feature_importance(feature_names)
        
        self.save_training_log()
        
        print("\n")
        print("=" * 80)
        print("ENTERPRISE TRAINING COMPLETED")
        print("=" * 80)