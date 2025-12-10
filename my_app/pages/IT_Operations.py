import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_tickets, insert_ticket

st.set_page_config(page_title="IT Ticket!", page_icon="🫧", layout="wide")

conn = connect_database()

st.title(".𖥔 ݁ ˖𓂃.☘︎ ݁˖ IT Tickets Dashboard .𖥔 ݁ ˖𓂃.☘︎ ݁˖")

#Show table of all tickets
tickets = get_all_tickets(conn)
st.dataframe(tickets, use_container_width=True)

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

# Logout button
st.divider()
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("home.py")
