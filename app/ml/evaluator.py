import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve
)


class ModelEvaluator:

    def __init__(self):

        os.makedirs("reports", exist_ok=True)

    ########################################################

    def evaluate(
        self,
        model,
        X_test,
        y_test,
        model_name="Model"
    ):

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        auc = roc_auc_score(
            y_test,
            probabilities
        )

        cm = confusion_matrix(
            y_test,
            predictions
        )

        report = classification_report(
            y_test,
            predictions,
            output_dict=True
        )

        metrics = {

            "Model": model_name,

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1": f1,

            "ROC_AUC": auc

        }

        self.plot_confusion_matrix(
            cm,
            model_name
        )

        self.plot_roc(
            y_test,
            probabilities,
            model_name
        )

        self.plot_precision_recall(
            y_test,
            probabilities,
            model_name
        )

        pd.DataFrame(report).transpose().to_csv(

            f"reports/{model_name}_classification_report.csv"

        )

        return metrics

    ########################################################

    def plot_confusion_matrix(
        self,
        cm,
        model_name
    ):

        plt.figure(figsize=(5,5))

        plt.imshow(cm)

        plt.title(f"{model_name} Confusion Matrix")

        plt.colorbar()

        plt.xticks([0,1],["Normal","Fraud"])

        plt.yticks([0,1],["Normal","Fraud"])

        for i in range(2):
            for j in range(2):

                plt.text(
                    j,
                    i,
                    cm[i,j],
                    ha="center",
                    va="center"
                )

        plt.tight_layout()

        plt.savefig(

            f"reports/{model_name}_confusion_matrix.png"

        )

        plt.close()

    ########################################################

    def plot_roc(
        self,
        y_test,
        probabilities,
        model_name
    ):

        fpr,tpr,_ = roc_curve(
            y_test,
            probabilities
        )

        plt.figure(figsize=(6,6))

        plt.plot(fpr,tpr,label="ROC")

        plt.plot([0,1],[0,1],"--")

        plt.xlabel("False Positive Rate")

        plt.ylabel("True Positive Rate")

        plt.title(f"{model_name} ROC Curve")

        plt.legend()

        plt.savefig(

            f"reports/{model_name}_roc_curve.png"

        )

        plt.close()

    ########################################################

    def plot_precision_recall(
        self,
        y_test,
        probabilities,
        model_name
    ):

        precision, recall, _ = precision_recall_curve(
            y_test,
            probabilities
        )

        plt.figure(figsize=(6,6))

        plt.plot(
            recall,
            precision
        )

        plt.xlabel("Recall")

        plt.ylabel("Precision")

        plt.title(f"{model_name} Precision Recall Curve")

        plt.savefig(

            f"reports/{model_name}_precision_recall.png"

        )

        plt.close()