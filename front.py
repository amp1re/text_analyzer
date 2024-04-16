import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8080"

# Для хранения токена в сессии
if "auth_token" not in st.session_state:
    st.session_state["auth_token"] = None


def authenticate(email, password):
    response = requests.post(
        f"{BASE_URL}/signin", json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Failed to authenticate.")
        return None


def register(username, email, password):
    response = requests.put(
        f"{BASE_URL}/signup",
        json={"username": username, "email": email, "password": password},
    )
    if response.status_code == 200:
        st.success("User registered successfully.")
    else:
        st.error("Registration failed.")


def update_balance(amount):
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
    response = requests.put(
        f"{BASE_URL}/update_balance", json={"amount": amount}, headers=headers
    )
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Failed to update balance: {response.text}")


def execute_task(text):
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
    response = requests.get(f"{BASE_URL}/execute", json={"text": text}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to execute task.")
        return None


st.title("Text analyzer")

with st.form("auth_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_login = st.form_submit_button("Login")
    submit_register = st.form_submit_button("Register")

    if submit_login:
        token = authenticate(email, password)
        if token:
            st.session_state["auth_token"] = token
            st.success("Logged in successfully!")

    if submit_register:
        register(username, email, password)

if st.session_state["auth_token"]:
    amount = st.number_input("Enter amount to update balance:", min_value=0, value=0)
    if st.button("Update Balance"):
        update_balance(amount)

    text = st.text_area("Enter text to classify:")
    if st.button("Classify Text"):
        result = execute_task(text)
        if result:
            st.write(result)
