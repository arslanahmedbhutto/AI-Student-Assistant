"""
AI-Student Assistant — Quiz Generator
"""

import streamlit as st
from utils.ai_engine import ask_ai

st.set_page_config(
    page_title="Quiz Generator — AI-Student Assistant",
    page_icon="❓",
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
.quiz-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 28px;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    line-height: 1.7;
}
.stButton button {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>❓ Interactive Quiz Generator</h1>
    <p>Test your knowledge with AI-generated multiple choice questions, answer keys, and explanations.</p>
</div>
""", unsafe_allow_html=True)

# State initialization
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = ""

col_text, col_opts = st.columns([3, 1])

with col_opts:
    difficulty = st.selectbox("🎯 Difficulty", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    include_exp = st.checkbox("Include Explanations", value=True)
    st.write("")
    if st.button("🗑️ Clear / Reset Quiz", use_container_width=True):
        st.session_state.quiz_topic = ""
        st.session_state.quiz_output = ""
        st.toast("Quiz generator cleared!", icon="🧹")
        st.rerun()

with col_text:
    topic_val = st.text_area(
        "Enter Syllabus Topic or Study Notes:",
        value=st.session_state.quiz_topic,
        height=260,
        placeholder="e.g. Newton's Laws of Motion, Cellular Respiration, Operating Systems Memory Management...",
    )
    st.session_state.quiz_topic = topic_val

if st.button("🚀 Generate Practice Quiz", use_container_width=True):
    if st.session_state.quiz_topic.strip():
        with st.spinner("Generating custom test questions..."):
            prompt = (
                f"You are an expert academic examiner.\n"
                f"Generate exactly {num_questions} {difficulty}-level Multiple Choice Questions (MCQs) "
                f"based on the study material below.\n\n"
                f"Rules:\n"
                f"- Format each question clearly with Options A, B, C, D.\n"
                f"- Include the Correct Answer clearly identified.\n"
                f"- {'Provide a brief explanation for the correct answer.' if include_exp else 'Do not include explanation.'}\n\n"
                f"Material:\n{st.session_state.quiz_topic}"
            )
            st.session_state.quiz_output = ask_ai(prompt)
        st.rerun()
    else:
        st.warning("Please enter a topic or study notes first.")

# Persisted quiz card
if st.session_state.quiz_output:
    st.markdown("### 📋 Generated Quiz")
    st.markdown(f'<div class="quiz-card">{st.session_state.quiz_output}</div>', unsafe_allow_html=True)

    st.download_button(
        "📥 Download Quiz (.txt)",
        data=st.session_state.quiz_output,
        file_name="practice_quiz.txt",
        mime="text/plain",
    )