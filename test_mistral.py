#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

try:
    from mistral_client import call_mistral
    print("Testing Mistral API connection...")
    
    test_prompt = "Hello, please respond with 'API connection successful'"
    response = call_mistral(test_prompt, max_tokens=50)
    print(f"✅ Success! Response: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check your .env file has correct MISTRAL_API_URL and MISTRAL_API_KEY")
    print("2. Verify your API key is valid")
    print("3. Check internet connection")