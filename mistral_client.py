from dotenv import load_dotenv
load_dotenv()
import os
import requests

# Try Streamlit secrets first (for cloud deployment), then fallback to environment variables
try:
    import streamlit as st
    MISTRAL_API_URL = st.secrets["api"]["MISTRAL_API_URL"]
    MISTRAL_API_KEY = st.secrets["api"]["MISTRAL_API_KEY"]
except (ImportError, KeyError, AttributeError):
    # Fallback to environment variables for local development
    MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def call_mistral(prompt: str, max_tokens: int = 512, model: str = 'mistral-small'):
    if not MISTRAL_API_URL or not MISTRAL_API_KEY:
        raise EnvironmentError('Set MISTRAL_API_URL and MISTRAL_API_KEY in Streamlit secrets or environment variables.')

    headers = {
        'Authorization': f'Bearer {MISTRAL_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": model,  # Available models: mistral-tiny, mistral-small, mistral-medium
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
