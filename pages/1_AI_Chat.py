"""
AI-Student Assistant — AI Chat Page
"""

import streamlit as st
from utils.ai_engine import ask_ai, get_active_api_key_info

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="AI Chat — AI-Student Assistant",
    page_icon="🤖",
    layout="wide",
)

# ── CSS (Light & High Contrast) ──────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: #FAFAFC !important;
    color: #0F172A !important;
}

/* Page Header */
.page-header {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}
.page-header h1 {
    color: #0F172A !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin: 0 0 6px 0 !important;
}
.page-header p {
    color: #64748B !important;
    font-size: 15px !important;
    margin: 0 !important;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border: 1px solid #EAECEF !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03) !important;
    color: #0F172A !important;
}

/* Chat Input */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}
[data-testid="stChatInput"] textarea {
    color: #0F172A !important;
}

/* Action Button */
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>💬 AI Study Tutor</h1>
    <p>Ask questions on any subject, request simplified explanations, or prepare for exams with your personal AI tutor.</p>
</div>
""", unsafe_allow_html=True)

# Check active API key
active_key, _ = get_active_api_key_info()
if not active_key:
    st.info(
        "💡 **Student Tip:** To enable AI answers, go to the **7_Settings** page in the left sidebar "
        "and paste your free Groq API key (free at [console.groq.com/keys](https://console.groq.com/keys))."
    )

# ── Controls Bar ─────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    language = st.selectbox(
        "🌍 Response Language",
        ["English", "Urdu", "Sindhi"],
        help="Select the language for the AI tutor's answers.",
    )
with col2:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.divider()

# ── Chat Session State ───────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Hello! I am your AI-Student Assistant.**\n\nWhat subject or topic are you studying today? You can ask me to explain concepts, solve homework problems, or summarize topics.",
        }
    ]

# ── Render Chat Messages ─────────────────────
for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── User Input ───────────────────────────────
prompt = st.chat_input("Type your question here (e.g., 'Explain photosynthesis simply')...")

if prompt:
    # Save & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            answer = ask_ai(prompt, language)
        st.markdown(answer)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})