from pathlib import Path
import pyttsx3
import argparse

def text_to_speech(input_file: str, output_file: str = None):
    """Convert text file to audio file."""
    
    # Read input text file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = Path(input_file).with_suffix('.mp3')
    
    # Convert text to speech and save
    try:
        engine.save_to_file(text, str(output_file))
        engine.runAndWait()
        print(f"Successfully created audio file: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error converting text to speech: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text file to audio')
    parser.add_argument('input_file', help='Path to input text file')
    parser.add_argument('--output', '-o', help='Path to output audio file (optional)')
    args = parser.parse_args()
    
    text_to_speech(args.input_file, args.output)