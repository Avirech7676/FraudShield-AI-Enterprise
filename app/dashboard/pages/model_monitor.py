import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from app.monitoring.metrics import evaluate_model

if "logged_in" not in st.session_state:
    st.error("Please Login")
    st.stop()

allowed = [
    "Admin",
    "Manager"
]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()

st.set_page_config(
    page_title="Model Monitoring",
    layout="wide"
)
st.title("📈 Model Monitoring Dashboard")
st.divider()

model = joblib.load(
    "models/fraud_model.pkl"
)

X_test = joblib.load(
    "artifacts/X_test.pkl"
)

y_test = joblib.load(
    "artifacts/y_test.pkl"
)

results = evaluate_model(
    model,
    X_test,
    y_test
)

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(
        "Accuracy",
        f"{results['Accuracy']:.3f}"

    )

with col2:
    st.metric(
        "Precision",
        f"{results['Precision']:.3f}"

    )

with col3:
    st.metric(
        "Recall",
        f"{results['Recall']:.3f}"
    )

with col4:
    st.metric(
        "F1",
        f"{results['F1 Score']:.3f}"

    )

with col5:
    st.metric(
        "ROC",
        f"{results['ROC AUC']:.3f}"
    )
cm = results["Confusion Matrix"]

cm_df = pd.DataFrame(
    cm,
    columns=["Pred Genuine","Pred Fraud"],
    index=["Actual Genuine","Actual Fraud"]
)
st.subheader("Confusion Matrix")
st.dataframe(
    cm_df,
    use_container_width=True
)

importance = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False

)

fig = px.bar(
    importance.head(20),
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top Features"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Model Information")

info = {
    "Algorithm":"Random Forest",
    "Version":"1.0.0",
    "Training Date":"2026-07-05",
    "Dataset Size":len(X_test)

}
st.json(info)

import subprocess
if st.button(
    "🔄 Retrain Model"
):
    subprocess.run(
        [
            "python",
            "-m",
            "app.training.train"
        ]
    )
    st.success(
        "Model Retrained Successfully"
    )

if st.button(
    "Refresh"
):
    st.rerun()

