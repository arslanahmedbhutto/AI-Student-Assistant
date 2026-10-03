"""
AI-Student Assistant — Summarizer Page
"""

import streamlit as st
from utils.ai_engine import ask_ai

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="AI Summarizer", page_icon="📝", layout="wide")

# ── CSS ──────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
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

# ── UI ───────────────────────────────────────
st.title("📝 AI Summarizer")
st.write("Generate smart summaries from your notes using AI.")
st.divider()

notes = st.text_area("📚 Enter your notes", height=250)

language = st.selectbox("🌍 Language", ["English", "Urdu", "Sindhi"])

if st.button("✨ Generate Summary"):
    if notes:
        with st.spinner("🤖 AI is summarizing..."):
            prompt = (
                "Summarize the following study notes.\n"
                "Give important points, simple explanation, and key concepts.\n\n"
                f"Notes:\n{notes}"
            )
            summary = ask_ai(prompt, language)

        st.success("Summary Generated!")
        st.markdown(summary)
    else:
        st.warning("Please enter notes.")