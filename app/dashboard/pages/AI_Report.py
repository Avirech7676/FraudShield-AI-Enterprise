import os
import streamlit as st
import pandas as pd

from app.ai.groq_report import EnterpriseFraudReporter
from app.database.connection import MongoDBConnection
from app.logging.logger import EnterpriseLogger

if "token" not in st.session_state or not st.session_state.logged_in:
    st.error("Please Login First.")
    st.stop()

allowed = [

    "Admin",
    "Fraud Analyst",
    "Manager"
]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()
# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="AI Fraud Report",
    layout="wide"
)

st.title("🤖 AI Fraud Investigation Report")

st.divider()

# ======================================================
# MongoDB Connection
# ======================================================

db = MongoDBConnection().connect()

predictions = list(
    db.predictions.find({}, {"_id": 0})
)

if len(predictions) == 0:

    st.warning("No Predictions Available.")

    st.stop()

# ======================================================
# Convert to DataFrame
# ======================================================

df = pd.DataFrame(predictions)

# ======================================================
# Select Transaction
# ======================================================

transaction = st.selectbox(

    "Select Transaction",

    df["transaction_id"]

)

selected = df[
    df["transaction_id"] == transaction
].iloc[0]

# ======================================================
# Build Prediction Dictionary
# ======================================================

prediction = {

    "Prediction": selected["prediction"],

    "Fraud_Probability": selected["fraud_probability"],

    "Risk_Score": selected["risk_score"],

    "Risk_Tier": selected["risk_tier"]

}

# ======================================================
# Build Risk Dictionary
# ======================================================

risk = {

    "Priority":

        "P1"
        if prediction["Risk_Score"] >= 80
        else "P4",

    "Recommended Action":

        "Block Transaction"
        if prediction["Risk_Score"] >= 80
        else "Approve Transaction"

}

# ======================================================
# Display Prediction Summary
# ======================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Prediction",

        prediction["Prediction"]

    )

with col2:

    st.metric(

        "Fraud Probability",

        f"{prediction['Fraud_Probability']*100:.2f}%"

    )

with col3:

    st.metric(

        "Risk Score",

        prediction["Risk_Score"]

    )

with col4:

    st.metric(

        "Priority",

        risk["Priority"]

    )

st.divider()

# ======================================================
# AI Report Generation
# ======================================================

reporter = EnterpriseFraudReporter()

if st.button(

    "🤖 Generate AI Report",

    use_container_width=True

):

    with st.spinner("Generating AI Report..."):

        report = reporter.generate_report(

            prediction,

            risk

        )

    st.success("AI Report Generated Successfully")

    st.markdown(report)
    EnterpriseLogger.info(

      f"AI Report Generated "

      f"{transaction}"

)

    # ------------------------------------------
    # Save Report
    # ------------------------------------------

    os.makedirs(

        "reports/ai_reports",

        exist_ok=True

    )

    filename = f"reports/ai_reports/{transaction}.txt"

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(report)

    st.success(f"Report Saved: {filename}")

    # ------------------------------------------
    # Download Report
    # ------------------------------------------

    st.download_button(
        "📥 Download Report",
        report,
        file_name=f"{transaction}.txt",
        mime="text/plain"
    )
    EnterpriseLogger.info(
      f"Report Downloaded "
      f"{transaction}"
)