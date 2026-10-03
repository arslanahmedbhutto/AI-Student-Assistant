"""
AI-Student Assistant — Multi-Provider API & Model Settings
Supports Groq (console.groq.com), xAI Grok (console.x.ai), Google Gemini, and OpenAI.
"""

import streamlit as st
from utils.ai_engine import (
    PROVIDERS,
    detect_provider_from_key,
    get_active_provider,
    get_active_model,
    get_api_key_for_provider,
    get_available_models_for_provider,
    test_api_key,
    is_valid_key_string,
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
    <h1>⚙️ Smart Multi-Provider AI Settings</h1>
    <p>Supports <strong>Groq (console.groq.com)</strong>, <strong>xAI Grok (console.x.ai)</strong>, <strong>Google Gemini</strong>, and <strong>OpenAI</strong>.</p>
</div>
""", unsafe_allow_html=True)

# Determine current active provider
active_p = get_active_provider()
saved_key, saved_source = get_api_key_for_provider(active_p)

col_config, col_overview = st.columns([3, 2])

with col_config:
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 🔑 Universal API Key Setup")
    st.markdown(
        '<p class="subtitle">Paste your key below. The engine detects your provider and configures the supported models automatically!</p>',
        unsafe_allow_html=True,
    )

    current_input_val = st.session_state.get(
        "user_pasted_api_key",
        saved_key if is_valid_key_string(saved_key) else "",
    )

    raw_input_key = st.text_input(
        "Paste your API Key:",
        value=current_input_val,
        type="password",
        placeholder="e.g. gsk_... (Groq) or xai-... (xAI Grok) or AIza... or sk-...",
        help="Paste your personal API key. Provider is auto-detected from prefix.",
    )

    st.session_state["user_pasted_api_key"] = raw_input_key

    detected = detect_provider_from_key(raw_input_key)

    # Provider Resolution
    if detected:
        st.success(f"🎯 **Auto-Detected:** `{detected}` — Models for `{detected}` loaded!")
        current_provider = detected
        st.session_state["active_ai_provider"] = detected
    else:
        provider_names = list(PROVIDERS.keys())
        current_provider = st.selectbox(
            "Or select provider manually:",
            options=provider_names,
            index=provider_names.index(active_p) if active_p in provider_names else 0,
            help="Choose your provider if prefix is not auto-detected:",
        )
        st.session_state["active_ai_provider"] = current_provider

    cfg = PROVIDERS[current_provider]

    # Action Buttons
    btn_c1, btn_c2, btn_c3 = st.columns([1.3, 1.2, 1])

    with btn_c1:
        if st.button(f"💾 Save & Use {current_provider}", use_container_width=True):
            if is_valid_key_string(raw_input_key):
                st.session_state[f"custom_key_{current_provider}"] = raw_input_key.strip()
                st.session_state["active_ai_provider"] = current_provider

                with st.spinner(f"Verifying {current_provider} key with {cfg['default_model']}..."):
                    ok, msg = test_api_key(current_provider, raw_input_key.strip(), cfg["default_model"])
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ Key saved, but test notice: {msg}")
                st.rerun()
            else:
                st.warning("Please paste an active, valid API key first.")

    with btn_c2:
        if st.button("🧪 Test Connection", use_container_width=True):
            test_target = raw_input_key.strip() if is_valid_key_string(raw_input_key) else saved_key
            if is_valid_key_string(test_target):
                target_model = st.session_state.get(f"active_model_{current_provider}", cfg["default_model"])
                with st.spinner(f"Testing {current_provider} with model '{target_model}'..."):
                    ok, msg = test_api_key(current_provider, test_target, target_model)
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
            else:
                st.warning("Please paste your API key in the field before testing.")

    with btn_c3:
        if st.button("🗑️ Clear Field", use_container_width=True):
            st.session_state["user_pasted_api_key"] = ""
            st.session_state.pop(f"custom_key_{current_provider}", None)
            st.info("Input field cleared.")
            st.rerun()

    # Dynamic Model Selection for detected / active provider
    st.markdown("---")
    st.markdown(f"#### 🤖 {current_provider} Model Selection")
    active_test_key = raw_input_key.strip() if is_valid_key_string(raw_input_key) else saved_key
    provider_models = get_available_models_for_provider(current_provider, active_test_key)
    model_session_key = f"active_model_{current_provider}"
    cur_p_model = st.session_state.get(model_session_key, cfg["default_model"])
    model_idx = provider_models.index(cur_p_model) if cur_p_model in provider_models else 0

    chosen_model = st.selectbox(
        f"Available {current_provider} Models:",
        options=provider_models,
        index=model_idx,
        help=f"These models run on {current_provider}.",
    )

    if chosen_model != cur_p_model:
        st.session_state[model_session_key] = chosen_model
        st.success(f"Model updated to `{chosen_model}`")
        st.rerun()

    # Direct signup link and explanation
    st.markdown(f"""
    <div class="guide-box">
        <strong>About {current_provider}:</strong><br>
        {cfg['desc']}<br>
        👉 Get your key here: <a href="{cfg['signup_url']}" target="_blank">{cfg['signup_url']}</a><br>
        <small>Key format: <code>{cfg['key_prefix']}...</code></small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with col_overview:
    # ── Live Status Overview ──────────────────────────────────────────
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown("### 📡 Active Engine Status")

    active_provider = get_active_provider()
    active_model = get_active_model()
    active_key, active_source = get_api_key_for_provider(active_provider)

    if active_key:
        masked = f"...{active_key[-6:]}"
        st.success(f"🟢 **Active Provider:** `{active_provider}`")
        st.write(f"• **Model:** `{active_model}`")
        st.write(f"• **Key Source:** `{active_source}`")
        st.write(f"• **Key Preview:** `{masked}`")
    else:
        st.error(f"🔴 **Active Provider:** `{active_provider}` (No Active Key)")
        st.write(f"Paste your {active_provider} key on the left to activate it.")

    st.markdown("---")
    st.markdown("#### 🔍 Provider & Key Format Guide")
    st.markdown("""
    | Provider | Prefix | Official Developer Portal |
    |---|---|---|
    | **Groq** | `gsk_...` | [console.groq.com](https://console.groq.com/keys) *(Fast & Free)* |
    | **xAI (Grok)** | `xai-...` | [console.x.ai](https://console.x.ai/) *(Elon Musk / xAI)* |
    | **Google Gemini** | `AIzaSy...` | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
    | **OpenAI** | `sk-...` | [platform.openai.com](https://platform.openai.com/api-keys) |
    """)

    st.markdown("---")
    st.markdown("#### ☁️ Streamlit Cloud Secrets (Repo Owner)")
    st.markdown("""
    To set default keys on **Streamlit Cloud**, add any of these to your app secrets:
    ```toml
    GROQ_API_KEY = "gsk_..."
    XAI_API_KEY = "xai-..."
    GEMINI_API_KEY = "AIzaSy..."
    OPENAI_API_KEY = "sk-..."
    ```
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("AI-Student Assistant v2.0 · Universal Auto-Detect Multi-Provider")