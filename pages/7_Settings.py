"""
AI-Student Assistant — Multi-Provider API & Model Settings
Supports Groq, Google Gemini, OpenAI, and xAI (Grok).
"""

import os
import streamlit as st
from utils.ai_engine import (
    PROVIDERS,
    get_active_provider,
    get_active_model,
    get_api_key_for_provider,
    test_api_key,
)

st.set_page_config(
    page_title="API Settings — AI-Student Assistant",
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
    margin: 0 0 18px 0 !important;
}
.badge-active {
    display: inline-block;
    background: #ECFDF5;
    color: #059669;
    border: 1px solid #A7F3D0;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
}
.guide-box {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 14px 0;
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
    <h1>⚙️ Multi-Provider AI Settings</h1>
    <p>Choose your AI engine and configure API keys for Groq, Google Gemini, OpenAI, or xAI (Grok).</p>
</div>
""", unsafe_allow_html=True)

active_provider = get_active_provider()
active_model = get_active_model()
active_key, active_source = get_api_key_for_provider(active_provider)

col_config, col_overview = st.columns([3, 2])

with col_config:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 🔌 Select Active AI Provider")
    st.markdown(
        '<p class="subtitle">Select which provider you want the assistant to use across all tools.</p>',
        unsafe_allow_html=True,
    )

    provider_names = list(PROVIDERS.keys())
    selected_p = st.radio(
        "Choose Provider:",
        options=provider_names,
        index=provider_names.index(active_provider) if active_provider in provider_names else 0,
        horizontal=True,
        help="Select your preferred AI engine.",
    )

    if selected_p != active_provider:
        st.session_state["active_ai_provider"] = selected_p
        st.rerun()

    cfg = PROVIDERS[selected_p]
    p_key, p_source = get_api_key_for_provider(selected_p)

    st.markdown("---")
    st.markdown(f"#### 🔑 {cfg['display_name']} Configuration")

    st.markdown(f"""
    <div class="guide-box">
        <strong>Need an API Key for {selected_p}?</strong><br>
        👉 Get your key here: <a href="{cfg['signup_url']}" target="_blank">{cfg['signup_url']}</a>
    </div>
    """, unsafe_allow_html=True)

    session_key_name = f"custom_key_{selected_p}"
    current_val = st.session_state.get(session_key_name, "")

    key_input = st.text_input(
        f"Enter your {selected_p} API Key:",
        value=current_val,
        type="password",
        placeholder=cfg["placeholder"],
        help=f"Your {selected_p} key is stored securely in your private browser session.",
    )

    btn_c1, btn_c2, btn_c3 = st.columns([1.3, 1.2, 1])

    with btn_c1:
        if st.button(f"💾 Save & Use {selected_p}", use_container_width=True):
            if key_input.strip():
                st.session_state[session_key_name] = key_input.strip()
                st.session_state["active_ai_provider"] = selected_p
                with st.spinner(f"Verifying {selected_p} key..."):
                    ok, msg = test_api_key(selected_p, key_input.strip(), cfg["default_model"])
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ Key saved, but test failed: {msg}")
                st.rerun()
            else:
                st.warning("Please enter an API key.")

    with btn_c2:
        if st.button("🧪 Test Connection", use_container_width=True):
            test_target = key_input.strip() or p_key
            if test_target:
                with st.spinner(f"Testing {selected_p} connection..."):
                    ok, msg = test_api_key(selected_p, test_target)
                if ok:
                    st.success(f"✅ Connection OK: {msg}")
                else:
                    st.error(f"❌ Test Failed: {msg}")
            else:
                st.warning("No API key available to test.")

    with btn_c3:
        if st.button("🗑️ Clear Key", use_container_width=True):
            st.session_state.pop(session_key_name, None)
            st.info(f"Custom {selected_p} key cleared.")
            st.rerun()

    # Model Selection for this provider
    st.markdown("---")
    st.markdown("#### 🤖 Model Selection")
    provider_models = cfg["models"]
    model_session_key = f"active_model_{selected_p}"
    cur_p_model = st.session_state.get(model_session_key, cfg["default_model"])
    model_idx = provider_models.index(cur_p_model) if cur_p_model in provider_models else 0

    chosen_model = st.selectbox(
        f"Select {selected_p} Model:",
        options=provider_models,
        index=model_idx,
    )

    if chosen_model != cur_p_model:
        st.session_state[model_session_key] = chosen_model
        st.success(f"Model updated to `{chosen_model}`")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


with col_overview:
    # ── Live Status Overview ──────────────────────────────────────────
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 📡 Active Engine Status")

    if active_key:
        masked = f"...{active_key[-6:]}"
        st.success(f"🟢 **Active Provider:** `{active_provider}`")
        st.write(f"• **Model:** `{active_model}`")
        st.write(f"• **Key Source:** `{active_source}`")
        st.write(f"• **Key Preview:** `{masked}`")
    else:
        st.error(f"🔴 **Active Provider:** `{active_provider}` (No Key Configured)")
        st.write(f"Enter your {active_provider} API key on the left to activate it.")

    st.markdown("---")
    st.markdown("#### 📋 Provider Availability")

    for p_name, p_cfg in PROVIDERS.items():
        k, src = get_api_key_for_provider(p_name)
        status_icon = "🟢" if k else "⚪"
        status_text = f"Ready ({src})" if k else "Not set"
        st.markdown(f"**{status_icon} {p_name}:** {status_text}")

    st.markdown("---")
    st.markdown("#### ☁️ Streamlit Cloud Secrets (Repo Owner)")
    st.markdown("""
    To supply default keys on **Streamlit Cloud**, add any of these to your app secrets:
    ```toml
    GROQ_API_KEY = "gsk_..."
    GEMINI_API_KEY = "AIzaSy..."
    OPENAI_API_KEY = "sk-..."
    XAI_API_KEY = "xai-..."
    ```
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("AI-Student Assistant v2.0 · Multi-Provider Support")