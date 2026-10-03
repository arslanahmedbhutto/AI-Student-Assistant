"""
AI-Student Assistant — History Page
Shows chat history and generated content from the current session.
"""

import streamlit as st

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="History", page_icon="📚", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Session History")
st.divider()

# ── Chat History ─────────────────────────────
st.subheader("💬 Chat Messages")
messages = st.session_state.get("messages", [])
if messages:
    for msg in messages:
        role = "🧑‍🎓 You" if msg["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")
        st.markdown("---")
else:
    st.info("No chat messages yet. Go to AI Chat to start a conversation.")

# ── PDF Summary ──────────────────────────────
st.subheader("📝 Last PDF Summary")
if "pdf_summary" in st.session_state:
    st.write(st.session_state.pdf_summary)
else:
    st.info("No summary generated yet. Upload a PDF in the PDF Assistant.")

# ── PDF Quiz ─────────────────────────────────
st.subheader("❓ Last PDF Quiz")
if "pdf_quiz" in st.session_state:
    st.write(st.session_state.pdf_quiz)
else:
    st.info("No quiz generated yet. Upload a PDF in the PDF Assistant.")

st.divider()
st.caption("History is stored in your current session. It resets when you close the browser tab.")