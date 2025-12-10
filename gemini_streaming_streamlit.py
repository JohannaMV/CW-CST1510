import streamlit as st
from google import genai

st.title("Gemini Streaming Chat (New API)")

# API key input
api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password",
    placeholder="AIza..."
)

if not api_key:
    st.warning("Please enter your Gemini API key to continue.")
    st.stop()

# Create client (new API)
client = genai.Client(api_key=api_key)
model_name = "gemini-1.5-flash"

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Say something...")

if prompt:
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation
    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in st.session_state.messages
    )

    # Assistant streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full = ""

        # NEW STREAMING METHOD
        for chunk in client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=prompt
        ):
            if chunk.text:
                st.write(chunk.text)

            if chunk.text:
                full += chunk.text
                container.markdown(full + "▌")

        container.markdown(full)

    # Save the assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": full}
    )
