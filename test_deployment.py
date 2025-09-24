import streamlit as st
import datetime

st.title("🔧 Deployment Test")
st.write(f"Current time: {datetime.datetime.now()}")
st.write("If you see this, the deployment is updating!")
st.success("✅ This file was created at 2024-09-24 22:35 UTC")

# Test admin functionality
if st.button("Test Admin Dashboard"):
    try:
        from enhanced_quiz_app import show_admin_dashboard
        show_admin_dashboard()
    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Admin dashboard not working yet")