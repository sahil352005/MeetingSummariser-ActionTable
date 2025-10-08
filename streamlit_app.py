import streamlit as st
import pandas as pd
from extractor import parse_mistral_action_items, rule_based_action_extraction
try:
    from mistral_client import call_mistral
except Exception:
    call_mistral = None
from prompts import SUMMARY_PROMPT, ACTION_ITEM_PROMPT

st.set_page_config(page_title='Meeting Notes Summarizer', layout='wide')

st.title('Meeting Notes Summarizer & Action Item Extractor')
st.write('Paste your meeting transcript below, then click **Generate** to get a summary and structured action items.')

transcript = st.text_area('Transcript', height=300)
use_mistral = st.checkbox('Use Mistral API (requires env vars)', value=False)

if st.button('Generate'):
    if not transcript.strip():
        st.warning('Please paste a transcript first.')
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
