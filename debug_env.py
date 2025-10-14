from dotenv import load_dotenv
load_dotenv()
import os

print("Environment variables:")
print(f"MISTRAL_API_URL: {os.getenv('MISTRAL_API_URL')}")
print(f"MISTRAL_API_KEY: {os.getenv('MISTRAL_API_KEY')[:10]}..." if os.getenv('MISTRAL_API_KEY') else "MISTRAL_API_KEY: None")

try:
    import streamlit as st
    print("\nStreamlit secrets:")
    try:
        print(f"st.secrets API URL: {st.secrets['api']['MISTRAL_API_URL']}")
        print(f"st.secrets API KEY: {st.secrets['api']['MISTRAL_API_KEY'][:10]}...")
    except:
        print("No Streamlit secrets found")
except ImportError:
    print("Streamlit not available")