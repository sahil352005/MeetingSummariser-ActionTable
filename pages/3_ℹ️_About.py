import streamlit as st

# Custom CSS for modern styling
st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .tech-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .setup-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .feature-list {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .tech-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <h1 style="margin: 0; font-size: 2.5rem;">ℹ️ About</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Learn more about this powerful meeting analysis tool</p>
</div>
""", unsafe_allow_html=True)

# Overview section
st.markdown("## 🎯 Overview")
st.markdown("""
<div class="info-card">
    <h3>📝 Meeting Notes Summarizer & Action Item Extractor</h3>
    <p>This application transforms your meeting recordings and transcripts into actionable insights. Whether you have audio files or text transcripts, our tool can generate concise summaries and extract structured action items with assigned owners and deadlines.</p>
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-list">
        <h4>🎤 Audio Processing</h4>
        <ul>
            <li>Multi-format audio support (MP3, WAV, M4A, OGG, FLAC)</li>
            <li>Chunked transcription for long recordings</li>
            <li>Progress tracking during processing</li>
            <li>High-quality speech recognition</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-list">
        <h4>📊 Smart Analysis</h4>
        <ul>
            <li>AI-powered meeting summaries</li>
            <li>Automatic action item extraction</li>
            <li>Owner and deadline identification</li>
            <li>Multiple export formats (CSV, JSON)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Technologies section
st.markdown("## 🛠️ Technologies Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tech-card">
        <h4><span class="tech-icon">🤖</span>AI & NLP</h4>
        <ul>
            <li><strong>Mistral LLM API</strong> - High-quality summaries and structured extraction</li>
            <li><strong>spaCy</strong> - Rule-based fallback for offline processing</li>
            <li><strong>SpeechRecognition</strong> - Audio transcription engine</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tech-card">
        <h4><span class="tech-icon">💻</span>Framework & Tools</h4>
        <ul>
            <li><strong>Streamlit</strong> - Modern web interface</li>
            <li><strong>pydub</strong> - Audio processing and format conversion</li>
            <li><strong>pyttsx3</strong> - Text-to-speech synthesis</li>
            <li><strong>pandas</strong> - Data manipulation and export</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Setup section
st.markdown("## ⚙️ Setup & Configuration")

st.markdown("""
<div class="setup-card">
    <h4>🚀 Getting Started</h4>
    <ol>
        <li><strong>Install Dependencies:</strong> <code>pip install -r requirements.txt</code></li>
        <li><strong>Download spaCy Model:</strong> <code>python -m spacy download en_core_web_sm</code></li>
        <li><strong>Run the Application:</strong> <code>streamlit run streamlit_app.py</code></li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Optional setup
st.markdown("### 🔧 Optional Enhancements")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🤖 Mistral API Setup</h4>
        <p>For enhanced AI capabilities, set these environment variables:</p>
        <ul>
            <li><code>MISTRAL_API_URL</code> - Your Mistral endpoint</li>
            <li><code>MISTRAL_API_KEY</code> - Your API key</li>
        </ul>
        <p><em>Without these, the app falls back to rule-based extraction.</em></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🎵 Audio Requirements</h4>
        <p>For MP3 export in Text-to-Speech:</p>
        <ul>
            <li>Install <strong>ffmpeg</strong> on your system</li>
            <li>Ensure <strong>pydub</strong> can access it</li>
        </ul>
        <p><em>WAV format works without additional setup.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Usage tips
st.markdown("## 💡 Usage Tips")

st.markdown("""
<div class="info-card">
    <h4>📋 Best Practices</h4>
    <ul>
        <li><strong>Audio Quality:</strong> Clear recordings produce better transcriptions</li>
        <li><strong>Text Format:</strong> Use speaker labels (e.g., "John: ...") for better analysis</li>
        <li><strong>Long Files:</strong> The app automatically chunks long audio for processing</li>
        <li><strong>Export Options:</strong> Download results in CSV or JSON format for further use</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>Built with ❤️ using Streamlit • Meeting Notes Summarizer v1.0</p>
</div>
""", unsafe_allow_html=True)

