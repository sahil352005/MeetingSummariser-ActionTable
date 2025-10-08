import streamlit as st
from text_to_audio import text_to_speech
from pathlib import Path

st.title("🗣️ Text to Speech")
st.markdown("Convert a text file into an audio file using your local TTS engine.")

uploaded = st.file_uploader("Upload a text file", type=["txt"])
custom_text = st.text_area("Or paste text here", height=200)

out_name = st.text_input("Output filename (optional, .mp3 or .wav)")

if st.button("Convert to Audio"):
    input_path = None
    if uploaded is not None:
        input_path = Path(f"temp_{uploaded.name}")
        with open(input_path, "wb") as f:
            f.write(uploaded.getbuffer())
    elif custom_text.strip():
        input_path = Path("temp_input.txt")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(custom_text)

    if input_path is None:
        st.error("Please upload a file or paste text.")
    else:
        out_path = text_to_speech(str(input_path), out_name or None)
        if out_path:
            st.success(f"Created: {out_path}")
            try:
                st.audio(str(out_path))
            except Exception:
                pass
        else:
            st.error("Failed to create audio.")

