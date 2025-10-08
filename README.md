# Meeting Notes Summarizer & Action Item Extractor (Mistral + spaCy fallback)

## Overview
This project:
- Summarizes meeting transcripts using a LLM (Mistral) when available.
- Extracts action items into a JSON / CSV table (task, owner, deadline).
- Provides a Streamlit UI to paste transcripts and get summary + action items interactively.

## Features
- Mistral integration for summarization and JSON action extraction (optional).
- spaCy-based rule fallback extractor if Mistral is not configured or fails.
- Streamlit web UI.
- Outputs action items as CSV and JSON downloads.

## Setup
1. Create a venv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\\Scripts\\activate on Windows
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. (Optional) Set environment variables for Mistral (if you have an endpoint):
   ```bash
   export MISTRAL_API_URL="https://your-mistral-endpoint.example/v1/generate"
   export MISTRAL_API_KEY="sk-..."
   ```

3. Run the CLI app (fallback only if --mistral not passed):
   ```bash
   python app.py -i sample_transcript.txt
   ```

4. Run the Streamlit UI:
   ```bash
   streamlit run streamlit_app.py
   ```

## Notes
- The `mistral_client.py` is intentionally generic. Adapt the request payload and response parsing to match your provider's API.
- Prompts are located in `prompts.py` and are tuned for deterministic output (temperature=0).
- The Streamlit app supports downloading the action items as CSV or JSON.
