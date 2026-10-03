"""
AI-Student Assistant — Settings & API Key Manager
Allows each student to securely input, verify, and use their own Groq API key.
"""

import os
import streamlit as st
from utils.ai_engine import (
    get_active_api_key_info,
    get_active_model,
    test_api_key,
)

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
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    margin-bottom: 20px;
}
.settings-card h3 {
    margin: 0 0 8px 0 !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
}
.settings-card p.subtitle {
    color: #64748B !important;
    font-size: 14px !important;
    margin: 0 0 20px 0 !important;
}
.guide-box {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 16px;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.6;
}
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>⚙️ Student Settings & API Key Setup</h1>
    <p>Configure your personal Groq API key and select preferred AI model settings for your study session.</p>
</div>
""", unsafe_allow_html=True)

# Retrieve current key info
active_key, active_source = get_active_api_key_info()
masked_key = f"gsk_...{active_key[-6:]}" if active_key else "None"

col_main, col_info = st.columns([3, 2])

with col_main:
    # ── 1. Student API Key Configuration ──────────────────────────
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 🔑 Personal Groq API Key")
    st.markdown(
        '<p class="subtitle">Each student can add their own free Groq API key here. '
        'Your key is stored securely in your private session and is never shared.</p>',
        unsafe_allow_html=True,
    )

    current_custom_key = st.session_state.get("custom_groq_api_key", "")
    new_key_input = st.text_input(
        "Paste your Groq API Key:",
        value=current_custom_key,
        type="password",
        placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Paste your personal Groq key here. It will activate immediately.",
    )

    btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1.2, 1])

    with btn_col1:
        if st.button("💾 Save & Use Key", use_container_width=True):
            if new_key_input.strip():
                st.session_state["custom_groq_api_key"] = new_key_input.strip()
                with st.spinner("Verifying key with Groq..."):
                    success, msg = test_api_key(new_key_input.strip())
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ Key saved, but test failed: {msg}")
                st.rerun()
            else:
                st.warning("Please enter a valid API key string.")

    with btn_col2:
        if st.button("🧪 Test Connection", use_container_width=True):
            with st.spinner("Testing Groq connection..."):
                test_target = new_key_input.strip() or active_key
                success, msg = test_api_key(test_target)
            if success:
                st.success(f"✅ Connection Successful: {msg}")
            else:
                st.error(f"❌ Connection Failed: {msg}")

    with btn_col3:
        if st.button("🗑️ Reset Key", use_container_width=True):
            st.session_state.pop("custom_groq_api_key", None)
            st.info("Custom session key removed.")
            st.rerun()

    st.markdown("""
    <div class="guide-box">
        <strong>💡 Need a free Groq API key?</strong><br>
        1. Open <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a>.<br>
        2. Sign up or log in (free, no credit card required).<br>
        3. Click <strong>Create API Key</strong>, copy it, and paste it above!
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 2. Model Selection ─────────────────────────────────────────
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Preferred AI Model")
    st.markdown(
        '<p class="subtitle">Choose which high-speed Groq model powers your explanations and quizzes.</p>',
        unsafe_allow_html=True,
    )

    model_options = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    current_model = get_active_model()
    default_idx = model_options.index(current_model) if current_model in model_options else 0

    selected_model = st.selectbox(
        "Active Model:",
        options=model_options,
        index=default_idx,
        help="llama-3.3-70b is recommended for best comprehension and accuracy.",
    )

    if selected_model != current_model:
        st.session_state["selected_groq_model"] = selected_model
        st.success(f"✅ Model changed to `{selected_model}`")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


with col_info:
    # ── Live Status Card ──────────────────────────────────────────
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 📡 Connection Status")

    if active_key:
        st.success(f"🟢 **API Status:** Active & Configured")
        st.write(f"• **Key:** `{masked_key}`")
        st.write(f"• **Active Source:** `{active_source}`")
        st.write(f"• **Selected Model:** `{get_active_model()}`")
    else:
        st.error("🔴 **API Status:** Not Configured")
        st.write("No active API key found. Enter your key on the left to start using AI features.")

    st.markdown("---")
    st.markdown("#### ☁️ Streamlit Cloud Hosting")
    st.markdown("""
    If you are the repository owner hosting this on **Streamlit Cloud**:
    - You can provide a shared default key via **App Settings → Secrets**:
    ```toml
    GROQ_API_KEY = "gsk_your_key_here"
    ```
    - Individual students can still override it anytime with their own key in this Settings page!
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("AI-Student Assistant v2.0 · Session-based Multi-user Support")