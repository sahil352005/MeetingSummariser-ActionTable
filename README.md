# 📝 Meeting Notes Summarizer & Action Item Extractor

A powerful Streamlit application that transforms meeting recordings and transcripts into actionable insights with a modern, professional interface.

## ✨ Features

### 🎤 **Audio Processing**
- **Multi-format support**: MP3, WAV, M4A, OGG, FLAC
- **Chunked transcription**: Handles long recordings without truncation
- **Progress tracking**: Real-time transcription progress
- **High-quality speech recognition**: Google Speech Recognition API

### 📊 **Smart Analysis**
- **AI-powered summaries**: Mistral LLM integration for intelligent meeting summaries
- **Action item extraction**: Automatically identifies tasks, owners, and deadlines
- **Rule-based fallback**: spaCy-based extraction when AI is unavailable
- **Multiple export formats**: CSV and JSON downloads

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

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
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

### **Optional: Mistral AI Integration**

#### **Local Development**
Set these environment variables:
```bash
export MISTRAL_API_URL="https://your-mistral-endpoint.example/v1/generate"
export MISTRAL_API_KEY="sk-..."
```

#### **Streamlit Cloud Deployment**
1. Create `.streamlit/secrets.toml` file:
```toml
[api]
MISTRAL_API_URL = "https://your-mistral-endpoint.example/v1/generate"
MISTRAL_API_KEY = "sk-your-api-key-here"
```
2. Upload the secrets file to your Streamlit Cloud app
3. The app will automatically detect and use these credentials

**Without Mistral**: The app automatically falls back to rule-based extraction using spaCy.

### **Audio Requirements**
For MP3 export in Text-to-Speech:
- Install **ffmpeg** on your system
- Ensure **pydub** can access it

**WAV format** works without additional setup.

## 🛠️ **Technology Stack**

### **Core Technologies**
- **Streamlit**: Modern web interface framework
- **pandas**: Data manipulation and export
- **spaCy**: Natural language processing
- **SpeechRecognition**: Audio transcription
- **pydub**: Audio processing and format conversion
- **pyttsx3**: Text-to-speech synthesis

### **AI Integration**
- **Mistral LLM API**: High-quality summaries and structured extraction
- **Google Speech Recognition**: Audio transcription service
- **Rule-based fallback**: Offline processing capabilities

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
4. Enable **Mistral API** (optional)
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

### **Long Files**
- The app automatically chunks long audio for processing
- Large text files are split into manageable segments
- Progress bars show real-time processing status

## 🔧 **Troubleshooting**

### **Common Issues**

**Transcription fails:**
- Check audio file format compatibility
- Ensure stable internet connection (for Google Speech Recognition)
- Try shorter audio segments

**Mistral API errors:**
- Verify environment variables are set correctly
- Check API endpoint and key validity
- App will fallback to rule-based extraction

**TTS conversion issues:**
- Install ffmpeg for MP3 support
- Check text file encoding (UTF-8 recommended)
- Ensure sufficient disk space for output files

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
├── mistral_client.py        # AI API integration
├── text_to_audio.py         # TTS functionality
├── prompts.py               # AI prompt templates
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

**Built with ❤️ using Streamlit • Meeting Notes Summarizer v2.0**
