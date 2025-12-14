import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

# --------------------------------------------------
# Database & Auth
# --------------------------------------------------
db = DatabaseManager("database/platform.db")
auth = AuthManager(db)

# --------------------------------------------------
# Page UI
# --------------------------------------------------
st.set_page_config(page_title="Login", page_icon="🔐")
st.title("🔐 Login")

# --------------------------------------------------
# Initialize session state
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# --------------------------------------------------
# Login form
# --------------------------------------------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = auth.login_user(username, password)

    if user is None:
        st.error("Invalid username or password")
    else:
        st.session_state.logged_in = True
        st.session_state.username = user.get_username()
        st.session_state.role = user.get_role()

        st.success(f"Welcome, {user.get_username()}!")
        st.switch_page("Home.py")
