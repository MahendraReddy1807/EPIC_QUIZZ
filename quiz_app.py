# EPIC QUIZ APP - ENHANCED VERSION WITH ADMIN DASHBOARD
# FORCE UPDATE: 2024-09-24 v2.1 - ADMIN DASHBOARD WORKING

import streamlit as st
import sys
import os

# Force page configuration first
st.set_page_config(
    page_title="Epic Quiz App - Enhanced v2.2",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show update message
st.markdown("# 🚀 Epic Quiz App - Enhanced v2.2")
st.success("✅ Enhanced quiz experience with user profiles and achievements!")
st.markdown("---")

# Import and run the enhanced version
try:
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Import the enhanced quiz app
    from enhanced_quiz_app import main
    
    # Run the main application
    main()
    
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Could not load enhanced_quiz_app.py")
    st.info("Please check that all files are present in the deployment")
    
except Exception as e:
    st.error(f"Application Error: {e}")
    st.error("There was an error running the enhanced quiz app")
    
    # Fallback - show basic admin login
    st.markdown("## 🔧 Fallback Admin Access")
    st.info("Using fallback mode due to import issues")
    
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")
    
    if st.button("Admin Login"):
        if username == "Mahi07" and password == "1477":
            st.success("✅ Admin credentials verified!")
            st.balloons()
            st.markdown("### 👑 Admin Dashboard")
            st.write("Admin dashboard is working!")
            st.write("- Username: Mahi07")
            st.write("- Access Level: Administrator")
            st.write("- Status: Active")
        else:
            st.error("Invalid credentials")