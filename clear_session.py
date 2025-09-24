#!/usr/bin/env python3
"""
Script to clear Streamlit session state and cache
"""

import os
import shutil
import glob

def clear_streamlit_cache():
    """Clear Streamlit cache and session files"""
    print("🧹 Clearing Streamlit cache and session data...")
    
    # Common Streamlit cache directories
    cache_dirs = [
        ".streamlit",
        "~/.streamlit",
        "./.streamlit",
        "./streamlit_cache",
        "./__pycache__",
        "./.cache"
    ]
    
    for cache_dir in cache_dirs:
        expanded_dir = os.path.expanduser(cache_dir)
        if os.path.exists(expanded_dir):
            try:
                shutil.rmtree(expanded_dir)
                print(f"✅ Cleared: {expanded_dir}")
            except Exception as e:
                print(f"⚠️  Could not clear {expanded_dir}: {e}")
    
    # Clear Python cache files
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print(f"✅ Cleared: {pycache_dir}")
        except Exception as e:
            print(f"⚠️  Could not clear {pycache_dir}: {e}")
    
    print("🎉 Cache clearing complete!")
    print("💡 Now restart the app with: python run_enhanced.py")

if __name__ == "__main__":
    clear_streamlit_cache()