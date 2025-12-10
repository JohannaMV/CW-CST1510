import streamlit as st
import google.generativeai as genai

st.title("Gemini AI Assistant")

# Input box for API key
api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password",
    placeholder="AIza..."
)

# Stop the app until user inserts key
if not api_key:
    st.warning("Please enter your Gemini API key to continue.")
    st.stop()

# Configure Gemini with user-provided key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask something...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build conversation string for Gemini
    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in st.session_state.messages
    )

    # Get model response
    response = model.generate_content(conversation)
    reply = response.text

    # Show reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
