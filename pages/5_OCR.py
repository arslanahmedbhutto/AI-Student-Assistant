"""
AI-Student Assistant — OCR Page
"""

import streamlit as st
from utils.ocr import extract_text_from_image
from utils.ai_engine import ask_ai

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="OCR Assistant", page_icon="🖼️", layout="wide")

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
st.title("🖼️ AI OCR Assistant")
st.write("Extract text from handwritten notes or document images.")
st.divider()

uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, use_container_width=True)

    # Run OCR once per image
    image_id = f"{uploaded_image.name}-{uploaded_image.size}"

    if st.session_state.get("ocr_id") != image_id:
        with st.spinner("🔍 Reading text from image..."):
            st.session_state.ocr_text = extract_text_from_image(uploaded_image)
        st.session_state.ocr_id = image_id

    text = st.session_state.ocr_text

    if text.startswith("Error:"):
        st.warning(f"⚠️ {text}")
        st.info(
            "💡 **Cloud Note:** EasyOCR requires PyTorch (~1.5GB). On lightweight cloud deployments "
            "(like Streamlit Community Cloud), image OCR is optional to preserve memory. "
            "All other features (AI Chat, PDF Assistant RAG, Summarizer, Quiz) run with full speed!"
        )
    else:
        st.success("✅ Text Extracted Successfully")
        st.subheader("📄 Extracted Text")
        st.text_area("OCR Output", text, height=250)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📝 Generate Summary"):
                with st.spinner("Generating Summary..."):
                    prompt = f"Summarize these notes in simple student-friendly language.\n\n{text}"
                    summary = ask_ai(prompt)
                st.subheader("📚 Summary")
                st.write(summary)

        with col2:
            if st.button("❓ Generate Quiz"):
                with st.spinner("Generating Quiz..."):
                    prompt = (
                        "Create 5 multiple-choice questions from these notes.\n\n"
                        "Rules:\n"
                        "- Four options (A, B, C, D)\n"
                        "- Mention the correct answer.\n"
                        "- Return only the quiz.\n\n"
                        f"Notes:\n{text}"
                    )
                    quiz = ask_ai(prompt)
                st.subheader("📝 Quiz")
                st.markdown(quiz)