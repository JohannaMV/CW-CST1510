import streamlit as st
import bcrypt
import os

USER_DATA_FILE = "DATA/users.txt"

def load_users():
    users = {}   # username → {password, role}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    username, hashed_pw, role = parts
                    users[username] = {"password": hashed_pw, "role": role}
    return users


def save_user(username, hashed_pw, role="user"):
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username}:{hashed_pw}:{role}\n")


st.set_page_config(page_title="Home!", page_icon="🫧 ",layout="centered")

# ---------- Initialise session state ----------
if "users" not in st.session_state:
    st.session_state.users = load_users()   # load from user.txt

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
st.title("🫧Welcome!🫧")

if st.session_state.logged_in:
     st.success(f"Already logged in as **{st.session_state.username}**.")
     if st.button("Go to dashboard"):
         # Use the official navigation API to switch pages
         st.switch_page("pages/1_Dashboard.py")
     st.stop() # Don’t show login/register again

# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if login_username in users:
            stored_hash = users[login_username]["password"]
            if bcrypt.checkpw(login_password.encode(), stored_hash.encode()):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.session_state.role = users[login_username]["role"]
                st.success(f"Welcome back, {login_username}!")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found.")

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    role= st.selectbox("Choose a role", ["user", "admin"])

    if st.button("Register", type="primary"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists.")
        else:
            hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # save in session
            st.session_state.users[new_username] = {
                "password": hashed,
                "role": "user"
            }

            # save to file
            save_user(new_username, hashed, "user")

            st.success("Account created! You can now log in.")

