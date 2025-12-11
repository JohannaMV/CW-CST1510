import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident, update_incident_status, delete_incident
from google import genai

st.set_page_config(page_title="Cyber!", page_icon="🫧", layout="wide")

conn = connect_database()

st.title("🫧Cyber Incidents Dashboard!🫧")
tab1, tab2 = st.tabs(["Incidents", "AI Chat"])

# TAB 1 — INCIDENT MANAGEMENT
with tab1:
    incidents = get_all_incidents(conn)
    st.dataframe(incidents, use_container_width=True)

    st.subheader("Add New Incident")
    with st.form("new_incident_form"):
        cat = st.text_input("Category")
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        status = st.selectbox("Status", ["open", "in progress", "resolved"])
        desc = st.text_input("Description")
        id = st.number_input("Incident ID", step=1)
        time = st.date_input("Time")
        submitted = st.form_submit_button("Add new incident")

    if submitted and cat:
        insert_incident(conn, id, time, severity, cat, status, desc)
        st.success("Incident added to database")
        st.rerun()

    st.subheader("Update Incident Status")
    with st.form("update_incident_status_form"):
        us_id = st.number_input("Incident ID", step=1)
        us_status = st.selectbox("New Status", ["open", "in progress", "resolved"])
        update_submit = st.form_submit_button("Update")

    if update_submit and us_id:
        rows = update_incident_status(conn, us_id, us_status)
        if rows:
            st.success("Incident status updated!")
        else:
            st.error("No incident found with that Incident ID.")
        st.rerun()

    st.subheader("Delete Incident")
    with st.form("delete_incident_form"):
        del_id = st.number_input("Incident ID to Delete", step=1)
        del_submit = st.form_submit_button("Delete")

    if del_submit and del_id:
        rows = delete_incident(conn, del_id)
        if rows:
            st.success(f"Incident {del_id} deleted successfully!")
        else:
            st.error("No incident found with that Incident ID.")
        st.rerun()

# TAB 2 — GEMINI AI CHAT

with tab2:
    st.header("Cybersecurity AI Chat")

    # API key input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        placeholder="AIza...",
        key="cyber_ai_api_key"
    )
    if not api_key:
        st.info("Enter your API key to use the AI chat.")
        st.stop()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash"

    # Initialize session state for chat
    if "cyber_ai_messages" not in st.session_state:
        st.session_state.cyber_ai_messages = [
            {
                "role": "system",
                "content": """You are a cybersecurity expert assistant.
- Analyze incidents and threats
- Provide technical guidance
- Explain attack vectors and mitigations
- Use MITRE ATT&CK / CVE terminology
- Prioritize actionable recommendations
Tone: Professional, technical
Format: Clear, structured responses."""
            }
        ]

    # Clear Chat Button
    if st.button("!!Clear Chat!!"):
        st.session_state.cyber_ai_messages = [
            st.session_state.cyber_ai_messages[0]  # keep system message
        ]
        st.rerun()

    # Display previous messages (skip system message)
    for msg in st.session_state.cyber_ai_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    # Chat input
    prompt = st.chat_input("Ask AI about cybersecurity...", key="cyber_ai_prompt")
    if prompt:
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to session state
        st.session_state.cyber_ai_messages.append({"role": "user", "content": prompt})

        # Flatten conversation to a string
        conversation = ""
        for msg in st.session_state.cyber_ai_messages:
            if msg["role"] == "system":
                conversation += f"System: {msg['content']}\n"
            else:
                conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"

        # Call Gemini API
        response = client.models.generate_content(
            model=model_name,
            contents=conversation
        )
        reply = response.text

        # Show assistant message
        with st.chat_message("assistant"):
            st.markdown(reply)

        # Save assistant response
        st.session_state.cyber_ai_messages.append({"role": "assistant", "content": reply})

# LOGOUT BUTTON
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("home.py")
