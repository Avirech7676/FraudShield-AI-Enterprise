import streamlit as st

from app.auth.login import login

# =====================================================
# Page Configuration (Must be First)
# =====================================================

st.set_page_config(

    page_title="FraudShield AI Enterprise",

    page_icon="🛡",

    layout="wide"

)

# =====================================================
# Session State Initialization
# =====================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

if "role" not in st.session_state:

    st.session_state.role = ""

if "token" not in st.session_state:

    st.session_state.token = ""

# =====================================================
# Login Check
# =====================================================


if "logged_in" not in st.session_state:

    st.error("Please Login")

    st.stop()

if st.session_state.role != "Admin":

    st.error("Access Denied")

    st.stop()
# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.success("Logged In")

    st.write(

        f"👤 User : {st.session_state.username}"

    )

    st.write(

        f"🎯 Role : {st.session_state.role}"

    )

    st.divider()

    if st.button(

        "🚪 Logout",

        use_container_width=True

    ):

        st.session_state.clear()

        st.rerun()

# =====================================================
# Main Dashboard
# =====================================================

st.title("🛡 FraudShield AI Enterprise")

st.divider()

st.success("Enterprise Fraud Detection Platform")

st.write("Use the navigation menu on the left.")