# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 18:25:51 2025

@author: User
"""

import streamlit as st
import requests

# === CONFIGURE USERS (for demo; use env vars or DB in production) ===
USER_CREDENTIALS = {
    "tetra": "atex123",
    "tetra1": "atex321"
}

# === PAGE SETUP ===
st.set_page_config(page_title="TETRA ATEX Chatbot", page_icon="🤖")
st.title("🤖 Chat with TETRA AI Agent")

# === SESSION STATE SETUP ===
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# === LOGIN FORM ===
def login():
    with st.form("login_form", clear_on_submit=True):
        st.subheader("🔐 Please log in to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if USER_CREDENTIALS.get(username) == password:
                st.session_state["authenticated"] = True
                st.rerun()  # 🔄 Force app rerun to show chat
            else:
                st.error("❌ Invalid username or password")

# === HANDLE INPUT ===
def handle_input():
    user_input = st.session_state.input_buffer
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call the webhook
    try:
        res = requests.post(
            "https://n8n-r2og.onrender.com/webhook/5e170738-f424-424a-9be2-eb226b9c99af",
            json={"message": user_input},
            timeout=300
        )
        res.raise_for_status()
        reply = res.json().get("reply", "⚠️ No 'reply' key found in response.")
    except requests.exceptions.RequestException as e:
        reply = f"❌ Request Error: {e}"
    except Exception as e:
        reply = f"❌ Unexpected Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.session_state.update({"input_buffer": ""})

# === MAIN LOGIC ===
if not st.session_state["authenticated"]:
    login()
else:
    st.markdown("### 💬 Chat History")
    for msg in st.session_state["messages"]:
        role = "🧑‍💼 You" if msg['role'] == 'user' else "🤖 Agent"
        st.markdown(f"**{role}:**\n\n{msg['content']}")

    st.text_input(
        "Type your message and press Enter:",
        key="input_buffer",
        on_change=handle_input,
    )

    # Optional: reset chat button
    if st.button("🔄 Reset Chat"):
        st.session_state["messages"] = []
