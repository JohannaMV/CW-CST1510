import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_tickets, insert_ticket, update_ticket_status, delete_ticket
from google import genai

st.set_page_config(page_title="IT Ticket!", page_icon="🫧", layout="wide")

conn = connect_database()

st.title("🫧IT Tickets Dashboard!🫧")
tab1, tab2 = st.tabs(["Tickets", "AI Chat"])

#Show table of all tickets
tickets = get_all_tickets(conn)
st.dataframe(tickets, use_container_width=True)

st.header("Add Ticket")
#Form to add a new ticket
with st.form("new ticket"):
    ticket_id = st.number_input("Ticket ID", step=1)
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    assigned_to = st.text_input("Assigned To")
    created_at = st.date_input("Created At")
    resolution_time_hours = st.number_input("Resolution Time (hours)", step=1)

    submitted = st.form_submit_button("Add Ticket")

# ---- Insert to database ----
if submitted and description:
    insert_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
    st.success("Ticket added to database")
    st.rerun()

st.header("Update Ticket Status")

with st.form("update_ticket_form"):
    u_ticket_id = st.number_input("Ticket ID to Update", step=1)
    new_status = st.selectbox("New Status", ["open", "in progress", "resolved"])

    update_submitted = st.form_submit_button("Update Ticket")

if update_submitted:
    # Call your update function
    rows_affected = update_ticket_status(conn, u_ticket_id, new_status)

    if rows_affected > 0:
        st.success(f"Successfully updated Ticket ID {u_ticket_id} to status '{new_status}'.")
        st.rerun()
    else:
        st.error(f"Ticket ID {u_ticket_id} not found. No updates were made.")


st.subheader("Delete Ticket")

with st.form("delete_ticket_form"):
    del_ticket_id = st.number_input("Ticket ID to Delete", step=1)
    delete_submitted = st.form_submit_button("Delete Ticket")

if delete_submitted and del_ticket_id:
    rows = delete_ticket(conn, del_ticket_id)
    if rows:
        st.success(f"Ticket {del_ticket_id} deleted successfully!")
    else:
        st.error("No ticket found with that Ticket ID.")
    st.rerun()

with tab2:
    st.header("IT Operations AI Chat")

    # API key input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        placeholder="AIza...",
        key="ai_api_key"
    )
    if not api_key:
        st.warning("Please enter your Gemini API key to continue.")
        st.stop()

    # Gemini client
    client = genai.Client(api_key=api_key)

    # Pick first available model for generate_content
    available = [m.name for m in client.models.list() if "generateContent" in getattr(m, "supported_actions", [])]
    if not available:
        st.error("No supported Gemini models found for generate_content.")
        st.stop()
    model_name = available[0]

    # Initialize session state for chat
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    # Display previous messages
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Ask AI about IT Operations...", key="ai_prompt")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.ai_messages.append({"role": "user", "content": prompt})

        conversation = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.ai_messages)

        # Get AI response
        response = client.models.generate_content(model=model_name, contents=conversation)
        reply = response.text

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.ai_messages.append({"role": "assistant", "content": reply})

# Logout button
st.divider()
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("home.py")
