#!/usr/bin/env python3
"""
Script to reset the app by clearing all data files
"""

import os
import json

def reset_app_data():
    """Reset all app data files"""
    print("🔄 Resetting Epic Quiz App data...")
    
    # Files to reset
    files_to_reset = [
        "quiz_scores.json",
        "user_profiles.json"
    ]
    
    for file_path in files_to_reset:
        if os.path.exists(file_path):
            try:
                if file_path.endswith('.json'):
                    # Reset JSON files to empty structures
                    if 'scores' in file_path:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump([], f, indent=2)
                    elif 'profiles' in file_path:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump({}, f, indent=2)
                    print(f"✅ Reset: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not reset {file_path}: {e}")
    
    print("🎉 App data reset complete!")
    print("💡 Now restart the app with: python run_enhanced.py")

if __name__ == "__main__":
    reset_app_data()