import streamlit as st
import pandas as pd

from app.database.connection import MongoDBConnection
from app.logging.logger import EnterpriseLogger

if "token" not in st.session_state or not st.session_state.logged_in:
    st.error("Please Login First.")
    st.stop()

allowed = [
    "Admin",
    "Auditor"
]

if st.session_state.role not in allowed:

    st.error("Access Denied")

    st.stop()
# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Database Explorer",
    layout="wide"
)
EnterpriseLogger.info(

    "Database Explorer Opened"

)
st.title("🗄 Database Explorer")

st.divider()

# ======================================================
# MongoDB Connection
# ======================================================

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

audit = list(
    db.audit_logs.find({}, {"_id": 0})
)

# ======================================================
# Dashboard Statistics
# ======================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Transactions",
        len(transactions)
    )

with col2:
    st.metric(
        "Predictions",
        len(predictions)
    )

with col3:
    st.metric(
        "Alerts",
        len(alerts)
    )

with col4:
    st.metric(
        "Audit Logs",
        len(audit)
    )

st.divider()

# ======================================================
# Tabs
# ======================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Transactions",
        "Predictions",
        "Alerts",
        "Audit Logs"
    ]
)

# ======================================================
# Transactions
# ======================================================

with tab1:

    st.subheader("Transactions")

    if transactions:

        transaction_df = pd.DataFrame(transactions)

        st.dataframe(
            transaction_df,
            use_container_width=True
        )

    else:

        st.info("No Transactions Found.")

# ======================================================
# Predictions
# ======================================================

with tab2:

    st.subheader("Predictions")

    if predictions:

        df = pd.DataFrame(predictions)

        # -------------------------------
        # Search
        # -------------------------------

        search = st.text_input(
            "🔍 Search Transaction ID"
        )

        if search:

            df = df[
                df["transaction_id"]
                .astype(str)
                .str.contains(search)
            ]

        # -------------------------------
        # Risk Filter
        # -------------------------------

        tier = st.selectbox(

            "Risk Tier",

            [
                "All",
                "Very Low",
                "Low",
                "Medium",
                "High",
                "Critical"
            ]

        )

        if tier != "All":

            df = df[
                df["risk_tier"] == tier
            ]

        # -------------------------------
        # Highlight Rows
        # -------------------------------

        def highlight(row):

            if row["risk_tier"] == "Critical":

                return ["background-color:red"] * len(row)

            elif row["risk_tier"] == "High":

                return ["background-color:orange"] * len(row)

            elif row["risk_tier"] == "Medium":

                return ["background-color:yellow"] * len(row)

            else:

                return [""] * len(row)

        st.dataframe(

            df.style.apply(
                highlight,
                axis=1
            ),

            use_container_width=True

        )

        # -------------------------------
        # Download CSV
        # -------------------------------

        csv = df.to_csv(index=False)

        st.download_button(

            "📥 Download Predictions",

            csv,

            file_name="predictions.csv",

            mime="text/csv"

        )

    else:

        st.info("No Predictions Found.")

# ======================================================
# Alerts
# ======================================================

with tab3:

    st.subheader("Alerts")

    if alerts:

        alert_df = pd.DataFrame(alerts)

        st.dataframe(

            alert_df,

            use_container_width=True

        )

    else:

        st.warning("No Alerts Generated.")

# ======================================================
# Audit Logs
# ======================================================

with tab4:

    st.subheader("Audit Logs")

    if audit:

        audit_df = pd.DataFrame(audit)

        st.dataframe(

            audit_df,

            use_container_width=True

        )

    else:

        st.info("No Audit Logs Found.")