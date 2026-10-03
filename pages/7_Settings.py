"""
AI-Student Assistant — Settings Page
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
}
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Settings")
st.divider()

# ── API Key Status ───────────────────────────
st.subheader("🔑 API Configuration")
api_key = os.getenv("GROQ_API_KEY", "")
if api_key:
    st.success(f"✅ Groq API Key loaded (ends with ...{api_key[-6:]})")
else:
    st.error("❌ GROQ_API_KEY not found. Add it to your `.env` file.")

# ── Model Info ───────────────────────────────
st.subheader("🤖 AI Model")
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
st.info(f"**Current Model:** `{model}`\n\nSet `GROQ_MODEL` in `.env` to change.")

# ── App Info ─────────────────────────────────
st.subheader("ℹ️ About")
st.markdown("""
| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM** | Groq (Llama 3.3 70B) |
| **Embeddings** | Ollama (nomic-embed-text) |
| **Vector Store** | FAISS |
| **PDF Parsing** | pdfplumber |
| **OCR** | EasyOCR |
""")

st.divider()
st.caption("AI-Student Assistant v1.0 — © 2026")