"""
AI-Student Assistant — OCR Note Reader
Supports Smart AI Vision OCR and Local Offline EasyOCR.
"""

import importlib
import streamlit as st
import utils.ocr as ocr_utils

# Hot-reload utils.ocr to ensure newly installed packages and functions are loaded
importlib.reload(ocr_utils)
extract_text_from_image = getattr(ocr_utils, "extract_text_from_image")
is_easyocr_available = getattr(ocr_utils, "is_easyocr_available", lambda: False)

from utils.ai_engine import ask_ai, get_active_provider, get_active_api_key_info

st.set_page_config(
    page_title="OCR Reader — AI-Student Assistant",
    page_icon="🖼️",
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
.content-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    margin-top: 15px;
    line-height: 1.7;
}
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25) !important;
}
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    color: #4338CA;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>🖼️ OCR Note Reader</h1>
    <p>Convert photos of textbook pages, handwritten study notes, flowchart diagrams, or whiteboard sketches into structured text.</p>
</div>
""", unsafe_allow_html=True)

# Provider info
active_key, active_source, active_provider = get_active_api_key_info()
easy_avail = is_easyocr_available()

# Control Bar
col_settings_l, col_settings_m, col_settings_r = st.columns([2, 1.5, 1])

with col_settings_l:
    ocr_engine = st.selectbox(
        "⚙️ Extraction Engine:",
        options=[
            "Auto (AI Vision with EasyOCR Fallback)",
            "AI Vision OCR (Best for Diagrams, Flowcharts & Handwriting)",
            "Local EasyOCR (Offline)",
        ],
        index=0,
        help="AI Vision uses your active LLM to recognize complex layouts, diagrams, and handwriting.",
    )

with col_settings_m:
    ocr_lang = st.selectbox("🌍 Target Language:", ["English", "Urdu", "Sindhi"], index=0)

with col_settings_r:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear / Refresh", use_container_width=True):
        st.session_state.pop("ocr_text", None)
        st.session_state.pop("ocr_id", None)
        st.session_state.pop("ocr_summary", None)
        st.session_state.pop("ocr_quiz", None)
        st.toast("OCR reader refreshed!", icon="🧹")
        st.rerun()

st.divider()

uploaded_image = st.file_uploader(
    "Upload note photo, scan, or diagram (PNG, JPG, JPEG):",
    type=["png", "jpg", "jpeg"],
    key="ocr_file_uploader",
)

if uploaded_image:
    col_img, col_txt = st.columns([1, 1])

    with col_img:
        st.markdown("#### 📷 Uploaded Image Preview")
        st.image(uploaded_image, use_container_width=True)

    image_id = f"{uploaded_image.name}-{uploaded_image.size}-{ocr_engine}"
    if st.session_state.get("ocr_id") != image_id:
        engine_mode = "auto"
        if "AI Vision" in ocr_engine:
            engine_mode = "ai_vision"
        elif "EasyOCR" in ocr_engine:
            engine_mode = "easyocr"

        with st.spinner("Analyzing image and extracting text..."):
            st.session_state.ocr_text = extract_text_from_image(
                uploaded_image, mode=engine_mode, language=ocr_lang
            )
        st.session_state.ocr_id = image_id

    extracted_text = st.session_state.get("ocr_text", "")

    with col_txt:
        st.markdown("#### 📄 Extracted Content")
        if extracted_text.startswith("Error:"):
            st.error(f"❌ {extracted_text}")
            if not easy_avail:
                st.info(
                    "💡 **Quick Fix:** Switch to **'AI Vision OCR'** in the dropdown above. "
                    "AI Vision connects directly to your active API key and reads diagrams and handwriting with high accuracy!"
                )
        else:
            st.text_area("Extracted Characters & Markdown", extracted_text, height=320)

            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("📝 Summarize Notes", use_container_width=True):
                    with st.spinner("Summarizing extracted text..."):
                        p = f"Summarize these extracted study notes simply and clearly in {ocr_lang}:\n\n{extracted_text}"
                        st.session_state.ocr_summary = ask_ai(p, language=ocr_lang)

            with act_col2:
                if st.button("❓ Quiz From This", use_container_width=True):
                    with st.spinner("Creating practice quiz..."):
                        p = f"Create 5 multiple choice questions with answers from this text in {ocr_lang}:\n\n{extracted_text}"
                        st.session_state.ocr_quiz = ask_ai(p, language=ocr_lang)

    if "ocr_summary" in st.session_state and st.session_state.ocr_summary:
        st.markdown(
            f'<div class="content-card"><h4>📝 Note Summary</h4>{st.session_state.ocr_summary}</div>',
            unsafe_allow_html=True,
        )

    if "ocr_quiz" in st.session_state and st.session_state.ocr_quiz:
        st.markdown(
            f'<div class="content-card"><h4>❓ Practice Quiz</h4>{st.session_state.ocr_quiz}</div>',
            unsafe_allow_html=True,
        )
else:
    # If previously extracted text is preserved in session state, keep it visible!
    if "ocr_text" in st.session_state and st.session_state.ocr_text:
        st.info("ℹ️ Showing previously extracted notes from this session. Upload a new image or click 'Clear / Refresh' above.")
        st.text_area("Extracted Notes", st.session_state.ocr_text, height=250)
    else:
        st.info("👆 Upload an image of textbook pages, handwritten notes, or diagrams to begin text extraction.")