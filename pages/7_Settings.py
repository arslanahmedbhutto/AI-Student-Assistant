"""
AI-Student Assistant — Settings & System Status
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Settings — AI-Student Assistant",
    page_icon="⚙️",
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
.settings-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    margin-bottom: 20px;
}
.settings-card h3 {
    margin-top: 0 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>⚙️ System Settings & Overview</h1>
    <p>Manage API configurations, monitor deployment health, and verify active inference backends.</p>
</div>
""", unsafe_allow_html=True)

col_api, col_spec = st.columns([1, 1])

with col_api:
    st.markdown('<div class="settings-card"><h3>🔑 API Authentication</h3>', unsafe_allow_html=True)
    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key:
        st.success(f"✅ **Groq API Connected:** Key active (`...{api_key[-6:]}`)")
    else:
        st.error("❌ **Groq API Key Not Found:** Add `GROQ_API_KEY` to `.env` or Streamlit Cloud Secrets.")

    st.markdown("""
    **Streamlit Cloud Setup Guide:**
    1. Go to your app settings on [share.streamlit.io](https://share.streamlit.io).
    2. Click **Secrets** in the left menu.
    3. Add:
    ```toml
    GROQ_API_KEY = "gsk_your_key_here"
    ```
    </div>
    """, unsafe_allow_html=True)

with col_spec:
    st.markdown('<div class="settings-card"><h3>💻 Architecture Overview</h3>', unsafe_allow_html=True)
    st.markdown("""
    | Component | Engine / Version |
    |---|---|
    | **LLM Inference** | Groq Llama 3.3 70B Versatile |
    | **Vector Retrieval** | FAISS FlatL2 (Dense Hash / Ollama) |
    | **Chunking Strategy** | RecursiveCharacterSplitter (500 chars) |
    | **Document Parser** | pdfplumber |
    | **UI Framework** | Streamlit Modern Web Architecture |
    </div>
    """, unsafe_allow_html=True)

st.caption("AI-Student Assistant v2.0 · Production Ready")