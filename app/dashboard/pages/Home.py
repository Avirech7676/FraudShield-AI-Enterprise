import streamlit as st
import pandas as pd
import plotly.express as px

from app.database.connection import MongoDBConnection

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="FraudShield AI Enterprise",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 FraudShield AI Enterprise")
st.caption("Real-Time Fraud Detection & Investigation Platform")

st.divider()

# =====================================================
# Database Connection
# =====================================================

db = MongoDBConnection().connect()

transactions = list(
    db.transactions.find({}, {"_id": 0})
)

predictions = list(
    db.predictions.find({}, {"_id": 0})
)

alerts = list(
    db.alerts.find({}, {"_id": 0})
)

audit_logs = list(
    db.audit_logs.find({}, {"_id": 0})
)

# =====================================================
# Convert to DataFrames
# =====================================================

transaction_df = pd.DataFrame(transactions)
prediction_df = pd.DataFrame(predictions)
alert_df = pd.DataFrame(alerts)
audit_df = pd.DataFrame(audit_logs)

# =====================================================
# KPI Cards
# =====================================================

fraud_count = 0
genuine_count = 0
average_risk = 0

if not prediction_df.empty:

    fraud_count = len(
        prediction_df[
            prediction_df["prediction"] == "Fraud"
        ]
    )

    genuine_count = len(
        prediction_df[
            prediction_df["prediction"] == "Genuine"
        ]
    )

    average_risk = round(
        prediction_df["risk_score"].mean(),
        2
    )

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Transactions",
        len(transaction_df)
    )

with col2:
    st.metric(
        "Predictions",
        len(prediction_df)
    )

with col3:
    st.metric(
        "Fraud Cases",
        fraud_count
    )

with col4:
    st.metric(
        "Alerts",
        len(alert_df)
    )

with col5:
    st.metric(
        "Average Risk",
        average_risk
    )

st.divider()

# =====================================================
# Charts
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("Fraud vs Genuine")

    if not prediction_df.empty:

        fig = px.pie(

            prediction_df,

            names="prediction",

            title="Prediction Distribution"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No prediction data available.")

with right:

    st.subheader("Risk Tier Distribution")

    if not prediction_df.empty:

        risk_chart = px.bar(

            prediction_df["risk_tier"].value_counts().reset_index(),

            x="risk_tier",

            y="count",

            labels={
                "risk_tier":"Risk Tier",
                "count":"Transactions"
            },

            title="Risk Tier Distribution"

        )

        st.plotly_chart(
            risk_chart,
            use_container_width=True
        )

    else:

        st.info("No risk data available.")

st.divider()

# =====================================================
# Recent Predictions
# =====================================================

st.subheader("📄 Recent Predictions")

if not prediction_df.empty:

    st.dataframe(

        prediction_df.sort_index(
            ascending=False
        ).head(10),

        use_container_width=True

    )

else:

    st.info("No predictions available.")

st.divider()

# =====================================================
# Recent Alerts
# =====================================================

st.subheader("🚨 Latest Alerts")

if not alert_df.empty:

    st.dataframe(

        alert_df.sort_index(
            ascending=False
        ).head(10),

        use_container_width=True

    )

else:

    st.success("No active alerts.")

st.divider()

# =====================================================
# Audit Logs
# =====================================================

st.subheader("📜 Recent Audit Logs")

if not audit_df.empty:

    st.dataframe(

        audit_df.sort_index(
            ascending=False
        ).head(10),

        use_container_width=True

    )

else:

    st.info("No audit logs found.")

st.divider()

# =====================================================
# System Status
# =====================================================

st.subheader("🖥 System Status")

status1, status2, status3, status4 = st.columns(4)

with status1:
    st.success("✅ FastAPI Online")

with status2:
    st.success("✅ MongoDB Connected")

with status3:
    st.success("✅ ML Model Loaded")

with status4:
    st.success("✅ Groq AI Ready")

st.divider()

# =====================================================
# Footer
# =====================================================

st.markdown(
    """
---
### FraudShield AI Enterprise

Version **1.0**

Developed by **Avinash Reddy**

© 2026
"""
)