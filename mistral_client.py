from dotenv import load_dotenv
load_dotenv()
import os
import requests

# Use environment variables first, then fallback to Streamlit secrets
MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

# If not found in env vars, try Streamlit secrets
if not MISTRAL_API_URL or not MISTRAL_API_KEY:
    try:
        import streamlit as st
        MISTRAL_API_URL = MISTRAL_API_URL or st.secrets["api"]["MISTRAL_API_URL"]
        MISTRAL_API_KEY = MISTRAL_API_KEY or st.secrets["api"]["MISTRAL_API_KEY"]
    except (ImportError, KeyError, AttributeError):
        pass

def call_mistral(prompt: str, max_tokens: int = 512, model: str = 'mistral-small'):
    if not MISTRAL_API_URL or not MISTRAL_API_KEY:
        raise EnvironmentError('Set MISTRAL_API_URL and MISTRAL_API_KEY in environment variables.')

    headers = {
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.0
    }

    resp = requests.post(MISTRAL_API_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if 'choices' in data and len(data['choices']) > 0:
        return data['choices'][0]['message']['content']
    return str(data)
