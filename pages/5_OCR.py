"""
AI-Student Assistant — OCR Note Reader
"""

import streamlit as st
from utils.ocr import extract_text_from_image
from utils.ai_engine import ask_ai

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
    <h1>🖼️ OCR Note Reader</h1>
    <p>Convert photos of textbook pages, handwritten study notes, or whiteboard sketches into editable text.</p>
</div>
""", unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "Upload note photo or scan (PNG, JPG, JPEG):",
    type=["png", "jpg", "jpeg"],
)

if uploaded_image:
    col_img, col_txt = st.columns([1, 1])

    with col_img:
        st.markdown("#### 📷 Uploaded Note Preview")
        st.image(uploaded_image, use_container_width=True)

    image_id = f"{uploaded_image.name}-{uploaded_image.size}"
    if st.session_state.get("ocr_id") != image_id:
        with st.spinner("Extracting text from image..."):
            st.session_state.ocr_text = extract_text_from_image(uploaded_image)
        st.session_state.ocr_id = image_id

    extracted_text = st.session_state.ocr_text

    with col_txt:
        st.markdown("#### 📄 Extracted Text Content")
        if extracted_text.startswith("Error:"):
            st.warning(f"⚠️ {extracted_text}")
            st.info(
                "💡 **Cloud Deployment Note:** Image OCR uses EasyOCR/PyTorch (~1.5GB). "
                "On lightweight cloud deployments like Streamlit Community Cloud, OCR is optional "
                "to preserve container memory. All other modules (PDF Assistant RAG, AI Tutor, Summarizer, Quiz) "
                "run with full speed!"
            )
        else:
            st.text_area("Extracted Characters", extracted_text, height=320)

            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("📝 Summarize This", use_container_width=True):
                    with st.spinner("Summarizing extracted text..."):
                        p = f"Summarize these extracted study notes simply and clearly:\n\n{extracted_text}"
                        st.session_state.ocr_summary = ask_ai(p)

            with act_col2:
                if st.button("❓ Quiz From This", use_container_width=True):
                    with st.spinner("Creating practice quiz..."):
                        p = f"Create 5 multiple choice questions with answers from this text:\n\n{extracted_text}"
                        st.session_state.ocr_quiz = ask_ai(p)

    if "ocr_summary" in st.session_state:
        st.markdown(f'<div class="content-card"><h4>📝 Note Summary</h4>{st.session_state.ocr_summary}</div>', unsafe_allow_html=True)

    if "ocr_quiz" in st.session_state:
        st.markdown(f'<div class="content-card"><h4>❓ Practice Quiz</h4>{st.session_state.ocr_quiz}</div>', unsafe_allow_html=True)
else:
    st.info("👆 Upload an image of notes to begin text extraction.")