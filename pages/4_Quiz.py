"""
AI-Student Assistant — Quiz Generator Page
"""

import streamlit as st
from utils.ai_engine import ask_ai

# ── Page Config ──────────────────────────────
st.set_page_config(page_title="Quiz Generator", page_icon="❓", layout="wide")

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
st.title("❓ AI Quiz Generator")
st.write("Generate AI-based MCQs from your study material.")
st.divider()

content = st.text_area(
    "📚 Enter Topic or Notes",
    height=250,
    placeholder="Example: Explain Neural Networks...",
)

difficulty = st.selectbox("🎯 Select Difficulty", ["Easy", "Medium", "Hard"])
number = st.slider("Number of Questions", 1, 10, 5)

if st.button("🚀 Generate Quiz"):
    if content:
        with st.spinner("🤖 Creating Quiz..."):
            prompt = (
                f"You are an expert teacher.\n\n"
                f"Create exactly {number} {difficulty} level MCQs from the following notes.\n\n"
                "Rules:\n"
                "- Every question must have 4 options (A, B, C, D).\n"
                "- Only one correct answer.\n"
                "- Questions must be based only on the notes.\n"
                "- Do not repeat questions.\n"
                "- Return only the quiz.\n\n"
                f"Notes:\n{content}"
            )
            quiz = ask_ai(prompt)

        st.success("✅ Quiz Generated Successfully!")
        st.markdown(quiz)
    else:
        st.warning("⚠ Please enter notes/topic first.")

st.divider()
st.info(
    "🚀 **Features:** AI MCQ Generation • Automatic Answers • "
    "Difficulty Selection • Groq AI Powered"
)