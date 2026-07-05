import streamlit as st
import pandas as pd
import requests

from app.database.connection import MongoDBConnection


if "logged_in" not in st.session_state:

    st.error("Please Login")

    st.stop()

allowed = [

    "Admin",

    "Fraud Analyst",

    "Auditor"

]

if st.session_state.role not in allowed:

    st.error("Access Denied")

    st.stop()

st.set_page_config(

    page_title="Alert Center",

    layout="wide"

)
st.title("🚨 Fraud Alert Center")
st.divider()

db = MongoDBConnection().connect()

alerts = list(

    db.alerts.find({}, {"_id": 0})

)

if len(alerts) == 0:

    st.info("No Alerts Found")

    st.stop()

df = pd.DataFrame(alerts)

total = len(df)

open_alerts = len(

    df[df["status"] == "OPEN"]

)

closed = len(

    df[df["status"] == "CLOSED"]

)

critical = len(

    df[df["priority"] == "P1"]

)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Alerts",

        total

    )

with col2:

    st.metric(

        "Open",

        open_alerts

    )

with col3:

    st.metric(

        "Closed",

        closed

    )

with col4:

    st.metric(

        "Critical",

        critical

    )

status = st.selectbox(

    "Status",

    [

        "All",

        "OPEN",

        "IN_PROGRESS",

        "CLOSED"

    ]

)

priority = st.selectbox(

    "Priority",

    [

        "All",

        "P1",

        "P2",

        "P3",

        "P4"

    ]

)

search = st.text_input(

    "Search Transaction ID"

)

filtered = df.copy()

if status != "All":

    filtered = filtered[

        filtered["status"] == status

    ]

if priority != "All":

    filtered = filtered[

        filtered["priority"] == priority

    ]

if search:

    filtered = filtered[

        filtered["transaction_id"]

        .str.contains(

            search,

            case=False

        )

    ]

st.subheader("Alert Queue")

st.dataframe(
    filtered,
    use_container_width=True
)

st.subheader("Assign Alert")

transaction = st.selectbox(

    "Transaction",

    filtered["transaction_id"]

)

analyst = st.text_input(

    "Assign To"

)

if st.button(

    "Assign Alert"

):

    db.alerts.update_one(

        {

            "transaction_id": transaction

        },

        {

            "$set": {

                "assigned_to": analyst,

                "status": "IN_PROGRESS"

            }

        }

    )

    st.success("Assigned Successfully")
    st.rerun()

st.subheader("Close Alert")

transaction = st.selectbox(

    "Alert",

    filtered["transaction_id"],

    key="close"

)

if st.button(

    "Close Alert"

):

    db.alerts.update_one(

        {

            "transaction_id": transaction

        },

        {

            "$set": {

                "status": "CLOSED"

            }

        }

    )
    st.success("Alert Closed")
    st.rerun()
csv = filtered.to_csv(
    index=False
)

st.download_button(
    "📥 Download Alerts",
    csv,
    "alerts.csv",
    "text/csv"
)

if st.button(

    "🔄 Refresh"

):

    st.rerun()