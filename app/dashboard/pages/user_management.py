import streamlit as st
import pandas as pd
import requests

if "logged_in" not in st.session_state:

    st.error("Please Login")

    st.stop()

if st.session_state.role != "Admin":

    st.error("Only Admin can access User Management")

    st.stop()

st.set_page_config(

    page_title="User Management",

    layout="wide"

)

st.title("👥 User Management")

st.divider()

response = requests.get(

    "http://127.0.0.1:8000/users"

)

users = response.json()

df = pd.DataFrame(users)

col1, col2 = st.columns(2)

with col1:

    st.metric(

        "Total Users",

        len(df)

    )

with col2:

    st.metric(

        "Roles",

        df["role"].nunique()

    )

st.divider()

search = st.text_input(

    "🔍 Search Username"

)

if search:

    df = df[

        df["username"]

        .str.contains(

            search,

            case=False

        )

    ]
st.subheader("Users")

st.dataframe(

    df,

    use_container_width=True

)

st.subheader("Users")

st.dataframe(

    df,

    use_container_width=True

)

st.divider()

st.subheader("➕ Add User")

username = st.text_input(

    "Username"

)

password = st.text_input(

    "Password",

    type="password"

)

role = st.selectbox(

    "Role",

    [

        "Admin",

        "Fraud Analyst",

        "Manager",

        "Auditor"

    ]

)

if st.button(

    "Create User",

    use_container_width=True

):

    response = requests.post(

        "http://127.0.0.1:8000/users",

        json={

            "username": username,

            "password": password,

            "role": role

        }

    )

    if response.status_code == 200:

        st.success("User Created")

        st.rerun()

    else:

        st.error(response.text)

st.divider()

st.subheader("✏ Change Role")

selected = st.selectbox(

    "Select User",

    df["username"]

)

new_role = st.selectbox(

    "New Role",

    [

        "Admin",

        "Fraud Analyst",

        "Manager",

        "Auditor"

    ],

    key="role"

)

if st.button(

    "Update Role",

    use_container_width=True

):

    response = requests.put(

        f"http://127.0.0.1:8000/users/{selected}/role",

        params={

            "role": new_role

        }

    )

    if response.status_code == 200:

        st.success("Role Updated")

        st.rerun()

st.divider()

st.subheader("🔑 Reset Password")

selected = st.selectbox(

    "User",

    df["username"],

    key="password"

)

new_password = st.text_input(

    "New Password",

    type="password"

)

if st.button(

    "Reset Password",

    use_container_width=True

):

    response = requests.put(

        f"http://127.0.0.1:8000/users/{selected}/password",

        params={

            "password": new_password

        }

    )

    if response.status_code == 200:

        st.success("Password Updated")
st.divider()

st.subheader("🗑 Delete User")

selected = st.selectbox(

    "Delete",

    df["username"],

    key="delete"

)

if st.button(

    "Delete User",

    use_container_width=True

):

    response = requests.delete(

        f"http://127.0.0.1:8000/users/{selected}"

    )

    if response.status_code == 200:

        st.success("User Deleted")

        st.rerun()

st.divider()

if st.button(

    "🔄 Refresh",

    use_container_width=True

):

    st.rerun()