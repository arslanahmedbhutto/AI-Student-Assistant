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
    line-height: 1.6;
}
.history-role {
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}
.stButton button {
    background: #EF4444 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(239, 68, 68, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header & Master Reset ────────────────────
col_h1, col_h2 = st.columns([3, 1])

with col_h1:
    st.markdown("""
    <div class="page-hero">
        <h1>📚 Study Session History</h1>
        <p>Review past interactions, questions, and generated materials across all features in your active session.</p>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear All Session History", use_container_width=True):
        keys_to_clear = [
            "messages", "pdf_chat_history", "pdf_summary", "pdf_quiz",
            "summarizer_notes", "summarizer_output",
            "quiz_topic", "quiz_output",
            "ocr_text", "ocr_summary", "ocr_quiz", "ocr_id"
        ]
        for k in keys_to_clear:
            st.session_state.pop(k, None)
        st.toast("All study session history cleared!", icon="🧹")
        st.rerun()

tab_chats, tab_pdf, tab_sums, tab_qzs, tab_ocr = st.tabs([
    "💬 Tutor Chat",
    "📄 PDF RAG Q&A",
    "📝 Summaries",
    "❓ Quizzes",
    "🖼️ OCR Scans"
])

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

with tab_pdf:
    pdf_chats = st.session_state.get("pdf_chat_history", [])
    if pdf_chats:
        for idx, item in enumerate(pdf_chats, 1):
            st.markdown(f"""
            <div class="history-card" style="border-left: 4px solid #4F46E5;">
                <div class="history-role" style="color: #4F46E5;">🧑‍🎓 Question #{idx}</div>
                <strong>{item['question']}</strong>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;">
                <div class="history-role" style="color: #059669;">🤖 Grounded Answer</div>
                <div>{item['answer']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No PDF questions asked yet. Upload a document in Document Assistant to get started.")

with tab_sums:
    has_sum = False
    if "pdf_summary" in st.session_state and st.session_state.pdf_summary:
        st.markdown(f'<div class="history-card"><h4>📄 Document PDF Summary</h4>{st.session_state.pdf_summary}</div>', unsafe_allow_html=True)
        has_sum = True
    if "summarizer_output" in st.session_state and st.session_state.summarizer_output:
        st.markdown(f'<div class="history-card"><h4>📝 Note Summarizer Result</h4>{st.session_state.summarizer_output}</div>', unsafe_allow_html=True)
        has_sum = True
    if "ocr_summary" in st.session_state and st.session_state.ocr_summary:
        st.markdown(f'<div class="history-card"><h4>🖼️ OCR Image Summary</h4>{st.session_state.ocr_summary}</div>', unsafe_allow_html=True)
        has_sum = True
    if not has_sum:
        st.info("No summaries generated yet in this session.")

with tab_qzs:
    has_qz = False
    if "pdf_quiz" in st.session_state and st.session_state.pdf_quiz:
        st.markdown(f'<div class="history-card"><h4>📄 Document Practice Quiz</h4>{st.session_state.pdf_quiz}</div>', unsafe_allow_html=True)
        has_qz = True
    if "quiz_output" in st.session_state and st.session_state.quiz_output:
        st.markdown(f'<div class="history-card"><h4>❓ Topic Practice Quiz</h4>{st.session_state.quiz_output}</div>', unsafe_allow_html=True)
        has_qz = True
    if "ocr_quiz" in st.session_state and st.session_state.ocr_quiz:
        st.markdown(f'<div class="history-card"><h4>🖼️ OCR Image Quiz</h4>{st.session_state.ocr_quiz}</div>', unsafe_allow_html=True)
        has_qz = True
    if not has_qz:
        st.info("No quizzes generated yet in this session.")

with tab_ocr:
    if "ocr_text" in st.session_state and st.session_state.ocr_text:
        st.markdown(f'<div class="history-card"><h4>🖼️ Recent OCR Extracted Text</h4><pre style="white-space: pre-wrap; font-family: inherit;">{st.session_state.ocr_text}</pre></div>', unsafe_allow_html=True)
    else:
        st.info("No OCR images transcribed yet in this session.")

st.caption("ℹ️ Session history is stored in local browser memory and resets when the session is closed or cleared.")