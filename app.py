import streamlit as st
from utils.ai_engine import get_active_provider, get_active_model

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI-Student Assistant — Smart AI Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# MODERN SAAS WEBSITE STYLING (Light, Clean, High-Contrast)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #FAFAFC !important;
    color: #0F172A !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: rgba(250, 250, 252, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid #EAECEF !important;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #EAECEF !important;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.02) !important;
}
[data-testid="stSidebar"] * {
    color: #1E293B !important;
}
[data-testid="stSidebarNav"] span {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #334155 !important;
}
[data-testid="stSidebarNav"] li a {
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin: 2px 8px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebarNav"] li a:hover {
    background-color: #F1F5F9 !important;
    color: #4F46E5 !important;
}
[data-testid="stSidebarNav"] li[aria-selected="true"] a {
    background-color: #EEF2FF !important;
}
[data-testid="stSidebarNav"] li[aria-selected="true"] span {
    color: #4F46E5 !important;
    font-weight: 700 !important;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 4px 18px 4px;
    border-bottom: 1px solid #EAECEF;
    margin-bottom: 16px;
}
.sidebar-logo-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4F46E5, #6366F1);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
}
.sidebar-logo-text {
    font-size: 17px;
    font-weight: 800;
    color: #0F172A !important;
    line-height: 1.2;
}
.sidebar-logo-sub {
    font-size: 12px;
    color: #64748B !important;
    font-weight: 500;
}

.sidebar-status-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px;
    margin-top: 20px;
}
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    color: #059669 !important;
    background: #ECFDF5;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: #10B981;
}

.hero-wrapper {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #EAECEF;
    border-radius: 24px;
    padding: 56px 40px 48px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05);
    margin-bottom: 36px;
}
.hero-wrapper::before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 180px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(255,255,255,0) 70%);
    pointer-events: none;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    color: #4338CA !important;
    font-size: 13px;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 50px;
    margin-bottom: 18px;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.08);
}
.hero-title {
    font-size: 46px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0 0 16px 0 !important;
}
.hero-title span {
    background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 18px !important;
    color: #475569 !important;
    max-width: 680px;
    margin: 0 auto 28px auto !important;
    line-height: 1.6;
    font-weight: 400;
}
.hero-tags {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}
.hero-tag {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 600;
    color: #334155 !important;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    transition: transform 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.04);
}
.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}
.stat-content h4 {
    margin: 0 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px;
}
.stat-content p {
    margin: 2px 0 0 0 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #64748B !important;
}

.section-heading {
    text-align: center;
    margin: 40px 0 28px 0;
}
.section-heading h2 {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px;
    margin: 0 0 8px 0 !important;
}
.section-heading p {
    font-size: 16px !important;
    color: #64748B !important;
    margin: 0 !important;
}

.feature-box {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 18px;
    padding: 30px 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-sizing: border-box;
}
.feature-box:hover {
    transform: translateY(-4px);
    border-color: #C7D2FE;
    box-shadow: 0 16px 32px rgba(79, 70, 229, 0.08);
}
.feature-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}
.feature-badge-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}
.feature-tag-chip {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    padding: 4px 10px;
    border-radius: 20px;
}
.feature-box h3 {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin: 0 0 10px 0 !important;
}
.feature-box p {
    font-size: 14.5px !important;
    color: #475569 !important;
    line-height: 1.6 !important;
    margin: 0 0 20px 0 !important;
}
.feature-footer-link {
    font-size: 13.5px;
    font-weight: 700;
    color: #4F46E5 !important;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.workflow-card {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 18px;
    padding: 36px 32px;
    margin-top: 40px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}
.workflow-card h3 {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin: 0 0 6px 0 !important;
}
.workflow-card p.subtitle {
    color: #64748B !important;
    font-size: 15px !important;
    margin: 0 0 28px 0 !important;
}
.step-item {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px;
    text-align: left;
    height: 100%;
}
.step-num {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #4F46E5;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
}
.step-item h4 {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin: 0 0 6px 0 !important;
}
.step-item p {
    font-size: 13.5px !important;
    color: #475569 !important;
    line-height: 1.55 !important;
    margin: 0 !important;
}

.cta-box {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
    border-radius: 20px;
    padding: 40px 32px;
    text-align: center;
    color: #FFFFFF !important;
    margin: 36px 0 20px 0;
    box-shadow: 0 16px 36px rgba(49, 46, 129, 0.25);
}
.cta-box h3 {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0 0 10px 0 !important;
}
.cta-box p {
    color: #C7D2FE !important;
    font-size: 16px !important;
    max-width: 580px;
    margin: 0 auto 20px auto !important;
}
.stButton button {
    background: #FFFFFF !important;
    color: #312E81 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    background: #EEF2FF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# Dynamic Provider & Model info
cur_provider = get_active_provider()
cur_model = get_active_model()

# ==========================================
# SIDEBAR NAVIGATION & SYSTEM STATUS
# ==========================================
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="sidebar-logo-icon">🎓</div>
    <div>
        <div class="sidebar-logo-text">AI-Student</div>
        <div class="sidebar-logo-sub">Smart Study Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="sidebar-status-box">
    <div class="status-indicator">
        <span class="status-dot"></span> System Operational
    </div>
    <div style="font-size: 12px; color: #475569; line-height: 1.6;">
        • <strong>Provider:</strong> {cur_provider}<br>
        • <strong>Model:</strong> {cur_model}<br>
        • <strong>Vector DB:</strong> FAISS Index<br>
        • <strong>Deployment:</strong> Streamlit Cloud Ready
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 AI-Student Assistant · Capstone Project")


# ==========================================
# HERO SECTION (MODERN SAAS LANDING VIEW)
# ==========================================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-pill">
        <span>✨</span> Next-Gen AI Learning Workspace
    </div>
    <h1 class="hero-title">
        Master Your Studies with <span>AI Intelligence</span>
    </h1>
    <p class="hero-subtitle">
        Upload course textbooks, chat with grounded PDF documents, generate exam-ready 
        MCQs, and extract handwritten notes — supporting Groq, Google Gemini, OpenAI, and xAI Grok.
    </p>
    <div class="hero-tags">
        <span class="hero-tag">⚡ Multi-LLM Engine</span>
        <span class="hero-tag">📄 Zero-Hallucination RAG</span>
        <span class="hero-tag">🌍 English · Urdu · Sindhi</span>
        <span class="hero-tag">🔒 100% Private Processing</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# STATS ROW
# ==========================================
stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon" style="background: #EEF2FF; color: #4F46E5;">📄</div>
        <div class="stat-content">
            <h4>PDF RAG</h4>
            <p>Document Search</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with stat2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background: #ECFDF5; color: #059669;">🤖</div>
        <div class="stat-content">
            <h4>{cur_provider}</h4>
            <p>Active Engine</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with stat3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon" style="background: #FEF3C7; color: #D97706;">❓</div>
        <div class="stat-content">
            <h4>Custom MCQs</h4>
            <p>Active Recall</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with stat4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon" style="background: #F3E8FF; color: #7C3AED;">🌐</div>
        <div class="stat-content">
            <h4>3 Languages</h4>
            <p>Multilingual Tutor</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# CORE FEATURE MODULES (BENTO-STYLE GRID)
# ==========================================
st.markdown("""
<div class="section-heading">
    <h2>Explore AI Study Modules</h2>
    <p>Everything you need to study faster, test your understanding, and ace exams.</p>
</div>
""", unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #EEF2FF; color: #4F46E5;">📄</div>
                <span class="feature-tag-chip" style="background: #EEF2FF; color: #4F46E5;">RAG Engine</span>
            </div>
            <h3>PDF Assistant</h3>
            <p>Upload lecture slides, papers, or books. Ask questions to get answers verified against your exact PDF pages.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #F0FDF4; color: #16A34A;">💬</div>
                <span class="feature-tag-chip" style="background: #F0FDF4; color: #16A34A;">Conversational</span>
            </div>
            <h3>AI Tutor Chat</h3>
            <p>A round-the-clock personal tutor. Clarify confusing homework problems, theory, or formulas with step-by-step logic.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)

with row1_col3:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #FFFBEB; color: #D97706;">📝</div>
                <span class="feature-tag-chip" style="background: #FFFBEB; color: #D97706;">High Yield</span>
            </div>
            <h3>Smart Summarizer</h3>
            <p>Paste paragraphs or textbook extracts to receive executive summaries, key concept breakdowns, and bullet lists.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #FEF2F2; color: #DC2626;">❓</div>
                <span class="feature-tag-chip" style="background: #FEF2F2; color: #DC2626;">Practice</span>
            </div>
            <h3>Quiz Generator</h3>
            <p>Create tailored 4-option multiple-choice quizzes with difficulty adjustment and instant answer keys for exam revision.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #F0F9FF; color: #0284C7;">🖼️</div>
                <span class="feature-tag-chip" style="background: #F0F9FF; color: #0284C7;">Vision OCR</span>
            </div>
            <h3>OCR Note Reader</h3>
            <p>Snap a photo of handwritten notes or whiteboard summaries to convert them into editable text ready for AI processing.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)

with row2_col3:
    st.markdown("""
    <div class="feature-box">
        <div>
            <div class="feature-header">
                <div class="feature-badge-icon" style="background: #FAF5FF; color: #9333EA;">📚</div>
                <span class="feature-tag-chip" style="background: #FAF5FF; color: #9333EA;">Timeline</span>
            </div>
            <h3>Session History</h3>
            <p>Access your past question threads, generated summaries, and practice quizzes anytime during your active study session.</p>
        </div>
        <div class="feature-footer-link">Open in Sidebar →</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HOW IT WORKS (3-STEP WORKFLOW)
# ==========================================
st.markdown("""
<div class="workflow-card">
    <h3>🔄 How the Platform Works</h3>
    <p class="subtitle">Streamlined 3-step pipeline designed for distraction-free learning.</p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px;">
        <div class="step-item">
            <div class="step-num">1</div>
            <h4>Input Study Content</h4>
            <p>Upload a course syllabus PDF, paste topic notes, or take a picture of class whiteboard diagrams.</p>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <h4>Semantic Indexing</h4>
            <p>Content is parsed, split into 500-char chunks, and indexed into FAISS vector space for precision retrieval.</p>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <h4>Interact & Test</h4>
            <p>Ask questions with RAG, generate high-yield revision summaries, or test yourself with automated quizzes.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# CALL TO ACTION (CTA)
# ==========================================
st.markdown("""
<div class="cta-box">
    <h3>Ready to Elevate Your Learning?</h3>
    <p>Jump directly into the PDF Assistant or AI Tutor Chat using the sidebar menu.</p>
</div>
""", unsafe_allow_html=True)

col_cta_l, col_cta_m, col_cta_r = st.columns([1, 2, 1])
with col_cta_m:
    if st.button("🚀 Start Studying Now", use_container_width=True):
        st.balloons()
        st.success("Select '1_AI_Chat' or '2_PDF_Assistant' from the left sidebar to start!")