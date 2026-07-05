import json
import os

import streamlit as st
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Application Settings")

st.divider()
SETTINGS_FILE = "config/settings.json"

DEFAULT_SETTINGS = {

    "theme": "Light",

    "risk_threshold": 80,

    "groq_model": "llama-3.3-70b-versatile",

    "api_url": "http://127.0.0.1:8000",

    "mongodb": "mongodb://localhost:27017",

    "export_directory": "reports"

}

if not os.path.exists("config"):

    os.makedirs("config")

if os.path.exists(SETTINGS_FILE):

    with open(
        SETTINGS_FILE,
        "r"
    ) as f:

        settings = json.load(f)

else:

    settings = DEFAULT_SETTINGS.copy()

    st.subheader("General Settings")

theme = st.selectbox(

    "Theme",

    [

        "Light",

        "Dark"

    ],

    index=[
        "Light",
        "Dark"
    ].index(settings["theme"])

)

risk = st.slider(

    "Risk Threshold",

    0,

    100,

    settings["risk_threshold"]

)

st.subheader("AI Settings")

groq = st.selectbox(

    "Groq Model",

    [

        "llama-3.3-70b-versatile",

        "llama-3.1-8b-instant",

        "gemma2-9b-it"

    ],

    index=0

)

st.subheader("Backend")

api = st.text_input(

    "FastAPI URL",

    settings["api_url"]

)

mongo = st.text_input(

    "MongoDB URL",

    settings["mongodb"]

)

st.subheader("Export")

directory = st.text_input(

    "Export Directory",

    settings["export_directory"]

)
col1, col2 = st.columns(2)

with col1:

    if st.button(

        "💾 Save Settings",

        use_container_width=True

    ):

        settings = {

            "theme": theme,

            "risk_threshold": risk,

            "groq_model": groq,

            "api_url": api,

            "mongodb": mongo,

            "export_directory": directory

        }

        with open(

            SETTINGS_FILE,

            "w"

        ) as f:

            json.dump(

                settings,

                f,

                indent=4

            )

        st.success(

            "Settings Saved Successfully."

        )

with col2:

    if st.button(

        "🔄 Reset",

        use_container_width=True

    ):

        with open(

            SETTINGS_FILE,

            "w"

        ) as f:

            json.dump(

                DEFAULT_SETTINGS,

                f,

                indent=4

            )

        st.success(

            "Settings Reset."

        )

        st.rerun()

st.divider()

st.subheader("Current Configuration")

st.json(settings)