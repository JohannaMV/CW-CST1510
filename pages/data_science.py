import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from services.database_manager import DatabaseManager
from models.dataset import Dataset
from services.ai_assistant import AIAssistant

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Datasets!", page_icon="🫧", layout="wide")

# --------------------------------------------------
# Session guards (login)
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# --------------------------------------------------
# Database manager
# --------------------------------------------------
db = DatabaseManager("database/platform.db")

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🫧 Datasets Dashboard 🫧")
tab1, tab2 = st.tabs(["Datasets", "AI Chat"])

# ==================================================
# TAB 1 — DATASET MANAGEMENT (PDF STEP 6)
# ==================================================
with tab1:
    st.subheader("All Datasets")

    rows = db.fetch_all(
        """SELECT dataset_id, name, rows, columns, uploaded_by, uploaded_at
           FROM datasets_metadata"""
    )

    datasets: list[Dataset] = []
    for row in rows:
        dataset = Dataset(
            dataset_id=row[0],
            name=row[1],
            rows=row[2],
            columns=row[3],
            uploaded_by=row[4],
            upload_date=row[5],
        )
        datasets.append(dataset)

    for dataset in datasets:
        st.write(dataset)
        st.divider()

    # -------------------------------
    # Add Dataset
    # -------------------------------
    st.subheader("Add Dataset")
    with st.form("add_dataset_form"):
        dataset_id = st.number_input("Dataset ID", step=1)
        name = st.text_input("Dataset Name")
        rows_count = st.number_input("Row Count", step=1)
        columns_count = st.number_input("Column Count", step=1)
        uploaded_by = st.text_input("Uploaded By")
        upload_date = st.date_input("Upload Date")
        add_btn = st.form_submit_button("Add Dataset")

    if add_btn and name:
        db.execute_query(
            """INSERT INTO datasets_metadata
               (dataset_id, name, rows, columns, uploaded_by, uploaded_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (dataset_id, name, rows_count, columns_count, uploaded_by, upload_date),
        )
        st.success("Dataset added successfully!")
        st.rerun()

    # -------------------------------
    # Update Dataset
    # -------------------------------
    st.subheader("Update Dataset")
    with st.form("update_dataset_form"):
        upd_id = st.number_input("Dataset ID to Update", step=1)
        new_rows = st.number_input("New Row Count", step=1)
        new_columns = st.number_input("New Column Count", step=1)
        update_btn = st.form_submit_button("Update Dataset")

    if update_btn:
        cur = db.execute_query(
            """UPDATE datasets_metadata
               SET rows = ?, columns = ?
               WHERE dataset_id = ?""",
            (new_rows, new_columns, upd_id),
        )
        if cur.rowcount > 0:
            st.success("Dataset updated successfully!")
        else:
            st.error("Dataset not found.")
        st.rerun()

    # -------------------------------
    # Delete Dataset
    # -------------------------------
    st.subheader("Delete Dataset")
    with st.form("delete_dataset_form"):
        del_id = st.number_input("Dataset ID to Delete", step=1)
        del_btn = st.form_submit_button("Delete Dataset")

    if del_btn:
        cur = db.execute_query(
            "DELETE FROM datasets_metadata WHERE dataset_id = ?",
            (del_id,),
        )
        if cur.rowcount > 0:
            st.success("Dataset deleted.")
        else:
            st.error("Dataset not found.")
        st.rerun()

# ==================================================
# TAB 2 — AI ASSISTANT (PDF STEP 3.3)
# ==================================================
with tab2:
    st.header("Data Science AI Assistant")

    api_key = st.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.info("Please enter your Gemini API key.")
        st.stop()

    ai = AIAssistant(
        api_key=api_key,
        system_prompt="""You are a data science expert assistant.
Analyze dataset metadata.
Suggest preprocessing, feature engineering, and visualizations.
Use standard data science terminology.
Provide clear, structured advice."""
    )

    if "data_ai_history" not in st.session_state:
        st.session_state.data_ai_history = []

    if st.button("Clear Chat"):
        st.session_state.data_ai_history.clear()
        ai.clear_history()
        st.rerun()

    for msg in st.session_state.data_ai_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask about data science...")
    if user_prompt:
        st.session_state.data_ai_history.append(
            {"role": "user", "content": user_prompt}
        )

        reply = ai.send_message(user_prompt)

        st.session_state.data_ai_history.append(
            {"role": "assistant", "content": reply}
        )
        st.rerun()

# --------------------------------------------------
# Logout
# --------------------------------------------------
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
