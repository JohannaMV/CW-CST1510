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
        key="it_ai_api_key"
    )
    if not api_key:
        st.info("Enter your API key to use the AI chat.")
        st.stop()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.0-flash"

    # Initialize session state for chat with system prompt
    if "it_ai_messages" not in st.session_state:
        st.session_state.it_ai_messages = [
            {
                "role": "system",
                "content": """You are an IT operations expert assistant.
- Analyze IT tickets and operational issues
- Suggest resolutions and troubleshooting steps
- Prioritize critical issues
- Use ITIL and standard IT operations terminology
Tone: Professional, technical
Format: Clear, structured responses."""
            }
        ]

    # Clear Chat button
    if st.button("!!Clear Chat!!"):
        st.session_state.it_ai_messages = [
            st.session_state.it_ai_messages[0]  # keep system message
        ]
        st.rerun()

    # Display previous messages (skip system)
    for msg in st.session_state.it_ai_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Ask AI about IT operations...", key="it_ai_prompt")
    if prompt:
        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to history
        st.session_state.it_ai_messages.append({"role": "user", "content": prompt})

        # Flatten conversation to a string for Gemini
        conversation = ""
        for msg in st.session_state.it_ai_messages:
            if msg["role"] == "system":
                conversation += f"System: {msg['content']}\n"
            else:
                conversation += f"{msg['role'].capitalize()}: {msg['content']}\n"

        # Call Gemini API
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=conversation
            )
            reply = response.text
        except Exception as e:
            reply = f"API Error or quota exceeded: {str(e)}"

        # Show assistant message
        with st.chat_message("assistant"):
            st.markdown(reply)

        # Save assistant response
        st.session_state.it_ai_messages.append({"role": "assistant", "content": reply})

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("home.py")
