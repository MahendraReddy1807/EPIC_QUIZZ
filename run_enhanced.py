#!/usr/bin/env python3
"""
Script to run the enhanced Epic Quiz App
"""

import subprocess
import sys
import os

def main():
    """Run the enhanced quiz app"""
    print("🚀 Starting Enhanced Epic Quiz App...")
    print("📚 Features: User Profiles, Achievements, Themes, Accessibility, Certificates")
    print("🌐 Access at: http://localhost:8501")
    print("-" * 60)
    
    try:
        # Run the enhanced app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "enhanced_quiz_app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Enhanced Epic Quiz App!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())