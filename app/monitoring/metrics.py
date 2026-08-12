import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
def evaluate_model(
    model,
    X_test,
    y_test

):
    prediction = model.predict(X_test)
    probability = model.predict_proba(X_test)[:,1]

    return {
        "Accuracy": accuracy_score(
            y_test,
            prediction
        ),
        "Precision": precision_score(
            y_test,
            prediction
        ),
        "Recall": recall_score(
            y_test,
            prediction
        ),
        "F1 Score": f1_score(
            y_test,
            prediction
        ),
        "ROC AUC": roc_auc_score(
            y_test,
            probability
        ),
        "Confusion Matrix": confusion_matrix(
            y_test,
            prediction
        )
    }
