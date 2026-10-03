"""
AI-Student Assistant — Smart Summarizer
"""

import streamlit as st
from utils.ai_engine import ask_ai, get_active_provider

st.set_page_config(
    page_title="Summarizer — AI-Student Assistant",
    page_icon="📝",
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
.result-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 28px;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    line-height: 1.7;
}
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>📝 Smart Note Summarizer</h1>
    <p>Transform dense study notes, articles, or chapters into high-yield executive summaries.</p>
</div>
""", unsafe_allow_html=True)

# State initialization
if "summarizer_notes" not in st.session_state:
    st.session_state.summarizer_notes = ""
if "summarizer_output" not in st.session_state:
    st.session_state.summarizer_output = ""

col_input, col_settings = st.columns([3, 1])

with col_settings:
    language = st.selectbox("🌍 Summary Language", ["English", "Urdu", "Sindhi"])
    summary_format = st.selectbox(
        "📋 Format",
        ["Key Bullet Points", "Executive Overview", "Detailed Breakdown"]
    )
    st.write("")
    if st.button("🗑️ Clear / Reset", use_container_width=True):
        st.session_state.summarizer_notes = ""
        st.session_state.summarizer_output = ""
        st.toast("Summarizer cleared!", icon="🧹")
        st.rerun()

with col_input:
    notes_val = st.text_area(
        "Paste your study notes or article text here:",
        value=st.session_state.summarizer_notes,
        height=260,
        placeholder="e.g. Paste lecture notes, textbook passages, or definitions..."
    )
    st.session_state.summarizer_notes = notes_val

if st.button("✨ Generate AI Summary", use_container_width=True):
    if st.session_state.summarizer_notes.strip():
        with st.spinner("Analyzing and condensing your notes..."):
            prompt = (
                f"You are AI-Student Assistant.\n"
                f"Summarize the study notes below in {language}.\n"
                f"Format requested: {summary_format}.\n"
                f"Provide clear, high-yield takeaways that a student can easily memorize.\n\n"
                f"Notes:\n{st.session_state.summarizer_notes}"
            )
            st.session_state.summarizer_output = ask_ai(prompt, language)
        st.rerun()
    else:
        st.warning("Please paste some notes or text to summarize.")

# Persisted result card
if st.session_state.summarizer_output:
    st.markdown(f'<div class="result-card">{st.session_state.summarizer_output}</div>', unsafe_allow_html=True)
    st.download_button(
        "📥 Download Summary (.txt)",
        data=st.session_state.summarizer_output,
        file_name="notes_summary.txt",
        mime="text/plain",
    )