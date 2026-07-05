import streamlit as st
import pandas as pd
import requests

from app.logging.logger import EnterpriseLogger

if "token" not in st.session_state or not st.session_state.logged_in:
    st.error("Please Login First.")
    st.stop()
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
    page_title="Batch Prediction",
    layout="wide"
)

st.title("📄 Batch Fraud Prediction")

st.divider()

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.write(f"Rows : {len(df)}")
    st.write(f"Columns : {len(df.columns)}")

    st.divider()

    if st.button("🚀 Predict All Transactions", use_container_width=True):

        predictions = []

        progress = st.progress(0)

        for index, row in df.iterrows():

            payload = row.to_dict(orient="records")

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                headers={
                    "Authorization": f"Bearer{st.session_state.token}"
                }
            )

            if response.status_code == 200:

                predictions = response["results"]
                response = response.json()

            progress.progress(
                (index + 1) / len(df)
            )

        st.success("Prediction Completed")

        # ---------------------------------------
        # Convert Predictions to DataFrame
        # ---------------------------------------

        results = []

        for item in predictions:

            pred = item["prediction"]
            risk = item["risk_analysis"]

            results.append({

                "Transaction_ID": item["transaction_id"],

                "Prediction": pred["Prediction"],

                "Fraud_Probability": pred["Fraud_Probability"],

                "Risk_Score": pred["Risk_Score"],

                "Risk_Tier": pred["Risk_Tier"],

                "Priority": risk["Priority"],

                "Recommended_Action": risk["Recommended Action"]

            })

        results_df = pd.DataFrame(results)

        # ---------------------------------------
        # Summary
        # ---------------------------------------

        frauds = len(
            results_df[
                results_df["Prediction"] == "Fraud"
            ]
        )

        genuine = len(results_df) - frauds

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Transactions",
                len(results_df)
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

        st.divider()

        # ---------------------------------------
        # Highlight High Risk Rows
        # ---------------------------------------

        def highlight(row):

            if row["Risk_Tier"] == "Critical":

                return ["background-color:red"] * len(row)

            elif row["Risk_Tier"] == "High":

                return ["background-color:orange"] * len(row)

            else:

                return [""] * len(row)

        st.subheader("Prediction Results")

        st.dataframe(

            results_df.style.apply(
                highlight,
                axis=1
            ),

            use_container_width=True

        )

        # ---------------------------------------
        # Download CSV
        # ---------------------------------------

        csv = results_df.to_csv(index=False)

        st.download_button(

            "📥 Download Predictions",
            csv,
            file_name="predictions.csv",
            mime="text/csv"
        )
EnterpriseLogger.info(

    f"Batch Prediction "

    f"{len(results_df)} transactions"

)