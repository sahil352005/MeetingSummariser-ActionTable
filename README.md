# ⚡ Lightning-Fast Meeting Intelligence Platform

An ultra-lightweight Streamlit application that transforms meeting recordings and transcripts into actionable insights with instant processing and zero heavy dependencies.



## ✨ Features

### 🎤 **Audio Processing**
- **Multi-format support**: MP3, WAV, M4A, OGG, FLAC
- **Chunked transcription**: Handles long recordings without truncation
- **Progress tracking**: Real-time transcription progress
- **High-quality speech recognition**: Google Speech Recognition API

### ⚡ **Lightning-Fast Analysis**
- **Instant summaries**: Ultra-fast NLP processing (0.02 seconds)
- **Smart action extraction**: Automatically identifies tasks, owners, deadlines, and priorities
- **Real-time analytics**: Meeting type, sentiment, and productivity scoring
- **Lightweight processing**: No heavy models, minimal dependencies, maximum speed

### 🗣️ **Text-to-Speech**
- **Chunked TTS**: Handles long text without truncation
- **Multiple formats**: WAV and MP3 output
- **Audio preview**: Built-in audio player
- **File management**: Automatic cleanup and download options

### 🎨 **Modern Interface**
- **Multipage design**: Organized navigation with dedicated pages
- **Professional UI**: Modern gradients, cards, and responsive layouts
- **Progress indicators**: Visual feedback for all operations
- **User-friendly**: Intuitive design with helpful tooltips and guides

## 🚀 Quick Start

### 1. **Installation**
   ```bash
# Clone or download the project
cd meeting_action_extractor

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install minimal dependencies (under 2 minutes)
pip install -r requirements.txt
   ```

### 2. **Run the Application**
```bash
streamlit run streamlit_app.py
```

## 🚀 **Deployment Options**

### **Local Development**
```bash
streamlit run streamlit_app.py
```

### **Streamlit Cloud**
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://share.streamlit.io/)
3. Add your secrets via the dashboard or `.streamlit/secrets.toml`
4. Deploy with one click!

### **Other Platforms**
The app can be deployed on any platform that supports Python and Streamlit:
- **Heroku**: Use Procfile and requirements.txt
- **Railway**: Direct GitHub integration
- **Render**: Web service deployment
- **Docker**: Containerized deployment

## 📱 **Pages Overview**

### 🏠 **Home Page**
- Welcome screen with feature overview
- Sample transcript loader
- Navigation guide
- How-it-works explanation

### 🔎 **Summarizer Page**
- **Text Input**: Paste meeting transcripts directly
- **Audio Input**: Upload audio files for transcription
- **AI Analysis**: Generate summaries and extract action items
- **Export Options**: Download results as CSV or JSON

### 🗣️ **Text-to-Speech Page**
- **File Upload**: Convert text files to audio
- **Text Input**: Paste text directly for conversion
- **Format Selection**: Choose WAV or MP3 output
- **Audio Preview**: Listen before downloading

### ℹ️ **About Page**
- Detailed feature descriptions
- Technology stack information
- Setup instructions
- Usage tips and best practices

## ⚙️ **Configuration**

### **Lightning-Fast NLP Processing (Zero Heavy Dependencies)**

The application uses optimized NLP techniques for:
- **Instant Processing**: 0.02-second summary generation with professional quality
- **Smart Pattern Recognition**: Efficient action item detection with priority analysis
- **Real-time Analytics**: Meeting type, sentiment, and productivity scoring
- **Intelligent Parsing**: Automatic speaker detection and content organization
- **Frequency Analysis**: Statistical keyword extraction and topic identification

**Ultra-lightweight** - no heavy models, instant processing, runs anywhere.

### **Audio Requirements**
For MP3 export in Text-to-Speech:
- Install **ffmpeg** on your system
- Ensure **pydub** can access it

**WAV format** works without additional setup.

## 🛠️ **Technology Stack**

### **Core Technologies**
- **Streamlit**: Modern web interface framework
- **pandas**: Data manipulation and export
- **Custom NLP Engine**: Lightning-fast text processing
- **SpeechRecognition**: Audio transcription
- **pydub**: Audio processing and format conversion
- **pyttsx3**: Text-to-speech synthesis

### **Lightning-Fast NLP Engine**
- **Instant Processing**: 0.02-second summary generation with professional quality
- **Smart Pattern Matching**: Efficient action item extraction with priority assignment
- **Real-time Analytics**: Meeting intelligence without heavy model dependencies
- **Google Speech Recognition**: Reliable audio transcription service

## 📋 **Usage Examples**

### **Audio Transcription**
1. Navigate to **Summarizer** page
2. Switch to **Audio Input** tab
3. Upload your meeting recording
4. Click **Transcribe Audio**
5. Review generated transcript
6. Generate summary and action items

### **Text Analysis**
1. Go to **Summarizer** page
2. Use **Text Input** tab
3. Paste your meeting transcript
4. Enable **Enhanced NLP Analysis** (recommended)
5. Click **Generate Summary & Actions**
6. Download results in preferred format

### **Text-to-Speech**
1. Visit **Text-to-Speech** page
2. Upload a text file or paste content
3. Choose output format (WAV/MP3)
4. Click **Convert to Audio**
5. Preview and download the audio file

## 💡 **Best Practices**

### **Audio Quality**
- Use clear recordings for better transcription accuracy
- Ensure good microphone quality and minimal background noise
- Consider speaker separation for multi-person meetings

### **Text Formatting**
- Use speaker labels: `John: Let's discuss the project timeline`
- Include timestamps if available
- Separate different topics with line breaks

### **Performance**
- Lightning-fast processing: summaries in 0.02 seconds
- No model downloads or heavy dependencies required
- Runs efficiently on any device with minimal resources

## 🔧 **Troubleshooting**

### **Common Issues**

**Transcription fails:**
- Check audio file format compatibility
- Ensure stable internet connection (for Google Speech Recognition)
- Try shorter audio segments

**Processing tips:**
- Use clear speaker labels (Name: content format)
- Ensure proper sentence structure for better analysis
- UTF-8 encoding recommended for best results

**Performance optimization:**
- App processes instantly with minimal resource usage
- No heavy model downloads or complex setup required
- Works reliably on any device or platform

## 📄 **File Structure**

```
meeting_action_extractor/
├── streamlit_app.py          # Main app entry point
├── pages/                    # Multipage structure
│   ├── 1_🔎_Summarizer.py    # Analysis page
│   ├── 2_🗣️_Text_to_Speech.py # TTS page
│   └── 3_ℹ️_About.py         # Information page
├── audio_processor.py        # Audio transcription logic
├── extractor.py             # Action item extraction
├── nlp_summarizer.py        # Fast NLP processing engine
├── text_to_audio.py         # TTS functionality
├── utils.py                 # Utility functions
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 **License**

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit • Lightning-Fast Meeting Intelligence v3.0**
