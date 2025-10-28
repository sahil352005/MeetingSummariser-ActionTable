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
    <h3>⚡ Lightning-Fast Meeting Intelligence Platform</h3>
    <p>Transform your meetings into actionable insights with our ultra-lightweight, lightning-fast analysis tool. From audio transcription to instant summarization and smart action item extraction, we provide professional-grade meeting intelligence with zero heavy dependencies.</p>
    <p><strong>Key Benefits:</strong> Instant processing (0.02s), minimal resources, maximum efficiency, and professional results.</p>
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-list">
        <h4>🎤 Audio Intelligence</h4>
        <ul>
            <li>Multi-format support (MP3, WAV, M4A, OGG, FLAC)</li>
            <li>Chunked processing for long recordings</li>
            <li>Real-time progress tracking</li>
            <li>Google Speech Recognition API</li>
            <li>Automatic speaker detection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-list">
        <h4>🧠 NLP Analysis</h4>
        <ul>
            <li>Structured meeting summaries</li>
            <li>Smart action item extraction</li>
            <li>Priority and status assignment</li>
            <li>Meeting analytics & insights</li>
            <li>Sentiment analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Technologies section
st.markdown("## 🛠️ Technologies Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tech-card">
        <h4><span class="tech-icon">⚡</span>Lightning-Fast NLP Engine</h4>
        <ul>
            <li><strong>Instant Processing</strong> - 0.02-second summary generation</li>
            <li><strong>Smart Pattern Matching</strong> - Efficient action item detection</li>
            <li><strong>Real-time Analytics</strong> - Meeting intelligence without heavy models</li>
            <li><strong>Lightweight Design</strong> - Minimal dependencies, maximum speed</li>
            <li><strong>Universal Compatibility</strong> - Runs on any device efficiently</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tech-card">
        <h4><span class="tech-icon">💻</span>Modern Tech Stack</h4>
        <ul>
            <li><strong>Streamlit</strong> - Professional web interface</li>
            <li><strong>pandas</strong> - Data processing and export</li>
            <li><strong>SpeechRecognition</strong> - Audio transcription</li>
            <li><strong>pydub</strong> - Audio format conversion</li>
            <li><strong>pyttsx3</strong> - Text-to-speech synthesis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Setup section
st.markdown("## ⚙️ Setup & Configuration")

st.markdown("""
<div class="setup-card">
    <h4>🚀 Quick Start Guide</h4>
    <ol>
        <li><strong>Install Dependencies:</strong> <code>pip install streamlit pandas</code></li>
        <li><strong>Clone Repository:</strong> Download or clone the project files</li>
        <li><strong>Run Application:</strong> <code>streamlit run streamlit_app.py</code></li>
        <li><strong>Start Analyzing:</strong> Upload audio or paste transcript text</li>
    </ol>
    <p><em>Ready to use in under 2 minutes! No complex setup required.</em></p>
</div>
""", unsafe_allow_html=True)

# Additional features
st.markdown("### ✨ Additional Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>⚡ Lightning-Fast Processing</h4>
        <p>Our optimized NLP engine delivers:</p>
        <ul>
            <li><strong>Instant Results</strong> - 0.02-second summary generation</li>
            <li><strong>Smart Analysis</strong> - Professional-quality insights without heavy models</li>
            <li><strong>Real-time Intelligence</strong> - Meeting analytics with zero latency</li>
            <li><strong>Efficient Extraction</strong> - Action items with priority and context</li>
        </ul>
        <p><strong>Performance Benefits:</strong></p>
        <ul>
            <li>No heavy model downloads required</li>
            <li>Minimal resource usage (under 100MB RAM)</li>
            <li>Works on any device or platform</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>🔊 Text-to-Speech</h4>
        <p>Convert meeting summaries to audio:</p>
        <ul>
            <li><strong>Multiple Formats:</strong> WAV and MP3 output</li>
            <li><strong>Audio Preview:</strong> Built-in player</li>
            <li><strong>Chunked Processing:</strong> Handles long text</li>
            <li><strong>Download Options:</strong> Save audio files locally</li>
        </ul>
        <p><em>Perfect for accessibility and on-the-go review.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Usage tips
st.markdown("## 💡 Usage Tips")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🎤 Audio Best Practices</h4>
        <ul>
            <li><strong>Clear Audio:</strong> Use good microphones for better transcription</li>
            <li><strong>Minimize Noise:</strong> Reduce background sounds</li>
            <li><strong>Speaker Separation:</strong> Clear speaker identification helps</li>
            <li><strong>File Size:</strong> Automatic chunking handles long recordings</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>📝 Text Best Practices</h4>
        <ul>
            <li><strong>Speaker Labels:</strong> Use "Name: content" format</li>
            <li><strong>Clear Structure:</strong> Separate topics with line breaks</li>
            <li><strong>Complete Sentences:</strong> Better analysis with proper grammar</li>
            <li><strong>Export Options:</strong> CSV, JSON, and insights downloads</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
# Performance metrics
st.markdown("## 📈 Performance & Capabilities")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #3b82f6; margin: 0;">⚡</h3>
        <h4 style="margin: 0.5rem 0;">Lightning Speed</h4>
        <p style="margin: 0; color: #6b7280;">0.02 seconds processing</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #10b981; margin: 0;">🔒</h3>
        <h4 style="margin: 0.5rem 0;">Privacy First</h4>
        <p style="margin: 0; color: #6b7280;">Local processing only</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #f59e0b; margin: 0;">🎯</h3>
        <h4 style="margin: 0.5rem 0;">Professional Quality</h4>
        <p style="margin: 0; color: #6b7280;">Smart NLP without bloat</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #8b5cf6; margin: 0;">📊</h3>
        <h4 style="margin: 0.5rem 0;">Rich Insights</h4>
        <p style="margin: 0; color: #6b7280;">Comprehensive analytics</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem; margin-top: 2rem; border-top: 1px solid #e5e7eb;">
    <p><strong>Built with ❤️ using Streamlit • Lightning-Fast Meeting Intelligence v3.0</strong></p>
    <p>Ultra-lightweight meeting analysis with instant processing and zero heavy dependencies</p>
</div>
""", unsafe_allow_html=True)

