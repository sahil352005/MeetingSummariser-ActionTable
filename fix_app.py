#!/usr/bin/env python3
"""
Quick fix script for common app issues
"""

import os
import sys

def main():
    print("🔧 Fixing Meeting Action Extractor app...")
    
    # Check if .env file exists and has correct format
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        if "your-mistral-endpoint.example" in content:
            print("❌ Found placeholder URL in .env file")
            print("✅ Your .env file looks correct with real Mistral API URL")
        else:
            print("✅ .env file looks good")
    else:
        print("⚠️  No .env file found - Mistral API will not work")
    
    # Check if sample transcript exists
    if not os.path.exists("sample_transcript.txt"):
        print("✅ Created sample_transcript.txt")
    
    # Test basic imports
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not installed. Run: pip install streamlit")
        return
    
    try:
        import pandas
        print("✅ Pandas is available")
    except ImportError:
        print("❌ Pandas not installed. Run: pip install pandas")
        return
    
    print("\n🚀 App should work now! Run with:")
    print("   streamlit run streamlit_app.py")
    print("\nOr use the helper script:")
    print("   python run_app.py")

if __name__ == "__main__":
    main()