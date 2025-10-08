import streamlit as st
import pandas as pd
from extractor import parse_mistral_action_items, rule_based_action_extraction
try:
    from mistral_client import call_mistral
except Exception:
    call_mistral = None
from prompts import SUMMARY_PROMPT, ACTION_ITEM_PROMPT
from audio_processor import transcribe_audio
import os

st.set_page_config(page_title='Meeting Notes Summarizer', layout='wide')

st.title('Meeting Notes Summarizer & Action Item Extractor')

# Add file uploader for audio
audio_file = st.file_uploader("Upload audio file (MP3, WAV, M4A, OGG, FLAC)", 
                             type=['mp3', 'wav', 'm4a', 'ogg', 'flac'])

# Add tabs for input methods
tab1, tab2 = st.tabs(["Text Input", "Audio Input"])

with tab1:
    transcript = st.text_area('Paste transcript here', height=300)

with tab2:
    if audio_file:
        with st.spinner('Transcribing audio...'):
            # Save uploaded file temporarily
            temp_path = f"temp_{audio_file.name}"
            with open(temp_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            # Get transcript
            transcript = transcribe_audio(temp_path)
            
            # Clean up
            os.remove(temp_path)
            
            if transcript:
                st.text_area("Generated Transcript", transcript, height=300)
            else:
                st.error("Failed to transcribe audio")

use_mistral = st.checkbox('Use Mistral API (requires env vars)', value=False)

if st.button('Generate Summary & Actions'):
    if not transcript or not transcript.strip():
        st.error('Please provide a transcript first!')
    else:
        with st.spinner('Generating summary...'):
            summary = None
            if use_mistral and call_mistral is not None:
                try:
                    summary = call_mistral(SUMMARY_PROMPT.format(transcript=transcript), max_tokens=200)
                except Exception as e:
                    st.error(f'Mistral error: {e}')
            if not summary:
                sents = [s.strip() for s in transcript.split('\n') if s.strip()]
                summary = '\n'.join(sents[:5])
            st.subheader('Summary')
            st.write(summary)

        with st.spinner('Extracting action items...'):
            items = None
            if use_mistral and call_mistral is not None:
                try:
                    resp = call_mistral(ACTION_ITEM_PROMPT.format(transcript=transcript), max_tokens=512)
                    items = parse_mistral_action_items(resp)
                except Exception as e:
                    st.error(f'Mistral error: {e}')
            if not items:
                items = rule_based_action_extraction(transcript)

            if items:
                df = pd.DataFrame(items)
                st.subheader('Action Items (Table)')
                st.dataframe(df)
                st.download_button('Download CSV', df.to_csv(index=False).encode('utf-8'), 'action_items.csv', 'text/csv')
                st.download_button('Download JSON', df.to_json(orient='records').encode('utf-8'), 'action_items.json', 'application/json')
            else:
                st.info('No action items found.')
