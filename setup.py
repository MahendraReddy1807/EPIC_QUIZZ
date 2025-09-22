#!/usr/bin/env python3
"""
Setup script for Epic Quiz App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def run_tests():
    """Run test suite"""
    print("🧪 Running tests...")
    try:
        subprocess.check_call([sys.executable, "test_quiz.py"])
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Some tests failed")
        return False

def run_demo():
    """Run demo script"""
    print("🎯 Running demo...")
    try:
        subprocess.check_call([sys.executable, "demo.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Demo failed")
        return False

def main():
    """Main setup function"""
    print("🚀 Epic Quiz App Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but continuing...")
    
    # Run demo
    run_demo()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Run the app: streamlit run quiz_app.py")
    print("   2. Open your browser to the displayed URL")
    print("   3. Start taking quizzes!")
    print("\n📚 For more info, check README.md")

if __name__ == "__main__":
    main()