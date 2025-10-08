import streamlit as st

st.set_page_config(
    page_title="Meeting Notes Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        height: 100%;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .stats-container {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .sample-container {
        background: #fef3c7;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #f59e0b;
    }
    .nav-hint {
        background: #dbeafe;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem;">📝 Meeting Notes Summarizer</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Transform your meetings into actionable insights</p>
</div>
""", unsafe_allow_html=True)

# Navigation hint
st.markdown("""
<div class="nav-hint">
    <strong>🚀 Get Started:</strong> Use the sidebar to navigate between pages - <strong>Summarizer</strong> for analysis, <strong>Text to Speech</strong> for audio conversion, and <strong>About</strong> for more info.
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("## ✨ Key Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎤</div>
        <h3>Audio Transcription</h3>
        <p>Upload audio files and get accurate transcriptions with progress tracking</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Smart Summaries</h3>
        <p>AI-powered meeting summaries with bullet points and key insights</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✅</div>
        <h3>Action Items</h3>
        <p>Automatically extract tasks, owners, and deadlines from meetings</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗣️</div>
        <h3>Text to Speech</h3>
        <p>Convert text documents to audio files with high-quality TTS</p>
    </div>
    """, unsafe_allow_html=True)

# Sample section
st.markdown("## 🧪 Try a Sample")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="sample-container">
        <h4>📄 Sample Transcript</h4>
        <p>Click the button to load a sample meeting transcript and see how the tool works.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("🔄 Load Sample", type="primary", use_container_width=True):
        try:
            with open("sample_transcript.txt", "r") as f:
                sample = f.read()
            st.code(sample, language="text")
        except Exception:
            st.error("No sample_transcript.txt found in the project root.")

# Stats section
st.markdown("## 📈 How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stats-container">
        <h4>1️⃣ Input</h4>
        <p>Upload audio files or paste meeting transcripts</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-container">
        <h4>2️⃣ Process</h4>
        <p>AI analyzes content and extracts key information</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-container">
        <h4>3️⃣ Output</h4>
        <p>Get summaries and action items in multiple formats</p>
    </div>
    """, unsafe_allow_html=True)
