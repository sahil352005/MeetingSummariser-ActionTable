import streamlit as st

st.title("ℹ️ About")
st.markdown(
    """
This app summarizes meeting transcripts and extracts action items.

Technologies:
- Streamlit UI
- Optional Mistral LLM API for high-quality summaries and structured action items
- spaCy-based rule fallback for offline/basic extraction
- Audio transcription via SpeechRecognition + pydub
"""
)

st.markdown("""
Setup tips:
- Ensure `en_core_web_sm` spaCy model is installed.
- To enable Mistral, set `MISTRAL_API_URL` and `MISTRAL_API_KEY`.
""")

