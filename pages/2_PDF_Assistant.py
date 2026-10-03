"""
AI-Student Assistant — PDF Assistant (RAG)
Supports interactive multi-turn Q&A chat, automatic summarization, and quiz generation.
"""

import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.ai_engine import ask_ai, get_active_provider
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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: #FAFAFC !important;
    color: #0F172A !important;
}
.page-header {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}
.page-header h1 {
    color: #0F172A !important;
    font-size: 30px !important;
    font-weight: 800 !important;
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
    font-size: 13.5px;
    line-height: 1.6;
}
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border: 1px solid #EAECEF !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02) !important;
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
    <p>Upload your textbook or study notes. Ask questions grounded in your document, generate summaries, and test yourself.</p>
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
            st.error("❌ No text could be extracted from this PDF. For scanned documents or image slides, try the OCR Assistant.")
            st.stop()

        rag = RAGEngine()
        with st.spinner("🔄 Building document vector index..."):
            try:
                rag.build_database(text)
            except Exception as e:
                st.error(f"❌ Could not build knowledge base: {e}")
                st.stop()

        st.session_state.pdf_id = file_id
        st.session_state.pdf_text = text
        st.session_state.rag = rag
        st.session_state.pdf_chat_history = []
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
            "RAG Search indexes the entire document."
        )

    st.write("")

    # ── Tabs ─────────────────────────────────
    tab_chat, tab_summary, tab_quiz, tab_doc = st.tabs(
        ["💬 Ask Questions (RAG Chat)", "📝 Generate Summary", "❓ Create Quiz", "📖 View Text"]
    )

    # ── TAB 1 — Multi-Turn RAG Chat ──────────
    with tab_chat:
        st.markdown("### 💬 Interactive Q&A (Grounded in PDF)")
        st.caption("Answers are derived exclusively from your document chunks. Previous questions are kept in session.")

        if "pdf_chat_history" not in st.session_state:
            st.session_state.pdf_chat_history = []

        q_ctrl1, q_ctrl2 = st.columns([4, 1])
        with q_ctrl2:
            if st.button("🗑️ Clear Q&A", use_container_width=True):
                st.session_state.pdf_chat_history = []
                st.toast("PDF Q&A thread cleared!", icon="🧹")
                st.rerun()

        # Render Q&A Chat Thread
        if st.session_state.pdf_chat_history:
            for item in st.session_state.pdf_chat_history:
                with st.chat_message("user", avatar="🧑‍🎓"):
                    st.markdown(item["question"])
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(item["answer"])
                    if item.get("chunks"):
                        with st.expander("🔍 View Retrieved Sources"):
                            for i, chk in enumerate(item["chunks"], 1):
                                st.markdown(f"**Source Passage #{i}:**")
                                st.markdown(f'<div class="chunk-box">{chk}</div>', unsafe_allow_html=True)
            st.divider()

        # Question input form
        with st.form("pdf_qa_form", clear_on_submit=True):
            user_q = st.text_input(
                "Ask a question from this document:",
                placeholder="e.g., What are the key formulas or findings in this chapter?",
            )
            submit_q = st.form_submit_button("🔍 Search & Answer", use_container_width=True)

        if submit_q and user_q.strip():
            with st.spinner("Retrieving relevant passages and formulating answer..."):
                chunks = rag.search(user_q, k=3)
                context = "\n\n".join(chunks)

                prompt = (
                    "You are AI-Student Assistant.\n\n"
                    "Answer the student's question ONLY using the context provided below.\n"
                    "If the answer is not contained in the context, explicitly say:\n"
                    '"I could not find this information in the uploaded PDF."\n\n'
                    f"Context:\n{context}\n\n"
                    f"Question:\n{user_q}"
                )
                answer = ask_ai(prompt)

            st.session_state.pdf_chat_history.append({
                "question": user_q,
                "answer": answer,
                "chunks": chunks,
            })
            st.rerun()

    # ── TAB 2 — Summary ──────────────────────
    with tab_summary:
        st.markdown("### 📝 AI Document Summary")
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            gen_sum = st.button("Generate Summary Now")
        with col_s2:
            if "pdf_summary" in st.session_state:
                if st.button("🗑️ Clear Summary", use_container_width=True):
                    st.session_state.pop("pdf_summary", None)
                    st.toast("Summary cleared!", icon="🧹")
                    st.rerun()

        if gen_sum:
            prompt = (
                "Summarize the following document for a student. Include key topics, "
                "important definitions, and main conclusions in clear bullet points:\n\n"
                f"{llm_text}"
            )
            with st.spinner("Writing summary..."):
                st.session_state.pdf_summary = ask_ai(prompt)
            st.rerun()

        if "pdf_summary" in st.session_state and st.session_state.pdf_summary:
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
        col_q1, col_q2 = st.columns([3, 1])
        with col_q1:
            gen_qz = st.button("Generate 10 Practice Questions")
        with col_q2:
            if "pdf_quiz" in st.session_state:
                if st.button("🗑️ Clear Quiz", use_container_width=True):
                    st.session_state.pop("pdf_quiz", None)
                    st.toast("Quiz cleared!", icon="🧹")
                    st.rerun()

        if gen_qz:
            prompt = (
                "Create exactly 10 Multiple Choice Questions from the text below.\n"
                "Format each question cleanly with Options A, B, C, D, followed by Correct Answer and Explanation:\n\n"
                f"{llm_text}"
            )
            with st.spinner("Generating quiz questions..."):
                st.session_state.pdf_quiz = ask_ai(prompt)
            st.rerun()

        if "pdf_quiz" in st.session_state and st.session_state.pdf_quiz:
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
