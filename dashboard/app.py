import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import joblib

# Set Page Config
st.set_page_config(
    page_title="FraudShield AI Enterprise Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #0f1116;
    }
    .metric-card {
        background-color: #1a1f2c;
        border: 1px solid #2e3748;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        font-size: 14px;
        color: #a0aec0;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        color: #ffffff;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Imports from backend
try:
    from app.database.connection import MongoDBConnection
    from app.database.repository import FraudRepository
    from app.continuous_learning.retraining_engine import RetrainingEngine
    from app.ai.groq_report import EnterpriseFraudReporter
    
    db = MongoDBConnection().connect()
    repository = FraudRepository(db)
    retrain_engine = RetrainingEngine()
    llm_reporter = EnterpriseFraudReporter()
    db_available = True
except Exception as e:
    db_available = False
    st.error(f"Failed to connect to backend/MongoDB: {e}")

# Title Block
st.markdown("<h1 style='text-align: center; color: #4F46E5;'>🛡️ FraudShield AI Enterprise</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 16px;'>Real-time Stacking Ensemble Model Monitoring & Case Investigation Hub</p>", unsafe_allow_html=True)
st.markdown("---")

if db_available:
    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/144/shield.png", width=100)
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Select Tab",
        ["Overview Monitoring", "Case Investigator", "Continuous Retraining"]
    )

    # ----------------------------------------------------
    # Load Data from MongoDB
    # ----------------------------------------------------
    predictions = list(repository.predictions.find().sort("created_at", -1))
    transactions = list(repository.transactions.find().sort("created_at", -1))
    cases = list(repository.cases.find().sort("created_at", -1))
    feedback = list(repository.db["analyst_feedback"].find())

    df_pred = pd.DataFrame(predictions) if predictions else pd.DataFrame()
    df_tx = pd.DataFrame(transactions) if transactions else pd.DataFrame()
    df_cases = pd.DataFrame(cases) if cases else pd.DataFrame()
    df_fb = pd.DataFrame(feedback) if feedback else pd.DataFrame()

    if menu == "Overview Monitoring":
        st.subheader("📊 System KPIs & Overview")
        
        # Calculate KPIs
        total_tx = len(df_tx)
        total_fraud = len(df_pred[df_pred["prediction"] == "Fraud"]) if not df_pred.empty else 0
        avg_risk = df_pred["risk_score"].mean() if not df_pred.empty else 0.0
        
        # Estimate Fraud Savings: Sum of blocked transaction amounts (where risk_score >= 80)
        blocked_tx_ids = []
        if not df_pred.empty:
            blocked_tx_ids = df_pred[df_pred["risk_score"] >= 80]["transaction_id"].tolist()
        
        fraud_savings = 0.0
        if blocked_tx_ids and not df_tx.empty:
            blocked_amounts = []
            for tx in transactions:
                if tx.get("transaction_id") in blocked_tx_ids:
                    blocked_amounts.append(float(tx.get("request", {}).get("Amount", 0)))
            fraud_savings = sum(blocked_amounts)

        # KPIs Grid
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Scored</div><div class='metric-value'>{total_tx}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Fraud Flagged</div><div class='metric-value'>{total_fraud}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Avg Risk Score</div><div class='metric-value'>{avg_risk:.1f}%</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Blocked Savings</div><div class='metric-value'>${fraud_savings:,.2f}</div></div>", unsafe_allow_html=True)
        with col5:
            avg_latency = df_pred["Latency_ms"].mean() if not df_pred.empty and "Latency_ms" in df_pred.columns else 4.2
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Mean Latency</div><div class='metric-value'>{avg_latency:.2f} ms</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts Section
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Risk Tier Distribution")
            if not df_pred.empty and "risk_tier" in df_pred.columns:
                tier_counts = df_pred["risk_tier"].value_counts().reset_index()
                tier_counts.columns = ["Risk Tier", "Count"]
                fig1 = px.bar(
                    tier_counts, 
                    x="Risk Tier", 
                    y="Count", 
                    color="Risk Tier", 
                    color_discrete_sequence=px.colors.sequential.Electric,
                    template="plotly_dark"
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No prediction data available yet.")

        with c2:
            st.markdown("### Fraud Trends (Daily Flag Count)")
            if not df_pred.empty:
                df_pred["date"] = pd.to_datetime(df_pred["created_at"]).dt.date
                daily_counts = df_pred[df_pred["prediction"] == "Fraud"].groupby("date").size().reset_index(name="Flags")
                fig2 = px.line(
                    daily_counts, 
                    x="date", 
                    y="Flags", 
                    markers=True,
                    template="plotly_dark",
                    color_discrete_sequence=["#EF4444"]
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No flags recorded yet.")

        st.markdown("<br>", unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("### Geographic Fraud Heatmap")
            if not df_pred.empty and "country" in df_pred.columns:
                country_data = df_pred[df_pred["prediction"] == "Fraud"].groupby("country").size().reset_index(name="Cases")
                fig3 = px.choropleth(
                    country_data,
                    locations="country",
                    locationmode="ISO-3",
                    color="Cases",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Sunsetdark,
                    template="plotly_dark"
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No location data available yet.")

        with c4:
            st.markdown("### Model Drift Detection (Prediction Score Distribution)")
            if not df_pred.empty:
                fig4 = px.histogram(
                    df_pred, 
                    x="fraud_probability", 
                    nbins=30,
                    template="plotly_dark",
                    color_discrete_sequence=["#10B981"],
                    opacity=0.75
                )
                fig4.add_vline(x=0.80, line_dash="dash", line_color="red", annotation_text="Critical Alert Threshold")
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No probability distributions yet.")

    elif menu == "Case Investigator":
        st.subheader("🔍 Case Investigation Console")

        if not df_cases.empty:
            col_list, col_det = st.columns([1, 2])

            with col_list:
                st.markdown("### Labeled Case Queue")
                
                # Format queue columns
                df_cases_view = df_cases[["case_id", "priority", "status", "created_at"]].copy()
                st.write("Select a Case ID below to investigate details:")
                
                selected_case_id = st.selectbox("Select Case ID", df_cases_view["case_id"].tolist())
                selected_case = df_cases[df_cases["case_id"] == selected_case_id].iloc[0]

            with col_det:
                st.markdown(f"### Case ID: {selected_case_id}")
                tx_id = selected_case.get("transaction_id")
                st.write(f"**Associated Transaction ID**: `{tx_id}`")
                st.write(f"**Priority**: `{selected_case.get('priority')}` | **Status**: `{selected_case.get('status')}`")

                # Fetch original transaction features
                tx_detail = repository.transactions.find_one({"transaction_id": tx_id})
                pred_detail = repository.predictions.find_one({"transaction_id": tx_id})

                if tx_detail and pred_detail:
                    st.markdown("#### Transaction Parameters")
                    st.json(tx_detail.get("request", {}))

                    st.markdown("#### Risk Metrics")
                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        st.metric("ML Fraud Probability", f"{pred_detail.get('fraud_probability') * 100:.2f}%")
                    with r_col2:
                        st.metric("Enterprise Risk Score", f"{pred_detail.get('enterprise_risk_score') or pred_detail.get('risk_score')}/100")

                    # LLM Explanation Section
                    st.markdown("#### AI Investigation Report Summary")
                    llm_expl = pred_detail.get("llm_explanation")
                    if not llm_expl:
                        llm_expl = "Model and risk engine flagged the transaction. Regenerate reports to read details."
                    st.info(llm_expl)

                    # Dynamic Q&A Panel
                    st.markdown("#### Ask Llama-3.3 (Investigator Q&A)")
                    question = st.text_input("Ask a question about this transaction (e.g. 'Why was this flagged?', 'Is the IP address safe?')")
                    if question:
                        with st.spinner("Llama-3.3 is analyzing transaction variables..."):
                            answer = llm_reporter.answer_investigator_question(
                                tx_detail.get("request", {}),
                                pred_detail,
                                {"Risk Score": pred_detail.get("enterprise_risk_score") or pred_detail.get("risk_score"), "Risk Tier": pred_detail.get("risk_tier")},
                                question
                            )
                            st.write("**AI Answer:**")
                            st.write(answer)

                    # SHAP Plots Display
                    st.markdown("#### SHAP Local Explanations")
                    s_c1, s_c2 = st.columns(2)
                    with s_c1:
                        if os.path.exists("reports/shap/waterfall.png"):
                            st.image("reports/shap/waterfall.png", caption="SHAP Waterfall Plot", use_container_width=True)
                        else:
                            st.write("Waterfall plot image not generated yet.")
                    with s_c2:
                        if os.path.exists("reports/shap/shap_force.png"):
                            st.image("reports/shap/shap_force.png", caption="SHAP Force Plot", use_container_width=True)
                        else:
                            st.write("Force plot image not generated yet.")

                    # Analyst Feedback submission
                    st.markdown("#### Submit Analyst Decision")
                    feedback_label = st.radio("Label transaction as:", ["Genuine", "Fraud"])
                    notes = st.text_area("Investigation Notes")
                    
                    if st.button("Submit Decision & Update Case"):
                        repository.save_feedback({
                            "transaction_id": tx_id,
                            "actual_label": feedback_label,
                            "notes": notes,
                            "submitted_at": datetime.utcnow()
                        })
                        repository.update_case(selected_case_id, {
                            "status": "CLOSED",
                            "resolution": feedback_label,
                            "updated_at": datetime.utcnow()
                        })
                        st.success(f"Feedback submitted! Transaction `{tx_id}` confirmed as **{feedback_label}**.")
                        st.rerun()

                else:
                    st.warning("Original transaction details missing in MongoDB.")

        else:
            st.info("No active fraud cases found in MongoDB queue.")

    elif menu == "Continuous Retraining":
        st.subheader("🔁 Continuous Learning & Retraining")

        # Feedback Counter Card
        pending_feedback = len(df_fb)
        st.markdown(f"""
        <div class='metric-card' style='max-width: 400px; margin: auto;'>
            <div class='metric-label'>Submitted Feedback Records</div>
            <div class='metric-value'>{pending_feedback}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.info("When analysts submit feedback regarding transaction classifications, the retraining engine uses the labeled items to run continuous model training, automatically updating the production model if the retrained accuracy exceeds current performance.")

        col_trigger, col_metrics = st.columns([1, 2])

        with col_trigger:
            st.markdown("### Retraining Console")
            if pending_feedback == 0:
                st.warning("You must submit at least 1 analyst feedback record in the Case Investigator tab before retraining can run.")
            
            # Button to trigger retraining
            if st.button("Trigger Stacking Ensemble Retraining", disabled=(pending_feedback == 0)):
                with st.spinner("Retraining preprocessor & Stacking Ensemble (XGBoost, CatBoost, RandomForest)..."):
                    success = retrain_engine.retrain()
                    if success:
                        st.success("Model retrained and deployed successfully!")
                        st.rerun()
                    else:
                        st.error("Retraining failed or threshold check was bypassed.")

        with col_metrics:
            st.markdown("### Model Registry Status")
            model_recs = list(repository.models.find().sort("created_at", -1))
            if model_recs:
                df_recs = pd.DataFrame(model_recs)
                st.dataframe(df_recs[["version", "model_name", "roc_auc", "accuracy", "status", "created_at"]])
            else:
                st.write("No models registered yet.")
else:
    st.warning("Database unavailable. Please check MongoDB configuration.")
