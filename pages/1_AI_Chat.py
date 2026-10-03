"""
AI-Student Assistant — AI Chat Page

Features:
  - AI Chat using Groq (Llama 3.3 70B)
  - Chat History with clear button
  - English / Urdu / Sindhi Support
  - Modern chat UI
"""

import streamlit as st
from utils.ai_engine import ask_ai

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="AI Chat", page_icon="🤖", layout="wide")

# ── CSS ──────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
}
.ai-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.35);
}
.ai-header h1 { font-size: 40px; font-weight: 800; }
.ai-header p { opacity: 0.9; }
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 1px solid rgba(255,255,255,0.5);
}
[data-testid="stChatInput"] {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
}
.stButton button:hover { transform: scale(1.03); }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────
st.markdown("""
<div class="ai-header">
    <h1>🤖 AI-Student Chat</h1>
    <p>Your personal AI learning companion — powered by Groq Llama 3.3</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ── Language Selection ───────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    language = st.selectbox(
        "🌍 Choose Response Language",
        ["English", "Urdu", "Sindhi"],
    )
with col2:
    st.info("🤖 **AI Model**\n\nGroq — Llama 3.3 70B")

st.divider()

# ── Chat History ─────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Clear Chat ───────────────────────────────
if st.button("🗑 Clear Conversation"):
    st.session_state.messages = []
    st.success("Chat history cleared!")
    st.rerun()

# ── Display Messages ─────────────────────────
for message in st.session_state.messages:
    avatar = "👩‍🎓" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── User Input ───────────────────────────────
prompt = st.chat_input("Ask anything about your studies...")

if prompt:
    # Save & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👩‍🎓"):
        st.markdown(prompt)

    # Get & display AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 AI is thinking..."):
            answer = ask_ai(prompt, language)
        st.markdown(answer)

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})