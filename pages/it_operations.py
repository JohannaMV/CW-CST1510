import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket
from services.ai_assistant import AIAssistant

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="IT Tickets!", page_icon="🫧", layout="wide")

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
st.title("🫧 IT Tickets Dashboard 🫧")
tab1, tab2 = st.tabs(["Tickets", "AI Chat"])

# ==================================================
# TAB 1 — TICKET MANAGEMENT (PDF STEP 6)
# ==================================================
with tab1:
    st.subheader("All IT Tickets")

    rows = db.fetch_all(
        """SELECT ticket_id, priority, description, status, assigned_to
           FROM it_tickets"""
    )

    tickets: list[ITTicket] = []
    for row in rows:
        ticket = ITTicket(
            ticket_id=row[0],
            title=row[2],
            priority=row[1],
            status=row[3],
            assigned_to=row[4],
        )
        tickets.append(ticket)

    for ticket in tickets:
        st.write(ticket)
        st.divider()

    # -------------------------------
    # Add Ticket
    # -------------------------------
    st.subheader("Add New Ticket")
    with st.form("add_ticket_form"):
        ticket_id = st.number_input("Ticket ID", step=1)
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        description = st.text_area("Description")
        status = st.selectbox(
            "Status", ["Open", "In Progress", "Resolved", "Closed"]
        )
        assigned_to = st.text_input("Assigned To")
        created_at = st.date_input("Created At")
        resolution_time = st.number_input(
            "Resolution Time (hours)", step=1
        )
        add_btn = st.form_submit_button("Add Ticket")

    if add_btn and description:
        db.execute_query(
            """INSERT INTO it_tickets
               (ticket_id, priority, description, status, assigned_to,
                created_at, resolution_time_hours)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ticket_id,
                priority,
                description,
                status,
                assigned_to,
                created_at,
                resolution_time,
            ),
        )
        st.success("Ticket added successfully!")
        st.rerun()

    # -------------------------------
    # Update Ticket Status
    # -------------------------------
    st.subheader("Update Ticket Status")
    with st.form("update_ticket_form"):
        upd_id = st.number_input("Ticket ID to Update", step=1)
        new_status = st.selectbox(
            "New Status", ["Open", "In Progress", "Resolved", "Closed"]
        )
        update_btn = st.form_submit_button("Update Ticket")

    if update_btn:
        cur = db.execute_query(
            "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
            (new_status, upd_id),
        )
        if cur.rowcount > 0:
            st.success("Ticket status updated!")
        else:
            st.error("Ticket not found.")
        st.rerun()

    # -------------------------------
    # Delete Ticket
    # -------------------------------
    st.subheader("Delete Ticket")
    with st.form("delete_ticket_form"):
        del_id = st.number_input("Ticket ID to Delete", step=1)
        del_btn = st.form_submit_button("Delete Ticket")

    if del_btn:
        cur = db.execute_query(
            "DELETE FROM it_tickets WHERE ticket_id = ?",
            (del_id,),
        )
        if cur.rowcount > 0:
            st.success("Ticket deleted.")
        else:
            st.error("Ticket not found.")
        st.rerun()

# ==================================================
# TAB 2 — AI ASSISTANT (PDF STEP 3.3)
# ==================================================
with tab2:
    st.header("IT Operations AI Assistant")

    api_key = st.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.info("Please enter your Gemini API key.")
        st.stop()

    ai = AIAssistant(
        api_key=api_key,
        system_prompt="""You are an IT operations expert assistant.
    Analyze IT tickets and operational issues.
    Suggest troubleshooting and resolution steps.
    Prioritize critical incidents.
    Use ITIL terminology.
    Provide clear, structured responses."""
    )

    if "it_ai_history" not in st.session_state:
        st.session_state.it_ai_history = []

    if st.button("Clear Chat"):
        st.session_state.it_ai_history.clear()
        ai.clear_history()
        st.rerun()

    for msg in st.session_state.it_ai_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask about IT operations...")
    if user_prompt:
        st.session_state.it_ai_history.append(
            {"role": "user", "content": user_prompt}
        )

        reply = ai.send_message(user_prompt)

        st.session_state.it_ai_history.append(
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
