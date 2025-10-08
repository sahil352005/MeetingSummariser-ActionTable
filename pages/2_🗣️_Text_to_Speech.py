import streamlit as st
from text_to_audio import text_to_speech
from pathlib import Path
import os

# Custom CSS for modern styling
st.markdown("""
<style>
    .page-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .input-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .result-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #06b6d4;
        margin: 1rem 0;
    }
    .upload-area {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
        margin: 1rem 0;
    }
    .feature-highlight {
        background: #fef3c7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🗣️ Text to Speech</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Convert your text into high-quality audio</p>
</div>
""", unsafe_allow_html=True)

# Feature highlight
st.markdown("""
<div class="feature-highlight">
    <strong>🎯 Features:</strong> Supports long text with chunking • Multiple output formats • High-quality TTS engine • Progress tracking
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("## 📥 Input Options")

tab1, tab2 = st.tabs(["📄 File Upload", "✍️ Text Input"])

with tab1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### Upload a text file")
    uploaded = st.file_uploader(
        "Choose a text file", 
        type=["txt"], 
        help="Upload a .txt file to convert to audio"
    )
    
    if uploaded is not None:
        st.success(f"✅ File uploaded: {uploaded.name}")
        # Show file preview
        with st.expander("📖 Preview file content"):
            content = uploaded.read().decode('utf-8')
            st.text_area("File content", content, height=150, disabled=True)
            uploaded.seek(0)  # Reset file pointer
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### Or paste text directly")
    custom_text = st.text_area(
        "Enter your text here", 
        height=200,
        placeholder="Type or paste the text you want to convert to speech...\n\nExample:\nHello! This is a sample text that will be converted to audio using our text-to-speech engine."
    )
    
    if custom_text.strip():
        char_count = len(custom_text)
        st.info(f"📊 Text length: {char_count} characters")
    st.markdown('</div>', unsafe_allow_html=True)

# Output options
st.markdown("## ⚙️ Output Options")

col1, col2 = st.columns(2)

with col1:
    output_format = st.selectbox(
        "Output format",
        ["WAV", "MP3"],
        help="WAV provides better quality, MP3 is more compressed"
    )

with col2:
    out_name = st.text_input(
        "Custom filename (optional)",
        placeholder="my_audio_file",
        help="Leave empty for auto-generated name"
    )

# Conversion section
st.markdown("## 🎵 Convert to Audio")

if st.button("🚀 Convert to Audio", type="primary", use_container_width=True):
    input_path = None
    
    # Determine input source
    if uploaded is not None:
        input_path = Path(f"temp_{uploaded.name}")
        with open(input_path, "wb") as f:
            f.write(uploaded.getbuffer())
    elif custom_text.strip():
        input_path = Path("temp_input.txt")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(custom_text)

    if input_path is None:
        st.error("❌ Please upload a file or paste text first!")
    else:
        # Determine output filename
        if out_name:
            output_file = f"{out_name}.{output_format.lower()}"
        else:
            output_file = None
        
        with st.spinner('🎤 Converting text to speech...'):
            out_path = text_to_speech(str(input_path), output_file)
            
            # Clean up temp file
            try:
                os.remove(input_path)
            except:
                pass
        
        if out_path:
            st.markdown("## 🎉 Conversion Complete!")
            st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
            st.success(f"✅ Audio file created: {out_path}")
            
            # Show file info
            if os.path.exists(out_path):
                file_size = os.path.getsize(out_path) / 1024  # KB
                st.info(f"📁 File size: {file_size:.1f} KB")
            
            # Audio player
            st.markdown("### 🎧 Preview")
            try:
                st.audio(str(out_path))
            except Exception as e:
                st.warning(f"Could not preview audio: {e}")
            
            # Download button
            with open(out_path, "rb") as f:
                st.download_button(
                    "📥 Download Audio File",
                    f.read(),
                    file_name=os.path.basename(out_path),
                    mime="audio/wav" if output_format == "WAV" else "audio/mpeg",
                    use_container_width=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Failed to create audio file. Please try again.")

