import json
import requests
import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first.")
    st.stop()

allowed = ["Admin", "Fraud Analyst"]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()
    
st.set_page_config(
    page_title="Prediction",
    layout="wide"
)

st.title("🔍 Single Transaction Prediction")

st.divider()

# --------------------------------------------------
# Transaction Details
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    time = st.number_input("Time", value=10000.0)
    amount = st.number_input("Amount", value=150.0)

with col2:
    st.info(
        """
        Enter the PCA Features (V1 - V28)

        These values come from the Credit Card Fraud dataset.
        """
    )

# --------------------------------------------------
# PCA Features
# --------------------------------------------------

values = {}

cols = st.columns(4)

for i in range(1, 29):

    with cols[(i - 1) % 4]:

        values[f"V{i}"] = st.number_input(

            f"V{i}",

            value=0.0,

            format="%.4f"

        )

st.divider()

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("🚀 Predict Transaction", use_container_width=True):

    payload = {

        "Time": time,

        "Amount": amount

    }

    payload.update(values)

    try:

        response = requests.post(

            "http://127.0.0.1:8000/predict",

            json=payload,
            headers = {
                "Authorization":
                f"Bearer {st.session_state.token}"
            }
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]

            risk = result["risk_analysis"]

            transaction_id = result["transaction_id"]

            st.success("Prediction Successful")

            st.divider()

            col1, col2, col3 = st.columns(3)

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

            st.divider()

            st.subheader("Risk Analysis")

            st.write(f"**Risk Tier:** {risk['Risk Tier']}")

            st.write(f"**Priority:** {risk['Priority']}")

            st.write(
                f"**Recommended Action:** {risk['Recommended Action']}"
            )

            st.divider()

            tier = prediction["Risk_Tier"]

            if tier == "Very Low":

                st.success("🟢 Very Low Risk")

            elif tier == "Low":

                st.info("🔵 Low Risk")

            elif tier == "Medium":

                st.warning("🟠 Medium Risk")

            elif tier == "High":

                st.error("🔴 High Risk")

            else:

                st.error("🚨 Critical Risk")

            st.divider()

            st.subheader("Transaction ID")

            st.code(transaction_id)

            st.download_button(

                label="📥 Download Prediction Report",

                data=json.dumps(result, indent=4),

                file_name="prediction_report.json",

                mime="application/json"

            )

        else:

            st.error(response.text)

    except Exception as e:

        st.error(f"Cannot connect to FastAPI Server.\n\n{e}")