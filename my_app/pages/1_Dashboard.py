import sys
import os

# Add the project root directory to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database

st.set_page_config(page_title="Dashboard", page_icon="🫧", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("home.py")
    st.stop()

# Logged in — show dashboard
conn = connect_database()

st.title("˚ 𝜗𝜚˚⋆｡☆ Dashboard! ˚ 𝜗𝜚˚⋆｡☆")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

st.subheader("Go to section:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("༄.° Cyber Incidents ༄.°"):
        st.switch_page("pages/CyberSecurity.py")

with col2:
    if st.button("༄.° Datasets Dashboard ༄.°"):
        st.switch_page("pages/DataScience.py")

with col3:
    if st.button("༄.° IT Tickets ༄.°"):
        st.switch_page("pages/IT_Operations.py")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("home.py")
