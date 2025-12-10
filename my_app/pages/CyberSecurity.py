import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident

st.set_page_config(page_title="Cyber!", page_icon="🫧", layout="wide")

conn= connect_database()

st.title(".𖥔 ݁ ˖𓂃.☘︎ ݁˖ Cyber Incidents Dashboard .𖥔 ݁ ˖𓂃.☘︎ ݁˖")

incidents=get_all_incidents(conn)
st.dataframe(incidents, use_container_width=True)

with st.form("new incident"):
    cat= st.text_input("Category")
    severity= st.selectbox("severity",["low","medium","high","critical"])
    status= st.selectbox("status",["open","in progress", "resolved"])
    desc= st.text_input("Description")
    id= st.number_input("Incident ID")
    time= st.date_input("Time")
    submitted= st.form_submit_button("Add new incident")

if submitted and cat:
    insert_incident(conn,id, time,severity,cat,status,desc)
    st.success("Incident added to database")
    st.rerun()

# Logout button
st.divider()
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("home.py")