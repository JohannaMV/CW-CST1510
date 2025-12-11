import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.datasets import get_all_datasets, insert_dataset, update_dataset, delete_dataset
from google import genai

st.set_page_config(page_title="Dataset!", page_icon="🫧", layout="wide")

conn = connect_database()

st.title("🫧Datasets Dashboard!🫧")
tab1, tab2 = st.tabs(["Datasets", "AI Chat"])

# ------------------- TAB 1: Dataset Management -------------------
with tab1:
    datasets = get_all_datasets(conn)
    st.dataframe(datasets, use_container_width=True)

    st.header("Add Dataset")
    with st.form("new_dataset_form"):
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

    st.header("Update Dataset")
    with st.form("update_dataset_form"):
        u_dataset_id = st.number_input("Dataset ID to Update", step=1)
        u_rows = st.number_input("New Row Count", step=1)
        u_columns = st.number_input("New Column Count", step=1)
        update_submitted = st.form_submit_button("Update Dataset")

    if update_submitted:
        rows_affected = update_dataset(conn, u_dataset_id, u_rows, u_columns)
        if rows_affected > 0:
            st.success(f"Successfully updated Dataset ID {u_dataset_id}.")
            st.rerun()
        else:
            st.error(f"Dataset ID {u_dataset_id} not found. No updates were made.")

    st.subheader("Delete Dataset")
    with st.form("delete_dataset_form"):
        del_dataset_id = st.number_input("Dataset ID to Delete", step=1)
        delete_submitted = st.form_submit_button("Delete Dataset")

    if delete_submitted and del_dataset_id:
        rows = delete_dataset(conn, del_dataset_id)
        if rows:
            st.success(f"Dataset {del_dataset_id} deleted successfully!")
        else:
            st.error("No dataset found with that Dataset ID.")
        st.rerun()

# ------------------- TAB 2: AI Chat -------------------
with tab2:
    st.header("Data Science AI Chat")

    # API key input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        placeholder="AIza...",
        key="dataset_ai_api_key"
    )
    if not api_key:
        st.info("Enter your API key to use the AI chat.")
        st.stop()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash"

    # Initialize session state for chat
    if "dataset_ai_messages" not in st.session_state:
        st.session_state.dataset_ai_messages = [
            {
                "role": "system",
                "content": """You are a Data Science and Dataset expert assistant.
- Analyze datasets and metadata
- Provide guidance on dataset structure, rows, columns
- Suggest improvements, normalization, or cleaning
- Explain dataset use cases for ML, analysis, visualization
- Prioritize actionable recommendations
Tone: Professional, clear, and technical."""
            }
        ]

    # Clear Chat Button
    if st.button("!!Clear Chat!!"):
        st.session_state.dataset_ai_messages = [
            st.session_state.dataset_ai_messages[0]  # keep system message
        ]
        st.rerun()

    # Display previous messages
    for msg in st.session_state.dataset_ai_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Ask AI about datasets...", key="dataset_ai_prompt")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.dataset_ai_messages.append({"role": "user", "content": prompt})

        # Prepare messages for Gemini
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.dataset_ai_messages
        ]

        # Get AI response
        response = client.models.generate_content(
            model=model_name,
            contents=messages
        )
        reply = response.text

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.dataset_ai_messages.append({"role": "assistant", "content": reply})

# LOGOUT BUTTON
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("home.py")
