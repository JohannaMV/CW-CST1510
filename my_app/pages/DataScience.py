import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.datasets import get_all_datasets, insert_dataset

st.set_page_config(page_title="Dataset!", page_icon="🫧", layout="wide")

conn= connect_database()

st.title(".𖥔 ݁ ˖𓂃.☘︎ ݁˖ Datasets Dashboard .𖥔 ݁ ˖𓂃.☘︎ ݁˖")

datasets=get_all_datasets(conn)
st.dataframe(datasets, use_container_width=True)

with st.form("new dataset"):
    dataset_id = st.number_input("Dataset ID", step=1)
    name = st.text_input("Dataset Name")
    rows = st.number_input("Row Count", step=1)
    columns = st.number_input("Column Count", step=1)
    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.date_input("Upload Date")
    submitted = st.form_submit_button("Add Dataset")

if submitted and name:
    insert_dataset(conn, dataset_id, name, rows, columns, uploaded_by, upload_date)
    st.success("Dataset metadata added to database")
    st.rerun()

# Logout button
st.divider()
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("home.py")