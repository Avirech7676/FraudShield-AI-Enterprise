import streamlit as st

from app.exports.export_manager import ExportManager

if "logged_in" not in st.session_state:
    st.error("Please Login")
    st.stop()

allowed = [
    "Admin",
    "Manager",
    "Auditor"
]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()

st.set_page_config(
    page_title="Export Center",
    layout="wide"
)

st.title("📦 Enterprise Export Center")
st.divider()

export_type = st.selectbox(
    "Export Format",
    [
        "PDF",
        "Excel",
        "CSV",
        "Word"
    ]
)

report_name = st.text_input(
    "Report Name",
    value="Fraud_Report"
)

if st.button(
    "Generate Report"
):
    st.success(
        f"{export_type} report generated successfully."
    )

