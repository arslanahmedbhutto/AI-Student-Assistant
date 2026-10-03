"""
AI-Student Assistant — PDF Assistant Page

Features:
  - Upload PDF and extract text
  - AI Summary & Quiz generation
  - RAG-powered PDF Chat (answers from document only)
"""

import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.ai_engine import ask_ai
from rag.rag_engine import RAGEngine

# Max characters of PDF text sent to the LLM for summary / quiz
MAX_CONTEXT_CHARS = 12000

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="PDF Assistant", page_icon="📄", layout="wide")

# ── CSS ──────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
}
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-size: 15px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ── Title ────────────────────────────────────
st.title("📄 AI PDF Assistant")
st.markdown("Upload your study material and chat with your PDF using AI.")
st.divider()

# ── Upload PDF ───────────────────────────────
uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

# ── Process PDF ──────────────────────────────
if uploaded_file:
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"

    if st.session_state.get("pdf_id") != file_id:
        text = extract_text_from_pdf(uploaded_file)

        if not text.strip():
            st.error("❌ No text found in PDF. If this is a scanned document, try the OCR page.")
            st.stop()

        rag = RAGEngine()
        with st.spinner("🔄 Preparing AI Knowledge Base..."):
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

    st.success(f"✅ Knowledge Base Ready — {rag.get_total_chunks()} chunks indexed ({rag.get_backend()})")
    st.write("📄 **File:**", uploaded_file.name)
    st.write("📦 **Size:**", round(uploaded_file.size / 1024, 2), "KB")

    llm_text = text[:MAX_CONTEXT_CHARS]
    if len(text) > MAX_CONTEXT_CHARS:
        st.caption(
            f"ℹ️ Summary and quiz use the first {MAX_CONTEXT_CHARS:,} characters. "
            "PDF Chat searches the entire document."
        )

    # ── Tabs ─────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📖 Document", "📝 Summary", "❓ Quiz", "💬 PDF Chat"]
    )

    # ── TAB 1 — Document ─────────────────────
    with tab1:
        st.subheader("📄 PDF Content")
        st.text_area("Extracted Text", text, height=450)

    # ── TAB 2 — AI Summary ───────────────────
    with tab2:
        st.subheader("📝 AI Summary")
        if st.button("Generate Summary"):
            prompt = f"Summarize the following PDF in simple student-friendly language.\n\n{llm_text}"
            with st.spinner("📝 Generating Summary..."):
                st.session_state.pdf_summary = ask_ai(prompt)

        if "pdf_summary" in st.session_state:
            st.write(st.session_state.pdf_summary)
            st.download_button(
                "📥 Download Summary",
                data=st.session_state.pdf_summary,
                file_name="summary.txt",
                mime="text/plain",
            )

    # ── TAB 3 — AI Quiz ──────────────────────
    with tab3:
        st.subheader("❓ AI Quiz Generator")
        if st.button("Generate Quiz"):
            prompt = (
                "Generate 10 Multiple Choice Questions from the given context.\n\n"
                "Each question must include:\n"
                "Question:\nA.\nB.\nC.\nD.\n\n"
                "Correct Answer:\nExplanation:\n\n"
                f"Context:\n{llm_text}"
            )
            with st.spinner("❓ Generating Quiz..."):
                st.session_state.pdf_quiz = ask_ai(prompt)

        if "pdf_quiz" in st.session_state:
            st.write(st.session_state.pdf_quiz)
            st.download_button(
                "📥 Download Quiz",
                data=st.session_state.pdf_quiz,
                file_name="quiz.txt",
                mime="text/plain",
            )

    # ── TAB 4 — RAG PDF Chat ─────────────────
    with tab4:
        st.subheader("💬 Chat with your PDF (RAG)")
        question = st.text_input(
            "Ask anything from this PDF",
            placeholder="Example: What is Machine Learning?",
        )

        if st.button("🚀 Ask AI"):
            if question.strip():
                with st.spinner("Searching relevant information..."):
                    chunks = rag.search(question)
                    context = "\n\n".join(chunks)

                    prompt = (
                        "You are AI-Student Assistant.\n\n"
                        "Answer ONLY from the context below.\n"
                        "If the answer is not available in the context, say:\n"
                        '"I could not find this information in the uploaded PDF."\n\n'
                        f"Context:\n{context}\n\nQuestion:\n{question}"
                    )

                with st.spinner("🤖 Finding Answer..."):
                    answer = ask_ai(prompt)

                st.write(answer)

                with st.expander("📚 View Retrieved PDF Chunks"):
                    for i, chunk in enumerate(chunks, start=1):
                        st.markdown(f"**Chunk {i}**")
                        st.write(chunk)
            else:
                st.warning("Please enter a question.")
