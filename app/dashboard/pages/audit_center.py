import streamlit as st
import pandas as pd
import plotly.express as px

from app.database.connection import MongoDBConnection

if "logged_in" not in st.session_state:

    st.error("Please Login")

    st.stop()

allowed = [

    "Admin",

    "Auditor"

]

if st.session_state.role not in allowed:

    st.error("Access Denied")

    st.stop()

st.set_page_config(

    page_title="Audit Center",

    layout="wide"

)

st.title("📋 Enterprise Audit Center")
st.divider()

db = MongoDBConnection().connect()

audit_logs = list(

    db.audit_logs.find({}, {"_id": 0})

)

if len(audit_logs) == 0:

    st.warning("No Audit Logs Found")
    st.stop()

df = pd.DataFrame(audit_logs)

total_logs = len(df)

users = df["user"].nunique() if "user" in df.columns else 0

actions = df["action"].nunique()

today = 0

if "created_at" in df.columns:

    df["created_at"] = pd.to_datetime(df["created_at"])

    today = len(

        df[

            df["created_at"].dt.date

            == pd.Timestamp.today().date()

        ]

    )

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Logs",

        total_logs

    )

with col2:

    st.metric(

        "Users",

        users

    )

with col3:

    st.metric(

        "Actions",

        actions

    )

with col4:

    st.metric(

        "Today's Logs",

        today

    )

search = st.text_input(

    "🔍 Search User / Transaction"

)

filtered = df.copy()

if search:

    if "transaction_id" in filtered.columns:

        filtered = filtered[

            filtered.astype(str)

            .apply(

                lambda col:

                col.str.contains(

                    search,

                    case=False
                )
            )
            .any(axis=1)
        ]

actions = [
    "All"
] + sorted(df["action"].dropna().unique())

selected = st.selectbox(
    "Action",
    actions
)

if selected != "All":
    filtered = filtered[
        filtered["action"] == selected
    ]

if "created_at" in filtered.columns:
    timeline = (
        filtered.groupby(
            filtered["created_at"].dt.date
        )
        .size()
        .reset_index(name="Logs")
    )

    fig = px.line(
        timeline,
        x="created_at",
        y="Logs",
        markers=True,
        title="Audit Timeline"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Audit Logs")

st.dataframe(

    filtered,

    use_container_width=True

)

csv = filtered.to_csv(

    index=False

)

st.download_button(
    "📥 Download Audit Logs",
    csv,
    "audit_logs.csv",
    "text/csv"
)

if st.button(
    "🔄 Refresh"
):
    st.rerun()

    