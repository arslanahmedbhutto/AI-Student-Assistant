"""
AI-Student Assistant — Session History
"""

import streamlit as st

st.set_page_config(
    page_title="Session History — AI-Student Assistant",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: #FAFAFC !important;
    color: #0F172A !important;
}
.page-hero {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}
.page-hero h1 {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin: 0 0 6px 0 !important;
}
.page-hero p {
    color: #64748B !important;
    font-size: 15px !important;
    margin: 0 !important;
}
.history-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}
.history-role {
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>📚 Study Session History</h1>
    <p>Review past interactions, generated summaries, and practice quizzes from your current study session.</p>
</div>
""", unsafe_allow_html=True)

tab_chats, tab_sums, tab_qzs = st.tabs(["💬 Tutor Messages", "📝 PDF Summaries", "❓ Practice Quizzes"])

with tab_chats:
    messages = st.session_state.get("messages", [])
    if messages:
        for msg in messages:
            is_user = msg["role"] == "user"
            color = "#4F46E5" if is_user else "#059669"
            label = "🧑‍🎓 You" if is_user else "🤖 AI Tutor"
            st.markdown(f"""
            <div class="history-card" style="border-left: 4px solid {color};">
                <div class="history-role" style="color: {color};">{label}</div>
                <div>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active chat history yet. Start a discussion in the AI Tutor Chat page.")

with tab_sums:
    if "pdf_summary" in st.session_state:
        st.markdown(f'<div class="history-card"><h4>Recent Document Summary</h4>{st.session_state.pdf_summary}</div>', unsafe_allow_html=True)
    else:
        st.info("No PDF summary generated during this session yet.")

with tab_qzs:
    if "pdf_quiz" in st.session_state:
        st.markdown(f'<div class="history-card"><h4>Recent Practice Quiz</h4>{st.session_state.pdf_quiz}</div>', unsafe_allow_html=True)
    else:
        st.info("No practice quiz generated during this session yet.")

st.caption("ℹ️ Session history is stored in local browser memory and resets when the session is closed.")