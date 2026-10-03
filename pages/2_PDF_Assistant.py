"""
AI-Student Assistant — PDF Assistant (RAG)
"""

import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.ai_engine import ask_ai
from rag.rag_engine import RAGEngine

MAX_CONTEXT_CHARS = 12000

# ── Page Config ──────────────────────────────
st.set_page_config(
    page_title="PDF Assistant — AI-Student Assistant",
    page_icon="📄",
    layout="wide",
)

# ── CSS (Light, Clean, High Contrast) ────────
st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}
.page-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}
.page-header h1 {
    color: #0F172A !important;
    font-size: 30px !important;
    font-weight: 700 !important;
    margin: 0 0 6px 0 !important;
}
.page-header p {
    color: #64748B !important;
    font-size: 15px !important;
    margin: 0 !important;
}
.chunk-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #4F46E5;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #334155;
    font-size: 14px;
    line-height: 1.6;
}
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>📄 Document Assistant (RAG)</h1>
    <p>Upload your textbook or study notes. Ask questions to get answers sourced directly from your document.</p>
</div>
""", unsafe_allow_html=True)

# ── Upload Box ───────────────────────────────
uploaded_file = st.file_uploader(
    "Choose a PDF file to analyze",
    type=["pdf"],
    help="Upload PDF course materials, slides, or chapters.",
)

if uploaded_file:
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"

    if st.session_state.get("pdf_id") != file_id:
        text = extract_text_from_pdf(uploaded_file)

        if not text.strip():
            st.error("❌ No text could be extracted from this PDF. For scanned documents, try the OCR Assistant.")
            st.stop()

        rag = RAGEngine()
        with st.spinner("🔄 Building document index..."):
            try:
                rag.build_database(text)
            except Exception as e:
                st.error(f"❌ Could not build knowledge base: {e}")
                st.stop()

        st.session_state.pdf_id = file_id
        st.session_state.pdf_text = text
        st.session_state.rag = rag
        st.session_state.pop("pdf_summary", None)
        st.session_state.pop("pdf_quiz", None)

    text = st.session_state.pdf_text
    rag = st.session_state.rag

    # Info summary bar
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info(f"📄 **File:** `{uploaded_file.name}`")
    with col_b:
        st.info(f"📦 **Size:** `{round(uploaded_file.size / 1024, 1)} KB`")
    with col_c:
        st.success(f"⚡ **Indexed:** `{rag.get_total_chunks()} chunks` ({rag.get_backend()})")

    llm_text = text[:MAX_CONTEXT_CHARS]
    if len(text) > MAX_CONTEXT_CHARS:
        st.caption(
            f"ℹ️ Summary & Quiz use the first {MAX_CONTEXT_CHARS:,} characters. "
            "RAG Search indexes the complete document."
        )

    st.write("")

    # ── Tabs ─────────────────────────────────
    tab_chat, tab_summary, tab_quiz, tab_doc = st.tabs(
        ["💬 Ask Questions (RAG)", "📝 Generate Summary", "❓ Create Quiz", "📖 View Text"]
    )

    # ── TAB 1 — RAG Chat ─────────────────────
    with tab_chat:
        st.markdown("### 💬 Ask Questions From This PDF")
        st.caption("Answers are derived exclusively from your uploaded text chunks.")

        question = st.text_input(
            "Enter your question:",
            placeholder="e.g., What are the key findings mentioned in Section 2?",
        )

        if st.button("🔍 Search & Answer", use_container_width=True):
            if question.strip():
                with st.spinner("Retrieving relevant passages and formulating answer..."):
                    chunks = rag.search(question, k=3)
                    context = "\n\n".join(chunks)

                    prompt = (
                        "You are AI-Student Assistant.\n\n"
                        "Answer the student's question ONLY using the context provided below.\n"
                        "If the answer is not contained in the context, explicitly say:\n"
                        '"I could not find this information in the uploaded PDF."\n\n'
                        f"Context:\n{context}\n\n"
                        f"Question:\n{question}"
                    )
                    answer = ask_ai(prompt)

                st.markdown("#### 💡 Answer")
                st.markdown(answer)

                st.write("")
                with st.expander("🔍 View Retrieved Document Chunks"):
                    for i, chunk in enumerate(chunks, start=1):
                        st.markdown(f"**Chunk #{i}**")
                        st.markdown(f'<div class="chunk-box">{chunk}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please type a question first.")

    # ── TAB 2 — Summary ──────────────────────
    with tab_summary:
        st.markdown("### 📝 AI Document Summary")
        if st.button("Generate Summary Now"):
            prompt = (
                "Summarize the following document for a student. Include key topics, "
                "important definitions, and main conclusions in clear bullet points:\n\n"
                f"{llm_text}"
            )
            with st.spinner("Writing summary..."):
                st.session_state.pdf_summary = ask_ai(prompt)

        if "pdf_summary" in st.session_state:
            st.markdown(st.session_state.pdf_summary)
            st.download_button(
                "📥 Download Summary (.txt)",
                data=st.session_state.pdf_summary,
                file_name=f"summary_{uploaded_file.name}.txt",
                mime="text/plain",
            )

    # ── TAB 3 — Quiz ─────────────────────────
    with tab_quiz:
        st.markdown("### ❓ Practice Quiz Generator")
        if st.button("Generate 10 Practice Questions"):
            prompt = (
                "Create exactly 10 Multiple Choice Questions from the text below.\n"
                "Format each question cleanly with Options A, B, C, D, followed by Correct Answer and Explanation:\n\n"
                f"{llm_text}"
            )
            with st.spinner("Generating quiz questions..."):
                st.session_state.pdf_quiz = ask_ai(prompt)

        if "pdf_quiz" in st.session_state:
            st.markdown(st.session_state.pdf_quiz)
            st.download_button(
                "📥 Download Quiz (.txt)",
                data=st.session_state.pdf_quiz,
                file_name=f"quiz_{uploaded_file.name}.txt",
                mime="text/plain",
            )

    # ── TAB 4 — Document Text ────────────────
    with tab_doc:
        st.markdown("### 📖 Extracted Plain Text")
        st.text_area("Document Contents", text, height=450)
else:
    st.info("👆 **Get started:** Upload any PDF document using the file box above.")
