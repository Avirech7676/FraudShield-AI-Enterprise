import streamlit as st

with open(

    "logs/app.log",

    "r"

) as file:

    logs = file.read()
st.text_area(

    "Application Logs",

    logs,

    height=600

)
st.download_button(

    "Download Logs",

    logs,

    "app.log"

)