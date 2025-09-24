#!/usr/bin/env python3
"""
Streamlit Cloud entry point - ensures the enhanced version is loaded
VERSION 2.1 - ADMIN DASHBOARD WORKING - FORCE UPDATE 20240924
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import and run the enhanced quiz app
    from enhanced_quiz_app import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    import streamlit as st
    st.error(f"Import error: {e}")
    st.error("Please check that all required files are present")
except Exception as e:
    import streamlit as st
    st.error(f"Error running app: {e}")
    st.error("Please check the logs for more details")