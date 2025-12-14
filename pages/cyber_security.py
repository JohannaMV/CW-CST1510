import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
from services.ai_assistant import AIAssistant

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Cyber!", page_icon="🫧", layout="wide")

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
# ---------------------------------
st.title("🫧 Cyber Incidents Dashboard 🫧")
tab1, tab2 = st.tabs(["Incidents", "AI Chat"])

# ==================================================
# TAB 1 — INCIDENT MANAGEMENT (PDF STEP 6)
# ==================================================
with tab1:
    st.subheader("All Incidents")

    rows = db.fetch_all(
        "SELECT id, category, severity, status, description FROM security_incidents"
    )

    incidents: list[SecurityIncident] = []
    for row in rows:
        incident = SecurityIncident(
            incident_id=row[0],
            incident_type=row[1],
            severity=row[2],
            status=row[3],
            description=row[4],
        )
        incidents.append(incident)

    for incident in incidents:
        st.write(incident)
        st.write("Severity level:", incident.get_severity_level())
        st.divider()

    # Add Incident

    st.subheader("Add New Incident")
    with st.form("add_incident_form"):
        inc_id = st.number_input("Incident ID", step=1)
        category = st.text_input("Category")
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        status = st.selectbox("Status", ["open", "in progress", "resolved"])
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Incident")

    if submitted and category:
        db.execute_query(
            """INSERT INTO security_incidents
               (id, category, severity, status, description)
               VALUES (?, ?, ?, ?, ?)""",
            (inc_id, category, severity, status, description),
        )
        st.success("Incident added successfully!")
        st.rerun()

    # -------------------------------
    # Update Status
    # -------------------------------
    st.subheader("Update Incident Status")
    with st.form("update_status_form"):
        upd_id = st.number_input("Incident ID to Update", step=1)
        new_status = st.selectbox(
            "New Status", ["open", "in progress", "resolved"]
        )
        update_btn = st.form_submit_button("Update Status")

    if update_btn:
        cur = db.execute_query(
            "UPDATE security_incidents SET status = ? WHERE id = ?",
            (new_status, upd_id),
        )
        if cur.rowcount > 0:
            st.success("Status updated!")
        else:
            st.error("Incident not found.")
        st.rerun()

    # -------------------------------
    # Delete Incident
    # -------------------------------
    st.subheader("Delete Incident")
    with st.form("delete_incident_form"):
        del_id = st.number_input("Incident ID to Delete", step=1)
        del_btn = st.form_submit_button("Delete Incident")

    if del_btn:
        cur = db.execute_query(
            "DELETE FROM security_incidents WHERE id = ?",
            (del_id,),
        )
        if cur.rowcount > 0:
            st.success("Incident deleted.")
        else:
            st.error("Incident not found.")
        st.rerun()

# ==================================================
# TAB 2 — AI ASSISTANT (PDF STEP 3.3)
# ==================================================
with tab2:
    st.header("Cybersecurity AI Assistant")

    api_key = st.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.info("Please enter your Gemini API key.")
        st.stop()

    ai = AIAssistant(
        api_key=api_key,
        system_prompt="""You are a cybersecurity expert assistant.
Analyze incidents, threats, and vulnerabilities.
Use MITRE ATT&CK and CVE terminology.
Provide clear mitigation steps."""
    )

    if "cyber_ai_history" not in st.session_state:
        st.session_state.cyber_ai_history = []

    if st.button("Clear Chat"):
        st.session_state.cyber_ai_history.clear()
        ai.clear_history()
        st.rerun()

    for msg in st.session_state.cyber_ai_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask about cybersecurity...")
    if user_prompt:
        st.session_state.cyber_ai_history.append(
            {"role": "user", "content": user_prompt}
        )

        reply = ai.send_message(user_prompt)

        st.session_state.cyber_ai_history.append(
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