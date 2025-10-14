#!/usr/bin/env python3
"""
Simple script to run the Meeting Action Extractor app
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required = ['streamlit', 'pandas', 'requests']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install streamlit pandas requests python-dotenv")
        return False
    return True

def main():
    print("🚀 Starting Meeting Action Extractor...")
    
    if not check_dependencies():
        sys.exit(1)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    main()