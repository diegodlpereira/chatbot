import streamlit as st
import requests

# --- Configuration ---
API_URL = "http://localhost:3000/api/chat/completions"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImE3N2IxYTk2LTY5YWMtNGYyOS1iZDcyLWQ2YWQ1NDhkMDdlOCJ9.Iz5f9SvRbP5T6Vkk8lvT94ReDo399a9V4rlACefqwc0"  # Replace with your real token
MODEL_NAME = "nezbistro-chatbot"

# --- Streamlit setup ---
st.set_page_config(page_title="Nez Bistro Chatbot", layout="centered")
st.title("🍷 Nez Bistro Chatbot")
st.markdown("Pergunte sobre o menu, vinhos ou sugestões do chef!")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Em que posso te ajudar?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build payload and headers
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages
    }
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send request
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    except Exception as e:
        st.error(f"Erro ao conectar com o chatbot: {e}")
