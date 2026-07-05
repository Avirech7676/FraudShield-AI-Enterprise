import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from app.database.connection import MongoDBConnection

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
    page_title="Enterprise Analytics",
    layout="wide"
)

st.title("📊 Fraud Analytics Dashboard")

st.divider()

# -------------------------------------------------------
# Connect MongoDB
# -------------------------------------------------------

db = MongoDBConnection().connect()

predictions = list(
    db.predictions.find({}, {"_id": 0})
)

if len(predictions) == 0:

    st.warning("No prediction data found.")

    st.stop()

df = pd.DataFrame(predictions)

# -------------------------------------------------------
# Filters
# -------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    risk_filter = st.selectbox(

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

with col2:

    prediction_filter = st.selectbox(

        "Prediction",

        [

            "All",

            "Fraud",

            "Genuine"

        ]

    )

filtered_df = df.copy()

if risk_filter != "All":

    filtered_df = filtered_df[

        filtered_df["risk_tier"] == risk_filter

    ]

if prediction_filter != "All":

    filtered_df = filtered_df[

        filtered_df["prediction"] == prediction_filter

    ]


# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

total = len(filtered_df)

frauds = len(
    filtered_df[filtered_df["prediction"] == "Fraud"]
)

genuine = total - frauds

average_risk = round(
    filtered_df["risk_score"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total
    )

with col2:
    st.metric(
        "Frauds",
        frauds
    )

with col3:
    st.metric(
        "Genuine",
        genuine
    )

with col4:
    st.metric(
        "Average Risk",
        average_risk
    )

st.divider()

# -------------------------------------------------------
# Pie Chart
# -------------------------------------------------------

pie = px.pie(

    filtered_df,

    names="prediction",
    hole=0.45,
    title="Fraud vs Genuine"
)

st.plotly_chart(
    pie,
    use_container_width=True
)

# -------------------------------------------------------
# Risk Tier Distribution
# -------------------------------------------------------

risk = px.bar(

    df["risk_tier"].value_counts().reset_index(),

    x="risk_tier",

    y="count",

    title="Risk Tier Distribution"

)

st.plotly_chart(
    risk,
    use_container_width=True
)

# -------------------------------------------------------
# Histogram
# -------------------------------------------------------

hist = px.histogram(

    filtered_df,

    x="risk_tier",
    color="risk_tier",
    title="Risk Score Distribution"
)

st.plotly_chart(
    risk,
    use_container_width=True
)

# -------------------------------------------------------
# Fraud Probability Scatter
# -------------------------------------------------------

scatter = px.scatter(

    filtered_df,

    x="fraud_probability",

    y="risk_score",

    color="prediction",

    hover_data=[

        "transaction_id"

    ],

    title="Fraud Probability vs Risk Score"

)

st.plotly_chart(

    scatter,

    use_container_width=True

)

# -------------------------------------------------------
# Timeline
# -------------------------------------------------------

if "created_at" in filtered_df.columns:

    filtered_df["created_at"] = pd.to_datetime(

        filtered_df["created_at"]

    )

    timeline = (

        filtered_df.groupby(

            filtered_df["created_at"].dt.date

        )

        .size()

        .reset_index(name="Transactions")

    )

    line = px.line(

        timeline,

        x="created_at",

        y="Transactions",

        markers=True,

        title="Transactions Over Time"

    )

    st.plotly_chart(

        line,

        use_container_width=True

    )



# -------------------------------------------------------
# Top Risk Transactions
# -------------------------------------------------------

st.subheader("Top 10 High Risk Transactions")

top = filtered_df.sort_values(

    by="risk_score",

    ascending=False

).head(10)

st.dataframe(
    top,
    use_container_width=True
)

# -------------------------------------------------------
# Download Analytics
# -------------------------------------------------------

csv = filtered_df.to_csv(

    index=False

)

st.download_button(

    "📥 Download Analytics",

    csv,

    "analytics.csv",

    "text/csv"
)

# -------------------------------------------------------
# Refresh Dashboard
# -------------------------------------------------------

if st.button(

    "🔄 Refresh Dashboard",

    use_container_width=True

):

    st.rerun()


