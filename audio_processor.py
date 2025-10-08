import os
import tempfile
from typing import Callable, Optional, List
import speech_recognition as sr
from pydub import AudioSegment

def convert_to_wav(audio_path):
    """Convert audio file to WAV format. Returns (wav_path, created_temp: bool)."""
    if audio_path.lower().endswith('.wav'):
        return audio_path, False
    audio = AudioSegment.from_file(audio_path)
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.export(temp_wav.name, format='wav')
    return temp_wav.name, True

def _split_to_chunks(wav_path: str, chunk_ms: int = 60000, overlap_ms: int = 1000) -> List[str]:
    """Split wav file path into fixed-size chunks with small overlap. Returns list of temp wav paths."""
    audio = AudioSegment.from_wav(wav_path)
    chunks: List[str] = []
    start = 0
    total = len(audio)
    while start < total:
        end = min(start + chunk_ms, total)
        seg = audio[start:end]
        if start != 0 and overlap_ms > 0:
            # add slight overlap at beginning to avoid boundary loss
            seg = audio[max(0, start - overlap_ms):end]
        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        seg.export(tmp.name, format='wav')
        chunks.append(tmp.name)
        start = end
    return chunks

def transcribe_audio(audio_path: str, on_progress: Optional[Callable[[float], None]] = None) -> Optional[str]:
    """Transcribe audio file to text using Google Speech Recognition with chunking.

    on_progress: optional callback receiving float in [0,1] to report progress.
    """
    wav_path, created_temp = convert_to_wav(audio_path)
    recognizer = sr.Recognizer()
    parts: List[str] = []
    chunk_paths: List[str] = []
    try:
        chunk_paths = _split_to_chunks(wav_path, chunk_ms=60000, overlap_ms=800)
        total = len(chunk_paths)
        for idx, path in enumerate(chunk_paths, start=1):
            try:
                with sr.AudioFile(path) as source:
                    # Optionally adjust for ambient noise per chunk
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio)
                    parts.append(text)
            except Exception as e:
                print(f"Chunk {idx}/{total} transcription error: {str(e)}")
                # Keep going; insert placeholder or skip
                continue
            finally:
                if on_progress:
                    try:
                        on_progress(min(idx / total, 1.0))
                    except Exception:
                        pass
    except Exception as e:
        print(f"Error preparing audio for transcription: {str(e)}")
        return None
    finally:
        # Cleanup temp chunk files
        for p in chunk_paths:
            try:
                os.unlink(p)
            except Exception:
                pass
        if created_temp:
            try:
                os.unlink(wav_path)
            except Exception:
                pass

    return ' '.join(parts).strip() if parts else None