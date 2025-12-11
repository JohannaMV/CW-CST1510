import streamlit as st
from google import genai

st.title("Gemini AI Assistant")

api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password",
    placeholder="AIza..."
)
if not api_key:
    st.warning("Please enter your Gemini API key to continue.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- find a valid model supporting generate_content ---
available = []
for m in client.models.list():
    if "generateContent" in m.supported_actions or "generate_content" in getattr(m, "supported_actions", []):
        available.append(m.name)

if not available:
    st.error("No supported Gemini models found for generate_content.")
    st.stop()

model_name = available[0]  # pick first valid model

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something…")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # build full conversation
    conversation = "\n".join(f"{m['role']}: {m['content']}"
                              for m in st.session_state.messages)

    response = client.models.generate_content(
        model=model_name,
        contents=conversation
    )
    reply = response.text

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})



