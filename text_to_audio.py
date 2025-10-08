from pathlib import Path
import pyttsx3
import argparse
from typing import List
from pydub import AudioSegment
import tempfile
import os

def _chunk_text(text: str, max_chars: int = 1800) -> List[str]:
    """Split long text into manageable chunks near sentence boundaries."""
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            # try to break on a sentence boundary
            breakpoint = max(
                text.rfind(". ", start, end),
                text.rfind("! ", start, end),
                text.rfind("? ", start, end),
                text.rfind("\n", start, end)
            )
            if breakpoint == -1 or breakpoint <= start:
                breakpoint = text.rfind(" ", start, end)
            if breakpoint == -1 or breakpoint <= start:
                breakpoint = end
            else:
                breakpoint += 1  # include the separator
        else:
            breakpoint = end
        chunks.append(text[start:breakpoint].strip())
        start = breakpoint
    return [c for c in chunks if c]


def text_to_speech(input_file: str, output_file: str = None):
    """Convert text file to audio file with chunking to avoid truncation.

    Returns the output file path string on success, otherwise None.
    """
    # Read input text file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Choose output extension (prefer wav for compatibility)
    if output_file is None:
        output_path = Path(input_file).with_suffix('.wav')
    else:
        output_path = Path(output_file)

    # Initialize TTS engine
    engine = pyttsx3.init()

    # Prepare temp wav files per chunk
    temp_wavs: List[str] = []
    try:
        chunks = _chunk_text(text)
        for chunk in chunks:
            tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            tmp_path = tmp.name
            tmp.close()
            temp_wavs.append(tmp_path)
            engine.save_to_file(chunk, tmp_path)

        # Process all queued saves
        engine.runAndWait()

        # Concatenate chunks
        combined: AudioSegment | None = None
        for idx, wav_path in enumerate(temp_wavs):
            seg = AudioSegment.from_wav(wav_path)
            combined = seg if combined is None else combined + seg

        if combined is None:
            raise RuntimeError('No audio generated from chunks')

        # Export to desired format based on suffix
        suffix = output_path.suffix.lower()
        if suffix == '.mp3':
            combined.export(str(output_path), format='mp3')
        else:
            # default/export wav
            if suffix != '.wav':
                output_path = output_path.with_suffix('.wav')
            combined.export(str(output_path), format='wav')

        print(f"Successfully created audio file: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"Error converting text to speech: {str(e)}")
        return None
    finally:
        for p in temp_wavs:
            try:
                os.unlink(p)
            except Exception:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text file to audio')
    parser.add_argument('input_file', help='Path to input text file')
    parser.add_argument('--output', '-o', help='Path to output audio file (optional)')
    args = parser.parse_args()
    
    text_to_speech(args.input_file, args.output)