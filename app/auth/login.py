import streamlit as st
import requests

from app.logging.logger import EnterpriseLogger


def login():

    st.title("🛡 FraudShield AI Enterprise")

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        response = requests.post(

            "http://127.0.0.1:8000/login",

            json={

                "username": username,

                "password": password

            }

        )

        if response.status_code == 200:

            result = response.json()

            st.session_state.logged_in = True

            st.session_state.username = username

            st.session_state.role = result["role"]

            st.session_state.token = result["access_token"]

            EnterpriseLogger.info(

                f"{username} logged in."

            )

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Username or Password")