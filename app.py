import streamlit as st

# ==============================
# PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="AI-Student Assistant",
    page_icon="🎓",
    layout="wide",
)

# ==============================
# CUSTOM CSS — Modern Glassmorphism
# ==============================
st.markdown("""
<style>
/* ---------- Main Background ---------- */
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 50%, #f0f4ff 100%);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e, #16213e, #0f3460);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #e0e0e0 !important;
}

/* ---------- Hero Section ---------- */
.hero {
    padding: 50px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 6s ease-in-out infinite;
}
@keyframes shimmer {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(30px, 30px); }
}
.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    position: relative;
}
.hero h3 {
    font-weight: 400;
    font-size: 20px;
    opacity: 0.9;
    position: relative;
}
.hero p {
    font-size: 16px;
    opacity: 0.85;
    position: relative;
}

/* ---------- Feature Cards ---------- */
.card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 28px 20px;
    height: 180px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(102, 126, 234, 0.2);
}
.card h2 { font-size: 36px; margin-bottom: 4px; }
.card h3 { color: #667eea; font-size: 18px; margin-bottom: 6px; }
.card p { color: #4a5568; font-size: 15px; line-height: 1.5; }

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.5);
}

/* ---------- Buttons ---------- */
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 28px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* ---------- About Section ---------- */
.about-box {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.5);
}
.about-box h2 { color: #667eea; }
.about-box p, .about-box li {
    color: #4a5568;
    font-size: 16px;
    line-height: 1.8;
}

/* ---------- Dark Mode ---------- */
@media (prefers-color-scheme: dark) {
    .stApp { background: linear-gradient(135deg, #0f172a, #1e293b); }
    .card, .about-box, [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.85);
        border-color: rgba(255,255,255,0.08);
    }
    .card h3 { color: #a5b4fc !important; }
    .card p, .about-box p, .about-box li { color: #cbd5e1 !important; }
    .about-box h2 { color: #a5b4fc !important; }
}
</style>
""", unsafe_allow_html=True)


# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("🎓 AI-Student Assistant")
st.sidebar.markdown("---")
st.sidebar.success("👋 Welcome Student!")
st.sidebar.markdown("Use the pages above to open each tool.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 Powered by Python + Streamlit + Groq AI")


# ==============================
# HERO BANNER
# ==============================
st.markdown("""
<div class="hero">
    <div class="hero-title">🎓 AI-Student Assistant</div>
    <h3>Your Personal AI Learning Companion</h3>
    <p>Learn smarter with AI-powered PDF analysis, summarization, quizzes and intelligent chat.</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# ==============================
# METRICS
# ==============================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📄 PDFs Uploaded", "0")
with c2:
    st.metric("📝 Summaries", "0")
with c3:
    st.metric("❓ Quizzes", "0")
with c4:
    st.metric("💬 AI Chats", "0")

st.divider()


# ==============================
# FEATURES
# ==============================
st.header("🚀 AI Features")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
        <h2>📄</h2>
        <h3>PDF Assistant</h3>
        <p>Upload PDFs and get AI explanations with RAG.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h2>📝</h2>
        <h3>Smart Summarizer</h3>
        <p>Convert long notes into clear, short summaries.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h2>❓</h2>
        <h3>Quiz Generator</h3>
        <p>Generate AI-based MCQs and quizzes instantly.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <div class="card">
        <h2>💬</h2>
        <h3>AI Chat</h3>
        <p>Ask questions and learn with AI assistance.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <h2>🖼️</h2>
        <h3>OCR Reader</h3>
        <p>Extract text from images and handwritten notes.</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card">
        <h2>🌍</h2>
        <h3>Multilingual</h3>
        <p>Supports English, Urdu and Sindhi responses.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==============================
# ABOUT PROJECT
# ==============================
st.markdown("""
<div class="about-box">
    <h2>📌 About This Project</h2>
    <p>AI-Student Assistant is a multimodal AI learning platform designed for students.</p>
    <p>It helps students:</p>
    <ul>
        <li>✔ Understand PDFs using AI-powered RAG</li>
        <li>✔ Summarize study notes instantly</li>
        <li>✔ Generate MCQs automatically</li>
        <li>✔ Extract text from images using OCR</li>
        <li>✔ Chat with an AI tutor</li>
        <li>✔ Learn efficiently with smart tools</li>
    </ul>
    <p>🚀 Built using Groq AI, RAG, FAISS, OCR and Streamlit.</p>
</div>
""", unsafe_allow_html=True)

st.divider()


# ==============================
# START BUTTON
# ==============================
if st.button("🚀 Start Learning"):
    st.balloons()
    st.success("AI Learning Journey Started! Use the sidebar to explore tools.")

st.caption("© 2026 AI-Student Assistant | AI Powered Learning Platform")