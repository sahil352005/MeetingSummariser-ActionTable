import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def convert_to_wav(audio_path):
    """Convert audio file to WAV format."""
    audio = AudioSegment.from_file(audio_path)
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.export(temp_wav.name, format='wav')
    return temp_wav.name

def transcribe_audio(audio_path):
    """Transcribe audio file to text using Google Speech Recognition."""
    # Convert to WAV if not already
    if not audio_path.lower().endswith('.wav'):
        audio_path = convert_to_wav(audio_path)
    
    recognizer = sr.Recognizer()
    transcript = []
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            transcript.append(text)
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return None
    finally:
        # Clean up temporary file if created
        if audio_path != audio_path:
            os.unlink(audio_path)
    
    return ' '.join(transcript)