# EPIC QUIZ APP - ENHANCED VERSION 2.1 - ADMIN DASHBOARD WORKING
# FORCE UPDATE: 2024-09-24 22:30 UTC
# This is the main entry point for Streamlit Cloud

import streamlit as st

# Force page config first
st.set_page_config(
    page_title="Epic Quiz App - Enhanced v2.1",
    page_icon="📚",
    layout="wide"
)

# Add version indicator at the very top
st.markdown("### 🚀 Epic Quiz App - Enhanced v2.1 (Admin Dashboard Working)")
st.markdown("---")

# Import and run the enhanced quiz app
try:
    from enhanced_quiz_app import main
    main()
except Exception as e:
    st.error(f"Error loading app: {e}")
    st.error("Please refresh the page or contact support")