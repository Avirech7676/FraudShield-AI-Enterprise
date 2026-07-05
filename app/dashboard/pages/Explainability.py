import os
import subprocess
from app.logging.logger import EnterpriseLogger

import streamlit as st
from PIL import Image


if "logged_in" not in st.session_state:
    st.error("Please Login")
    st.stop()

allowed = [
    "Admin",
    "Fraud Analyst",
    "Manager"
]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()

st.set_page_config(
    page_title="Explainable AI",
    layout="wide"
)

st.title("🧠 Explainable AI Dashboard")

st.divider()

REPORT_DIR = "reports/shap"

summary = os.path.join(
    REPORT_DIR,
    "summary_plot.png"
)

importance = os.path.join(
    REPORT_DIR,
    "feature_importance.png"
)

waterfall = os.path.join(
    REPORT_DIR,
    "waterfall_plot.png"
)

decision = os.path.join(
    REPORT_DIR,
    "decision_plot.png"
)

force = os.path.join(
    REPORT_DIR,
    "force_plot.html"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Images Generated",
        4
    )

with col2:

    st.metric(
        "Interactive Reports",
        1
    )

st.divider()

if st.button("🔄 Generate SHAP Visualizations"):

    with st.spinner("Generating SHAP..."):

        subprocess.run(
            [
                "python",
                "-m",
                "app.xai.test_shap"
            ]
        )

    st.success("SHAP Visualizations Generated")

st.divider()
st.subheader("📊 SHAP Summary Plot")
EnterpriseLogger.info(
    "SHAP Report Generated"
)
if os.path.exists(summary):

    st.image(
        Image.open(summary),
        use_container_width=True
    )

else:

    st.warning("Summary Plot Not Found")

st.divider()
st.subheader("⭐ Feature Importance")

if os.path.exists(importance):

    st.image(
        Image.open(importance),
        use_container_width=True
    )

else:

    st.warning("Feature Importance Plot Not Found")

st.divider()
st.subheader("🌊 Waterfall Plot")

if os.path.exists(waterfall):

    st.image(
        Image.open(waterfall),
        use_container_width=True
    )

else:

    st.warning("Waterfall Plot Not Found")

st.divider()
st.subheader("📈 Decision Plot")

if os.path.exists(decision):

    st.image(
        Image.open(decision),
        use_container_width=True
    )

else:

    st.warning("Decision Plot Not Found")

st.divider()
st.subheader("⚡ Interactive Force Plot")

if os.path.exists(force):

    with open(force, "r", encoding="utf-8") as f:

        html = f.read()

    st.components.v1.html(
        html,
        height=600,
        scrolling=True
    )
else:
    st.warning("Force Plot Not Found")

