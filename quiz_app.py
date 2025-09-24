import streamlit as st
import json
import datetime
import pandas as pd
import os
import random
import hashlib
import time
from typing import Dict, List, Optional

# Enhanced imports for new features
import base64
from pathlib import Path

# Initialize session state for user management
def init_session_state():
    """Initialize session state variables"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'theme' not in st.session_state:
        st.session_state.theme = 'default'
    if 'accessibility_mode' not in st.session_state:
        st.session_state.accessibility_mode = False
    if 'font_size' not in st.session_state:
        st.session_state.font_size = 'medium'
    if 'sound_enabled' not in st.session_state:
        st.session_state.sound_enabled = True
    if 'enhanced_mode' not in st.session_state:
        st.session_state.enhanced_mode = True

# User Profile Management
class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.created_date = datetime.datetime.now().isoformat()
        self.total_quizzes = 0
        self.total_score = 0
        self.achievements = []
        self.streak_days = 0
        self.last_quiz_date = None
        self.xp_points = 50  # Give new users 50 starting XP to show progress bar
        self.level = 1
        self.preferred_language = 'english'
        self.quiz_history = []
        
    def to_dict(self):
        return {
            'username': self.username,
            'created_date': self.created_date,
            'total_quizzes': self.total_quizzes,
            'total_score': self.total_score,
            'achievements': self.achievements,
            'streak_days': self.streak_days,
            'last_quiz_date': self.last_quiz_date,
            'xp_points': self.xp_points,
            'level': self.level,
            'preferred_language': self.preferred_language,
            'quiz_history': self.quiz_history
        }
    
    @classmethod
    def from_dict(cls, data):
        profile = cls(data['username'])
        for key, value in data.items():
            setattr(profile, key, value)
        return profile

# User Management Functions
@st.cache_data
def load_users():
    """Load user profiles from file"""
    if os.path.exists("user_profiles.json"):
        with open("user_profiles.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users_data):
    """Save user profiles to file"""
    with open("user_profiles.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)
    load_users.clear()

def create_user_profile(username: str) -> UserProfile:
    """Create a new user profile"""
    users = load_users()
    if username.lower() in [u.lower() for u in users.keys()]:
        return None  # User already exists
    
    profile = UserProfile(username)
    users[username] = profile.to_dict()
    save_users(users)
    return profile

def get_user_profile(username: str) -> Optional[UserProfile]:
    """Get user profile by username"""
    users = load_users()
    for stored_username, profile_data in users.items():
        if stored_username.lower() == username.lower():
            return UserProfile.from_dict(profile_data)
    return None

def update_user_profile(profile: UserProfile):
    """Update user profile"""
    users = load_users()
    users[profile.username] = profile.to_dict()
    save_users(users)

# Achievement System
class AchievementSystem:
    ACHIEVEMENTS = {
        'first_quiz': {'name': '🎯 First Steps', 'description': 'Complete your first quiz', 'xp': 50},
        'perfect_score': {'name': '💯 Perfectionist', 'description': 'Score 100% on any quiz', 'xp': 200},
        'high_scorer': {'name': '🌟 High Achiever', 'description': 'Score 80% or higher', 'xp': 100},
        'quiz_master': {'name': '🏆 Quiz Master', 'description': 'Complete 10 quizzes', 'xp': 300},
        'streak_3': {'name': '🔥 On Fire', 'description': '3-day quiz streak', 'xp': 150},
        'streak_7': {'name': '⚡ Lightning', 'description': '7-day quiz streak', 'xp': 300},
        'bilingual': {'name': '🌍 Polyglot', 'description': 'Take quizzes in both languages', 'xp': 250},
        'epic_scholar': {'name': '📚 Epic Scholar', 'description': 'Complete both Mahabharata and Ramayana quizzes', 'xp': 400},
        'level_5': {'name': '🎖️ Veteran', 'description': 'Reach Level 5', 'xp': 500},
        'level_10': {'name': '👑 Master', 'description': 'Reach Level 10', 'xp': 1000}
    }
    
    @staticmethod
    def check_achievements(profile: UserProfile, quiz_result: dict) -> List[str]:
        """Check and award new achievements"""
        new_achievements = []
        
        # First quiz
        if profile.total_quizzes == 1 and 'first_quiz' not in profile.achievements:
            new_achievements.append('first_quiz')
        
        # Perfect score
        if quiz_result['percentage'] == 100 and 'perfect_score' not in profile.achievements:
            new_achievements.append('perfect_score')
        
        # High scorer
        if quiz_result['percentage'] >= 80 and 'high_scorer' not in profile.achievements:
            new_achievements.append('high_scorer')
        
        # Quiz master
        if profile.total_quizzes >= 10 and 'quiz_master' not in profile.achievements:
            new_achievements.append('quiz_master')
        
        # Streak achievements
        if profile.streak_days >= 3 and 'streak_3' not in profile.achievements:
            new_achievements.append('streak_3')
        if profile.streak_days >= 7 and 'streak_7' not in profile.achievements:
            new_achievements.append('streak_7')
        
        # Level achievements
        if profile.level >= 5 and 'level_5' not in profile.achievements:
            new_achievements.append('level_5')
        if profile.level >= 10 and 'level_10' not in profile.achievements:
            new_achievements.append('level_10')
        
        # Add new achievements to profile
        for achievement in new_achievements:
            profile.achievements.append(achievement)
            profile.xp_points += AchievementSystem.ACHIEVEMENTS[achievement]['xp']
        
        return new_achievements

# XP and Level System
def calculate_level(xp_points: int) -> int:
    """Calculate user level based on XP points"""
    if xp_points < 100:
        return 1
    elif xp_points < 300:
        return 2
    elif xp_points < 600:
        return 3
    elif xp_points < 1000:
        return 4
    elif xp_points < 1500:
        return 5
    elif xp_points < 2100:
        return 6
    elif xp_points < 2800:
        return 7
    elif xp_points < 3600:
        return 8
    elif xp_points < 4500:
        return 9
    else:
        return min(10 + (xp_points - 4500) // 1000, 50)

def get_xp_for_quiz(score: int, total: int, difficulty_bonus: float = 1.0) -> int:
    """Calculate XP earned for a quiz"""
    base_xp = (score / total) * 100
    return int(base_xp * difficulty_bonus)

def calculate_xp_progress(profile: UserProfile) -> float:
    """Calculate XP progress percentage to next level"""
    next_level_xp = (profile.level * 500)
    current_level_xp = ((profile.level - 1) * 500)
    if next_level_xp == current_level_xp:
        return 100.0
    progress = ((profile.xp_points - current_level_xp) / (next_level_xp - current_level_xp)) * 100
    # Ensure minimum 2% width so progress bar is always visible
    return min(100.0, max(2.0, progress))

def get_xp_progress_text(profile: UserProfile) -> str:
    """Get XP progress text for display"""
    next_level_xp = (profile.level * 500)
    current_level_xp = ((profile.level - 1) * 500)
    current_progress = profile.xp_points - current_level_xp
    needed_for_next = next_level_xp - current_level_xp
    
    if profile.xp_points == 0:
        return f"Complete your first quiz to start earning XP! (0 / {needed_for_next} XP to Level {profile.level + 1})"
    else:
        return f"{current_progress} / {needed_for_next} XP to Level {profile.level + 1}"

# Cache questions to avoid reloading - using fast questions for better performance
@st.cache_data
def load_questions():
    """Load and cache questions for better performance"""
    from fast_questions import get_mahabharata_questions, get_ramayana_questions
    return {
        "mahabharata": get_mahabharata_questions(),
        "ramayana": get_ramayana_questions()
    }

# Quiz questions data - Load with caching for performance
@st.cache_data
def get_quiz_data():
    """Get quiz data with caching"""
    questions = load_questions()
    return {
        "mahabharata": {
            "title": {"english": "Mahabharata Quiz", "telugu": "మహాభారత క్విజ్"},
            "questions": questions["mahabharata"]
        },
        "ramayana": {
            "title": {"english": "Ramayana Quiz", "telugu": "రామాయణ క్విజ్"},
            "questions": questions["ramayana"]
        }
    }

@st.cache_data
def load_scores():
    """Load existing scores from file with caching"""
    if os.path.exists("quiz_scores.json"):
        with open("quiz_scores.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_score(name, quiz_type, score, total, language, timestamp, questions_used):
    """Save quiz score to file and clear cache"""
    scores = load_scores()
    scores.append({
        "name": name,
        "quiz_type": quiz_type,
        "score": score,
        "total": total,
        "percentage": round((score/total)*100, 2),
        "language": language,
        "timestamp": timestamp,
        "questions_used": questions_used
    })
    with open("quiz_scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
    # Clear cache to reload updated scores
    load_scores.clear()

# Theme System
def get_theme_css(theme_name: str, font_size: str, accessibility_mode: bool) -> str:
    """Generate CSS for different themes"""
    
    # Font size mapping
    font_sizes = {
        'small': {'base': '14px', 'h1': '1.8rem', 'h2': '1.5rem', 'h3': '1.3rem'},
        'medium': {'base': '16px', 'h1': '2.2rem', 'h2': '1.8rem', 'h3': '1.5rem'},
        'large': {'base': '18px', 'h1': '2.5rem', 'h2': '2rem', 'h3': '1.7rem'},
        'extra-large': {'base': '20px', 'h1': '2.8rem', 'h2': '2.3rem', 'h3': '2rem'}
    }
    
    fs = font_sizes[font_size]
    
    # Theme configurations
    themes = {
        'default': {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'accent': '#f093fb',
            'background': '#ffffff',
            'surface': '#f8f9fa',
            'text': '#2c3e50',
            'text_secondary': '#7f8c8d'
        },
        'dark': {
            'primary': '#4a90e2',
            'secondary': '#5a67d8',
            'accent': '#ed64a6',
            'background': '#1a202c',
            'surface': '#2d3748',
            'text': '#f7fafc',
            'text_secondary': '#a0aec0'
        },
        'temple': {
            'primary': '#d4af37',
            'secondary': '#b8860b',
            'accent': '#ff6b35',
            'background': '#fdf6e3',
            'surface': '#f4e4bc',
            'text': '#8b4513',
            'text_secondary': '#a0522d'
        },
        'forest': {
            'primary': '#2d5016',
            'secondary': '#3e6b1f',
            'accent': '#7cb342',
            'background': '#f1f8e9',
            'surface': '#e8f5e8',
            'text': '#1b5e20',
            'text_secondary': '#388e3c'
        }
    }
    
    theme = themes.get(theme_name, themes['default'])
    
    # High contrast mode for accessibility
    if accessibility_mode:
        theme['text'] = '#000000'
        theme['background'] = '#ffffff'
        theme['surface'] = '#f0f0f0'
    
    return f"""
    <style>
    /* Base styling with proper text visibility */
    .stApp {{
        background-color: {theme['background']};
        color: {theme['text']} !important;
        font-size: {fs['base']};
    }}
    
    /* Ensure main text is visible but allow specific overrides */
    .stApp, .stMarkdown, p, div, span {{
        color: {theme['text']} !important;
    }}
    
    /* Headers with proper spacing */
    h1 {{ 
        font-size: {fs['h1']} !important; 
        color: {theme['primary']} !important; 
        margin-bottom: 1rem !important;
        line-height: 1.2 !important;
    }}
    h2 {{ 
        font-size: {fs['h2']} !important; 
        color: {theme['secondary']} !important; 
        margin: 1rem 0 !important;
        line-height: 1.3 !important;
    }}
    h3 {{ 
        font-size: {fs['h3']} !important; 
        color: {theme['text']} !important; 
        margin: 0.8rem 0 !important;
        line-height: 1.4 !important;
    }}
    
    /* Paragraphs and text elements */
    p, div, span {{
        color: {theme['text']} !important;
        line-height: 1.6 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Streamlit specific elements */
    .stMarkdown p {{
        color: {theme['text']} !important;
        margin-bottom: 1rem !important;
    }}
    
    .stInfo {{
        background-color: {theme['surface']} !important;
        color: {theme['text']} !important;
        border: 1px solid {theme['primary']} !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
    }}
    
    .stSuccess {{
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
    }}
    
    /* Fix button text visibility */
    .stButton > button {{
        color: white !important;
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: {fs['base']} !important;
        font-weight: 600 !important;
        margin: 0.5rem 0 !important;
    }}
    
    /* Clean radio button styling like the image */
    .stRadio {{
        background: white !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        border: 1px solid #ddd !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }}
    
    .stRadio > div {{
        background: transparent !important;
    }}
    
    .stRadio label {{
        color: #2d3436 !important;
        font-size: {fs['base']} !important;
        font-weight: 400 !important;
        margin: 0.4rem 0 !important;
        padding: 0.8rem 1rem !important;
        display: block !important;
        cursor: pointer !important;
        border-radius: 8px !important;
        border: 1px solid #e9ecef !important;
        transition: all 0.2s ease !important;
        background: #fdfdfd !important;
    }}
    
    .stRadio label:hover {{
        background: #f1f3f4 !important;
        border-color: #6c5ce7 !important;
        color: #2d3436 !important;
    }}
    
    /* Radio button input styling */
    .stRadio input[type="radio"] {{
        margin-right: 0.8rem !important;
        transform: scale(1.2) !important;
        accent-color: #6c5ce7 !important;
    }}
    
    /* Ensure radio button options are properly spaced */
    .stRadio div[role="radiogroup"] > label {{
        color: #2d3436 !important;
        background: #fdfdfd !important;
        padding: 0.8rem 1rem !important;
        margin: 0.3rem 0 !important;
        border-radius: 8px !important;
        border: 1px solid #e9ecef !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    .stRadio div[role="radiogroup"] > label:hover {{
        background: #f1f3f4 !important;
        border-color: #6c5ce7 !important;
        color: #2d3436 !important;
    }}
    
    /* Selected radio button styling */
    .stRadio div[role="radiogroup"] > label[data-checked="true"] {{
        background: #e8f4fd !important;
        border-color: #6c5ce7 !important;
        font-weight: 500 !important;
        color: #2d3436 !important;
    }}
    
    /* Fix text input labels */
    .stTextInput label {{
        color: {theme['text']} !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Fix selectbox labels */
    .stSelectbox label {{
        color: {theme['text']} !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Ensure proper spacing for all elements */
    .element-container {{
        margin-bottom: 1rem !important;
    }}
    
    /* Fix markdown text visibility */
    .stMarkdown {{
        color: {theme['text']} !important;
    }}
    
    /* Fix caption text */
    .caption {{
        color: {theme['text_secondary']} !important;
        font-size: 0.9rem !important;
        margin-top: 0.5rem !important;
    }}
    
    /* Ensure proper line height for readability */
    body, .stApp {{
        line-height: 1.6 !important;
    }}
    
    /* Fix any white text on white background issues */
    .stApp > div {{
        color: {theme['text']} !important;
    }}
    
    /* Override any conflicting styles */
    .stMarkdown > div {{
        color: {theme['text']} !important;
    }}
    
    /* Fix subheader visibility */
    .stMarkdown h3 {{
        color: {theme['text']} !important;
        font-weight: 600 !important;
        margin: 1rem 0 0.5rem 0 !important;
    }}
    
    /* Add proper spacing between sections */
    .stMarkdown hr {{
        margin: 2rem 0 !important;
        border-color: {theme['text_secondary']} !important;
    }}
    
    /* Form styling improvements with better visibility */
    .stTextInput > div > div > input {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        border: 2px solid {theme['primary']}40 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: {fs['base']} !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {theme['primary']} !important;
        box-shadow: 0 0 0 2px {theme['primary']}20 !important;
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {theme['text_secondary']} !important;
        opacity: 0.7 !important;
    }}
    
    /* Selectbox styling with proper visibility */
    .stSelectbox > div > div > select {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        border: 2px solid {theme['primary']}40 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }}
    
    .stSelectbox > div > div > select:focus {{
        border-color: {theme['primary']} !important;
        box-shadow: 0 0 0 2px {theme['primary']}20 !important;
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    
    /* Fix selectbox dropdown options */
    .stSelectbox > div > div > select option {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        padding: 0.5rem !important;
    }}
    
    /* Fix selectbox text visibility in all states */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        border: 2px solid {theme['primary']}40 !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: {theme['text']} !important;
    }}
    
    /* Login page specific styling is now inline */
    
    /* Container styling with centered content and compact padding */
    .stContainer {{
        background-color: {theme['surface']} !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid {theme['primary']}20 !important;
        text-align: center !important;
    }}
    
    /* Center all content within tabs with compact padding */
    .stTabs [data-baseweb="tab-panel"] {{
        text-align: center !important;
        padding: 1rem 0.5rem !important;
    }}
    
    /* Center form elements */
    .stTabs [data-baseweb="tab-panel"] .stMarkdown {{
        text-align: center !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] h3 {{
        text-align: center !important;
        margin-bottom: 1.5rem !important;
    }}
    
    /* Center input labels */
    .stTabs [data-baseweb="tab-panel"] .stTextInput label {{
        text-align: center !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stSelectbox label {{
        text-align: center !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Center input fields */
    .stTabs [data-baseweb="tab-panel"] .stTextInput {{
        text-align: center !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stSelectbox {{
        text-align: center !important;
    }}
    
    /* Center buttons in tabs */
    .stTabs [data-baseweb="tab-panel"] .stButton {{
        text-align: center !important;
        margin: 0.5rem auto !important;
    }}
    
    /* Force center alignment for all tab content */
    .stTabs [data-baseweb="tab-panel"] * {{
        text-align: center !important;
    }}
    
    /* Override for input fields to keep text left-aligned inside the field */
    .stTabs [data-baseweb="tab-panel"] input {{
        text-align: left !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] select {{
        text-align: left !important;
    }}
    
    /* Center the input containers */
    .stTabs [data-baseweb="tab-panel"] .stTextInput > div {{
        text-align: center !important;
        margin: 0 auto !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stSelectbox > div {{
        text-align: center !important;
        margin: 0 auto !important;
    }}
    
    /* Center error/success/warning messages in tabs */
    .stTabs [data-baseweb="tab-panel"] .stAlert {{
        text-align: center !important;
        margin: 1rem auto !important;
    }}
    
    /* Center help text */
    .stTabs [data-baseweb="tab-panel"] .stTextInput > label > div[data-testid="stMarkdownContainer"] {{
        text-align: center !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stSelectbox > label > div[data-testid="stMarkdownContainer"] {{
        text-align: center !important;
    }}
    
    /* Reduce spacing between form elements in tabs */
    .stTabs [data-baseweb="tab-panel"] .stTextInput {{
        margin-bottom: 0.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stSelectbox {{
        margin-bottom: 0.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] .stButton {{
        margin-top: 0.5rem !important;
        margin-bottom: 0.25rem !important;
    }}
    
    /* Reduce spacing in tab headers */
    .stTabs [data-baseweb="tab-panel"] h3 {{
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
    }}
    
    /* Compact alert messages */
    .stTabs [data-baseweb="tab-panel"] .stAlert {{
        margin: 0.5rem auto !important;
        padding: 0.5rem !important;
    }}
    
    /* Force visibility for all form elements */
    input, select, textarea {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    
    /* Override any dark theme conflicts */
    .stSelectbox [data-testid="stMarkdownContainer"] {{
        color: {theme['text']} !important;
    }}
    
    .stTextInput [data-testid="stMarkdownContainer"] {{
        color: {theme['text']} !important;
    }}
    
    /* Ensure dropdown visibility */
    .stSelectbox div[role="listbox"] {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        border: 1px solid {theme['primary']} !important;
    }}
    
    .stSelectbox div[role="option"] {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    
    .stSelectbox div[role="option"]:hover {{
        background-color: {theme['primary']}20 !important;
        color: {theme['text']} !important;
    }}
    
    /* Streamlit specific selectbox fixes */
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: white !important;
        color: #000000 !important;
        border: 2px solid {theme['primary']} !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div > div {{
        color: #000000 !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: #000000 !important;
    }}
    
    /* Fix dropdown menu */
    .stSelectbox ul[role="listbox"] {{
        background-color: white !important;
        border: 1px solid {theme['primary']} !important;
    }}
    
    .stSelectbox li[role="option"] {{
        background-color: white !important;
        color: #000000 !important;
        padding: 0.5rem !important;
    }}
    
    .stSelectbox li[role="option"]:hover {{
        background-color: {theme['primary']}20 !important;
        color: #000000 !important;
    }}
    
    .stSelectbox li[role="option"][aria-selected="true"] {{
        background-color: {theme['primary']} !important;
        color: white !important;
    }}
    
    /* Fix text input */
    .stTextInput input {{
        background-color: white !important;
        color: #000000 !important;
        border: 2px solid {theme['primary']}40 !important;
    }}
    
    .stTextInput input:focus {{
        background-color: white !important;
        color: #000000 !important;
        border-color: {theme['primary']} !important;
    }}
    
    /* Keep button text white */
    .stButton > button {{
        color: white !important;
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
    }}
    
    /* Keep card text as intended */
    .score-card, .score-card * {{
        color: white !important;
    }}
    
    .achievement-card, .achievement-card * {{
        color: white !important;
    }}
    
    .performance-excellent, .performance-excellent * {{
        color: white !important;
    }}
    
    .performance-good, .performance-good * {{
        color: white !important;
    }}
    
    .performance-improve, .performance-improve * {{
        color: white !important;
    }}
    
    /* Override the global color rule for specific elements */
    .stSelectbox, .stSelectbox * {{
        color: #000000 !important;
    }}
    
    .stTextInput, .stTextInput * {{
        color: #000000 !important;
    }}
    
    /* But keep labels visible */
    .stSelectbox > label {{
        color: {theme['text']} !important;
    }}
    
    .stTextInput > label {{
        color: {theme['text']} !important;
    }}
    
    /* Help text styling */
    .stTextInput > label > div[data-testid="stMarkdownContainer"] > p {{
        color: {theme['text_secondary']} !important;
        font-size: 0.85rem !important;
        margin-top: 0.25rem !important;
    }}
    
    /* Compact question form styling */
    .stForm {{
        background-color: white !important;
        border: 2px solid {theme['primary']}30 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }}
    
    /* Reduce spacing in forms */
    .stForm > div {{
        margin-bottom: 0.5rem !important;
    }}
    
    /* Compact form buttons */
    .stForm .stButton {{
        margin-top: 0.8rem !important;
    }}
    
    .stForm .stButton > button {{
        padding: 0.6rem 1.2rem !important;
        font-size: 0.9rem !important;
    }}
    
    /* Question text styling */
    .stForm h3 {{
        color: {theme['text']} !important;
        font-size: {fs['h3']} !important;
        margin-bottom: 1rem !important;
        line-height: 1.4 !important;
    }}
    
    /* Progress bar styling */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
        height: 12px !important;
        border-radius: 6px !important;
    }}
    
    /* Expander styling for results */
    .streamlit-expanderHeader {{
        background-color: {theme['surface']} !important;
        color: {theme['text']} !important;
        border: 1px solid {theme['primary']}30 !important;
        border-radius: 8px !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {theme['background']} !important;
        border: 1px solid {theme['primary']}20 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }}
    
    /* Enhanced score card */
    .score-card {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 1.5rem 0;
        animation: slideInUp 0.6s ease-out;
    }}
    
    .score-card h2 {{
        margin: 0;
        font-size: 2.8rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }}
    
    .score-card h3 {{
        margin: 0.5rem 0;
        font-size: 2.2rem !important;
        color: #FFD700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* Achievement card */
    .achievement-card {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        animation: bounceIn 0.8s ease-out;
    }}
    
    /* User profile card */
    .profile-card {{
        background: linear-gradient(135deg, {theme['surface']} 0%, {theme['background']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid {theme['primary']};
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    
    /* Statistics container */
    .stats-container {{
        background: linear-gradient(135deg, {theme['surface']} 0%, {theme['background']} 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid {theme['primary']};
    }}
    
    .stats-item {{
        display: inline-block;
        margin: 1rem;
        text-align: center;
        transition: transform 0.3s ease;
    }}
    
    .stats-item:hover {{
        transform: scale(1.05);
    }}
    
    .stats-number {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {theme['primary']};
        display: block;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    
    .stats-label {{
        font-size: 1rem;
        color: {theme['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }}
    
    /* Performance cards */
    .performance-excellent {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: slideInRight 0.6s ease-out;
    }}
    
    .performance-good {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: slideInRight 0.6s ease-out;
    }}
    
    .performance-improve {{
        background: linear-gradient(135deg, {theme['accent']} 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: slideInRight 0.6s ease-out;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: {fs['base']};
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    /* Animations */
    @keyframes slideInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes bounceIn {{
        0% {{
            opacity: 0;
            transform: scale(0.3);
        }}
        50% {{
            opacity: 1;
            transform: scale(1.05);
        }}
        70% {{
            transform: scale(0.9);
        }}
        100% {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes pulse {{
        0% {{
            transform: scale(1);
        }}
        50% {{
            transform: scale(1.05);
        }}
        100% {{
            transform: scale(1);
        }}
    }}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .score-card {{
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .score-card h2 {{
            font-size: 2.2rem !important;
        }}
        
        .score-card h3 {{
            font-size: 1.8rem !important;
        }}
        
        .stats-container {{
            padding: 1.5rem;
        }}
        
        .stats-item {{
            margin: 0.5rem;
        }}
        
        .stats-number {{
            font-size: 2rem;
        }}
    }}
    
    /* Accessibility enhancements */
    .stButton > button:focus,
    .stRadio > div:focus-within {{
        outline: 3px solid {theme['accent']};
        outline-offset: 2px;
    }}
    </style>
    """

# Certificate Generation
def generate_certificate(username: str, quiz_type: str, score: int, total: int, percentage: float) -> str:
    """Generate a certificate for the user"""
    certificate_html = f"""
    <div style="
        width: 100%;
        max-width: 800px;
        height: 600px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 10px solid #d4af37;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: white;
        font-family: 'Georgia', serif;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        margin: 20px auto;
    ">
        <h1 style="font-size: 2.5rem; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🏆 CERTIFICATE OF ACHIEVEMENT 🏆
        </h1>
        
        <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0;">
            <h2 style="font-size: 1.3rem; margin-bottom: 20px;">This is to certify that</h2>
            
            <h1 style="font-size: 2rem; color: #FFD700; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                {username.upper()}
            </h1>
            
            <h2 style="font-size: 1.2rem; margin: 20px 0;">
                has successfully completed the<br>
                <strong style="font-size: 1.5rem; color: #FFD700;">{quiz_type.title()} Quiz</strong>
            </h2>
            
            <h2 style="font-size: 1.3rem; margin: 20px 0;">
                with a score of <strong style="color: #FFD700;">{score}/{total} ({percentage}%)</strong>
            </h2>
            
            <p style="font-size: 0.9rem; margin-top: 30px; opacity: 0.9;">
                Demonstrating knowledge of ancient Indian epics and cultural heritage
            </p>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-top: 40px; font-size: 0.8rem;">
            <div>
                <p>Date: {datetime.datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            <div>
                <p>Epic Quiz App</p>
                <p>Cultural Education Platform</p>
            </div>
        </div>
    </div>
    """
    return certificate_html

def get_user_history(name, quiz_type):
    """Get user's quiz history to avoid repeated questions"""
    scores = load_scores()
    user_scores = [s for s in scores if s["name"].lower() == name.lower() and s["quiz_type"] == quiz_type]
    used_questions = []
    for score in user_scores:
        if "questions_used" in score:
            used_questions.extend(score["questions_used"])
    return list(set(used_questions))  # Remove duplicates

@st.cache_data
def get_random_questions(quiz_type, num_questions=20, exclude_questions=None):
    """Get random questions with difficulty distribution: 6 easy, 8 medium, 6 hard"""
    if exclude_questions is None:
        exclude_questions = []
    
    quiz_data = get_quiz_data()
    all_questions = quiz_data[quiz_type]["questions"]
    
    # Separate questions by difficulty
    easy_questions = []
    medium_questions = []
    hard_questions = []
    
    for i, q in enumerate(all_questions):
        question_id = hashlib.md5(q["question"]["english"].encode()).hexdigest()[:8]
        difficulty = q.get("difficulty", "medium")  # Default to medium if not specified
        
        if question_id not in exclude_questions:
            if difficulty == "easy":
                easy_questions.append((i, question_id, q))
            elif difficulty == "medium":
                medium_questions.append((i, question_id, q))
            elif difficulty == "hard":
                hard_questions.append((i, question_id, q))
    
    # If we don't have enough questions in any category, add from excluded ones
    if len(easy_questions) < 3 or len(medium_questions) < 4 or len(hard_questions) < 3:
        for i, q in enumerate(all_questions):
            question_id = hashlib.md5(q["question"]["english"].encode()).hexdigest()[:8]
            difficulty = q.get("difficulty", "medium")
            
            if question_id in exclude_questions:
                if difficulty == "easy" and len(easy_questions) < 3:
                    easy_questions.append((i, question_id, q))
                elif difficulty == "medium" and len(medium_questions) < 4:
                    medium_questions.append((i, question_id, q))
                elif difficulty == "hard" and len(hard_questions) < 3:
                    hard_questions.append((i, question_id, q))
    
    # Select questions according to difficulty distribution for 20 questions
    selected_questions = []
    
    # Select 6 easy questions
    if len(easy_questions) >= 6:
        selected_questions.extend(random.sample(easy_questions, 6))
    else:
        selected_questions.extend(easy_questions)
        # Fill remaining with medium questions
        remaining = 6 - len(easy_questions)
        if len(medium_questions) >= remaining:
            selected_questions.extend(random.sample(medium_questions, remaining))
    
    # Select 8 medium questions (excluding already selected)
    available_medium = [q for q in medium_questions if q not in selected_questions]
    if len(available_medium) >= 8:
        selected_questions.extend(random.sample(available_medium, 8))
    else:
        selected_questions.extend(available_medium)
        # Fill remaining with any available questions
        remaining = 8 - len(available_medium)
        all_available = [q for q in easy_questions + hard_questions if q not in selected_questions]
        if len(all_available) >= remaining:
            selected_questions.extend(random.sample(all_available, remaining))
    
    # Select 6 hard questions (excluding already selected)
    available_hard = [q for q in hard_questions if q not in selected_questions]
    if len(available_hard) >= 6:
        selected_questions.extend(random.sample(available_hard, 6))
    else:
        selected_questions.extend(available_hard)
        # Fill remaining with any available questions
        remaining = 6 - len(available_hard)
        all_available = [q for q in easy_questions + medium_questions if q not in selected_questions]
        if len(all_available) >= remaining:
            selected_questions.extend(random.sample(all_available, remaining))
    
    # Shuffle the final selection to randomize order
    random.shuffle(selected_questions)
    
    # Ensure we have exactly 20 questions
    return selected_questions[:20]

def display_leaderboard():
    """Display leaderboard with CSV download option - shows best score per user per quiz"""
    scores = load_scores()
    if not scores:
        st.info("No scores yet! Take a quiz to see the leaderboard.")
        return
    
    df = pd.DataFrame(scores)
    
    # Get best score per user per quiz type (eliminate duplicates)
    df_best = df.loc[df.groupby(['name', 'quiz_type'])['percentage'].idxmax()]
    df_best = df_best.sort_values(['percentage', 'timestamp'], ascending=[False, False])
    
    st.subheader("🏆 Leaderboard")
    st.caption("Showing best score per user for each quiz type")
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["🏆 Best Scores", "📊 All Attempts", "📈 Statistics"])
    
    with tab1:
        # Best scores view (no duplicates)
        col1, col2 = st.columns([3, 1])
        with col2:
            # Prepare CSV data for best scores
            csv_data = df_best[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']].copy()
            csv_data['Quiz'] = csv_data['quiz_type'].str.title()
            csv_data['Date'] = pd.to_datetime(csv_data['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            csv_export = csv_data[['name', 'Quiz', 'score', 'total', 'percentage', 'language', 'Date']].rename(columns={
                'name': 'Name',
                'Quiz': 'Quiz Type',
                'score': 'Score',
                'total': 'Total Questions',
                'percentage': 'Percentage',
                'language': 'Language',
                'Date': 'Date & Time'
            })
            
            st.download_button(
                label="📥 Download Best Scores",
                data=csv_export.to_csv(index=False),
                file_name=f"quiz_best_scores_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col1:
            st.write(f"**Total Participants:** {len(df_best['name'].unique())}")
            st.write(f"**Total Quiz Attempts:** {len(df)}")
        
        # Top scores display (best per user per quiz)
        if len(df_best) > 0:
            top_scores = df_best.head(15)[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']]
            top_scores['Quiz'] = top_scores['quiz_type'].str.title()
            top_scores['Score'] = top_scores['score'].astype(str) + '/' + top_scores['total'].astype(str) + ' (' + top_scores['percentage'].astype(str) + '%)'
            top_scores['Date'] = pd.to_datetime(top_scores['timestamp']).dt.strftime('%Y-%m-%d')
            
            display_df = top_scores[['name', 'Quiz', 'Score', 'language', 'Date']].rename(columns={
                'name': 'Name',
                'language': 'Language',
                'Date': 'Date'
            })
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No scores available yet.")
    
    with tab2:
        # All attempts view
        col1, col2 = st.columns([3, 1])
        with col2:
            # Download all attempts
            all_csv_data = df[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']].copy()
            all_csv_data['Quiz'] = all_csv_data['quiz_type'].str.title()
            all_csv_data['Date'] = pd.to_datetime(all_csv_data['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            all_csv_export = all_csv_data[['name', 'Quiz', 'score', 'total', 'percentage', 'language', 'Date']].rename(columns={
                'name': 'Name',
                'Quiz': 'Quiz Type',
                'score': 'Score',
                'total': 'Total Questions',
                'percentage': 'Percentage',
                'language': 'Language',
                'Date': 'Date & Time'
            })
            
            st.download_button(
                label="📥 Download All Attempts",
                data=all_csv_export.to_csv(index=False),
                file_name=f"quiz_all_attempts_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col1:
            st.write(f"**Total Attempts:** {len(df)}")
            st.write(f"**Unique Users:** {len(df['name'].unique())}")
        
        # Show all attempts (with duplicates)
        df_all_sorted = df.sort_values(['percentage', 'timestamp'], ascending=[False, False])
        if len(df_all_sorted) > 0:
            all_scores = df_all_sorted.head(20)[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']]
            all_scores['Quiz'] = all_scores['quiz_type'].str.title()
            all_scores['Score'] = all_scores['score'].astype(str) + '/' + all_scores['total'].astype(str) + ' (' + all_scores['percentage'].astype(str) + '%)'
            all_scores['Date'] = pd.to_datetime(all_scores['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            
            display_all_df = all_scores[['name', 'Quiz', 'Score', 'language', 'Date']].rename(columns={
                'name': 'Name',
                'language': 'Language',
                'Date': 'Date & Time'
            })
            
            st.dataframe(display_all_df, use_container_width=True, hide_index=True)
    
    with tab3:
        # Statistics view
        if len(df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Quiz Statistics")
                
                # Quiz type distribution
                quiz_counts = df['quiz_type'].value_counts()
                st.write("**Quiz Attempts by Type:**")
                for quiz_type, count in quiz_counts.items():
                    st.write(f"• {quiz_type.title()}: {count} attempts")
                
                # Language distribution
                lang_counts = df['language'].value_counts()
                st.write("\n**Language Preferences:**")
                for lang, count in lang_counts.items():
                    st.write(f"• {lang.title()}: {count} attempts")
            
            with col2:
                st.subheader("🎯 Performance Stats")
                
                # Average scores
                avg_score = df['percentage'].mean()
                st.write(f"**Average Score:** {avg_score:.1f}%")
                
                # Score distribution
                excellent = len(df[df['percentage'] >= 80])
                good = len(df[(df['percentage'] >= 60) & (df['percentage'] < 80)])
                needs_improvement = len(df[df['percentage'] < 60])
                
                st.write("**Performance Distribution:**")
                st.write(f"• Excellent (≥80%): {excellent} attempts")
                st.write(f"• Good (60-79%): {good} attempts")
                st.write(f"• Needs Improvement (<60%): {needs_improvement} attempts")
                
                # Top performer
                if len(df_best) > 0:
                    top_performer = df_best.iloc[0]
                    st.write(f"\n**🏆 Top Performer:**")
                    st.write(f"• {top_performer['name']}")
                    st.write(f"• {top_performer['percentage']}% in {top_performer['quiz_type'].title()}")
        else:
            st.info("No statistics available yet.")

def main():
    # Initialize session state
    init_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Epic Quiz App - Enhanced",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply theme CSS
    theme_css = get_theme_css(st.session_state.theme, st.session_state.font_size, st.session_state.accessibility_mode)
    st.markdown(theme_css, unsafe_allow_html=True)
    
    # Enhanced sidebar styling
    st.markdown("""
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea15 0%, #f8f9fa 100%) !important;
    }
    
    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* User stats cards */
    .stat-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateX(5px);
    }
    
    /* Navigation styling */
    .nav-item {
        background: white;
        margin: 0.3rem 0;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .nav-item:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Mode toggle styling */
    .mode-toggle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Sidebar radio buttons */
    .css-1d391kg .stRadio > div {
        background: white;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .css-1d391kg .stRadio > div:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .css-1d391kg .stRadio label {
        color: #2c3e50 !important;
        font-weight: 500;
        padding: 0.5rem;
        cursor: pointer;
    }
    
    .css-1d391kg .stRadio label:hover {
        color: #667eea !important;
    }
    
    /* Sidebar toggle styling */
    .css-1d391kg .stCheckbox {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
    
    /* Sidebar markdown styling */
    .css-1d391kg .stMarkdown {
        color: #2c3e50;
    }
    
    .css-1d391kg h3 {
        color: #2c3e50 !important;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced mode toggle in sidebar
    with st.sidebar:
        st.markdown("""
        <div class="mode-toggle">
            <h4 style="margin: 0; color: white;">⚙️ App Mode</h4>
        </div>
        """, unsafe_allow_html=True)
        
        enhanced_mode = st.toggle("Enhanced Mode", value=st.session_state.enhanced_mode, help="Enable user profiles, achievements, and themes")
        if enhanced_mode != st.session_state.enhanced_mode:
            st.session_state.enhanced_mode = enhanced_mode
            st.rerun()
    
    # Check if enhanced mode is enabled and user authentication
    if st.session_state.enhanced_mode:
        if not st.session_state.user_profile:
            show_login_page()
            return
        
        # Enhanced header with user info
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>📚 Epic Quiz App - Enhanced</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">Welcome back, {st.session_state.user_profile.username}! Level {st.session_state.user_profile.level} • {st.session_state.user_profile.xp_points} XP</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced sidebar navigation with beautiful user profile
        with st.sidebar:
            # User profile header
            st.markdown(f"""
            <div class="sidebar-header">
                <h3 style="margin: 0; color: white;">👤 {st.session_state.user_profile.username}</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: white;">Level {st.session_state.user_profile.level} Explorer</p>
            </div>
            """, unsafe_allow_html=True)
            
            # User stats with cards
            st.markdown(f"""
            <div class="stat-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2c3e50;">⭐ XP Points</span>
                    <span style="color: #e74c3c; font-weight: bold;">{st.session_state.user_profile.xp_points}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stat-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2c3e50;">🔥 Streak</span>
                    <span style="color: #f39c12; font-weight: bold;">{st.session_state.user_profile.streak_days} days</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stat-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #2c3e50;">📚 Quizzes</span>
                    <span style="color: #27ae60; font-weight: bold;">{st.session_state.user_profile.total_quizzes}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # XP Progress bar using consistent helper functions
            progress = calculate_xp_progress(st.session_state.user_profile)
            progress_text = get_xp_progress_text(st.session_state.user_profile)
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.9rem; color: #2c3e50; font-weight: 600;">Level Progress</span>
                    <span style="font-size: 0.8rem; color: #7f8c8d;">{progress:.0f}%</span>
                </div>
                <div style="background: #ecf0f1; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: {progress}%; transition: width 0.3s ease;"></div>
                </div>
                <div style="font-size: 0.8rem; color: #7f8c8d; margin-top: 0.3rem; text-align: center;">
                    {progress_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Enhanced navigation with icons and styling
            st.markdown("### 🧭 Navigation")
            page = st.radio(
                "Choose your destination:",
                ["🎯 Take Quiz", "👤 Profile", "🏆 Leaderboard", "⚙️ Settings", "📜 About", "🚪 Logout"],
                key="nav_radio",
                label_visibility="collapsed"
            )
        
        # Enhanced page routing
        if page == "🚪 Logout":
            st.session_state.user_profile = None
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()
        elif page == "👤 Profile":
            show_user_profile()
            return
        elif page == "🏆 Leaderboard":
            display_enhanced_leaderboard()
            return
        elif page == "⚙️ Settings":
            show_settings()
            return
        elif page == "📜 About":
            show_enhanced_about()
            return
        elif page == "🎯 Take Quiz":
            show_enhanced_quiz_interface()
            return
    
    else:
        # Classic mode - original interface with enhanced sidebar
        st.title("📚 Epic Quiz App")
        st.caption("Test your knowledge of Mahabharata & Ramayana")
        
        # Enhanced sidebar for classic mode
        with st.sidebar:
            st.markdown("""
            <div class="sidebar-header">
                <h3 style="margin: 0; color: white;">📚 Epic Quiz</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: white;">Classic Mode</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🧭 Navigation")
            page = st.radio("Choose your destination:", ["Take Quiz", "Leaderboard", "About"], label_visibility="collapsed")
            
            # Performance indicator with styling
            st.markdown("---")
            st.markdown("""
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; border-left: 4px solid #27ae60;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">⚡</span>
                    <div>
                        <div style="font-weight: 600; color: #27ae60;">Classic Mode</div>
                        <div style="font-size: 0.8rem; color: #2c3e50;">Simple & Fast</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if page == "Take Quiz":
            show_classic_quiz_interface()
        elif page == "Leaderboard":
            display_leaderboard()
        elif page == "About":
            show_classic_about()
    

    st.sidebar.caption("⚡ Fast Mode: Optimized for speed")
    
    if page == "Take Quiz":
        # Language selection - Interface remains in English
        st.markdown("### 🌐 Select Quiz Language")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("English", key="lang_en", use_container_width=True):
                st.session_state.selected_language = "english"
        
        with col2:
            if st.button("తెలుగు (Telugu)", key="lang_te", use_container_width=True):
                st.session_state.selected_language = "telugu"
        
        # Show selected language
        if hasattr(st.session_state, 'selected_language'):
            if st.session_state.selected_language == "english":
                st.success("✅ Selected Language: English")
                language = "English"
            else:
                st.success("✅ Selected Language: Telugu")
                language = "Telugu"
        else:
            st.info("Please select a language first")
            return
        
        # User name input - Always in English interface
        st.subheader("👤 Enter Your Name")
        user_name = st.text_input("Name:", placeholder="Enter your name here...", key="main_user_name")
        
        if user_name:
            # Quiz selection - Interface always in English
            st.subheader("📖 Select Quiz")
            st.info(f"Quiz will be displayed in: **{language}**")
            st.info("📊 **Difficulty Distribution**: 6 Easy + 8 Medium + 6 Hard questions (20 total)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🏹 Mahabharata Quiz", key="maha", use_container_width=True):
                    # Get user's previous questions to avoid repetition
                    used_questions = get_user_history(user_name, "mahabharata")
                    selected_questions = get_random_questions("mahabharata", 20, used_questions)
                    
                    st.session_state.selected_quiz = "mahabharata"
                    st.session_state.quiz_started = True
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.answers = []
                    st.session_state.user_name = user_name
                    st.session_state.language = st.session_state.selected_language
                    st.session_state.quiz_questions = selected_questions
                    st.session_state.questions_used = [qid for _, qid, _ in selected_questions]
                    st.rerun()
            
            with col2:
                if st.button("� Ramayana QuizQ", key="rama", use_container_width=True):
                    # Get user's previous questions to avoid repetition
                    used_questions = get_user_history(user_name, "ramayana")
                    selected_questions = get_random_questions("ramayana", 20, used_questions)
                    
                    st.session_state.selected_quiz = "ramayana"
                    st.session_state.quiz_started = True
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.answers = []
                    st.session_state.user_name = user_name
                    st.session_state.language = st.session_state.selected_language
                    st.session_state.quiz_questions = selected_questions
                    st.session_state.questions_used = [qid for _, qid, _ in selected_questions]
                    st.rerun()
        
        # Quiz interface
        if hasattr(st.session_state, 'quiz_started') and st.session_state.quiz_started:
            if not hasattr(st.session_state, 'quiz_questions'):
                st.error("Quiz questions not loaded properly. Please restart the quiz.")
                return
                
            questions = st.session_state.quiz_questions
            current_q = st.session_state.current_question
            lang = st.session_state.language
            
            # Show quiz title - Interface in English, but show selected language
            quiz_data = get_quiz_data()
            quiz_title_en = quiz_data[st.session_state.selected_quiz]["title"]["english"]
            st.markdown(f"## {quiz_title_en}")
            st.info(f"Language: **{language}**")
            
            # Progress bar
            progress = min((current_q + 1) / len(questions), 1.0)
            st.progress(progress)
            
            # Question counter - Always in English interface
            st.write(f"Question {current_q + 1} of {len(questions)}")
            
            if current_q < len(questions):
                _, _, question = questions[current_q]
                
                # Display difficulty level
                difficulty = question.get('difficulty', 'medium')
                difficulty_colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
                difficulty_emoji = difficulty_colors.get(difficulty, '🟡')
                
                # Display question with better styling - Content in selected language
                st.markdown("---")
                st.markdown(f"### 📝 {question['question'][lang]}")
                st.markdown(f"**Difficulty**: {difficulty_emoji} {difficulty.title()}")
                st.markdown("---")
                
                # Display options in selected language
                options = question["options"][lang]
                
                # Use a form to prevent auto-submission
                with st.form(key=f"question_form_{current_q}"):
                    # Radio button label - Always in English interface
                    selected_option = st.radio(
                        "Choose your answer:",
                        options,
                        key=f"q_{current_q}",
                        index=None
                    )
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    # Button labels - Always in English interface
                    with col1:
                        submit_answer = st.form_submit_button("Submit Answer", use_container_width=True)
                    
                    with col2:
                        if st.form_submit_button("Skip Question", use_container_width=True):
                            # Record as skipped
                            st.session_state.answers.append({
                                "question": question["question"][lang],
                                "selected": "Skipped",
                                "correct": options[question["correct"]],
                                "is_correct": False,
                                "explanation": question["explanation"][lang]
                            })
                            st.session_state.current_question += 1
                            st.rerun()
                    
                    with col3:
                        if st.form_submit_button("Restart Quiz", use_container_width=True):
                            for key in ['quiz_started', 'selected_quiz', 'current_question', 'score', 'answers', 'quiz_questions']:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.rerun()
                    
                    if submit_answer and selected_option is not None:
                        # Record answer
                        selected_index = options.index(selected_option)
                        is_correct = selected_index == question["correct"]
                        
                        st.session_state.answers.append({
                            "question": question["question"][lang],
                            "selected": selected_option,
                            "correct": options[question["correct"]],
                            "is_correct": is_correct,
                            "explanation": question["explanation"][lang]
                        })
                        
                        if is_correct:
                            st.session_state.score += 1
                        
                        st.session_state.current_question += 1
                        st.rerun()
                    elif submit_answer and selected_option is None:
                        st.warning("Please select an answer before submitting!")
            
            else:
                # Quiz completed - show results
                st.balloons()
                
                score = st.session_state.score
                total = len(questions)
                percentage = round((score/total)*100, 2)
                
                # Save score with questions used
                timestamp = datetime.datetime.now().isoformat()
                save_score(st.session_state.user_name, st.session_state.selected_quiz, 
                          score, total, st.session_state.language, timestamp, 
                          st.session_state.questions_used)
                
                # Enhanced results display with beautiful visualizations
                st.markdown(f'''
                <div class="score-card">
                    <h2>🎉 Quiz Completed!</h2>
                    <h3>Score: {score}/{total} ({percentage}%)</h3>
                    <p>Congratulations, {st.session_state.user_name}!</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Beautiful statistics display
                correct_answers = score
                incorrect_answers = total - score
                accuracy = percentage
                
                st.markdown(f'''
                <div class="stats-container">
                    <div style="text-align: center;">
                        <h3 style="color: #2c3e50; margin-bottom: 1rem;">📊 Quiz Statistics</h3>
                        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                            <div class="stats-item">
                                <span class="stats-number" style="color: #27ae60;">✅ {correct_answers}</span>
                                <span class="stats-label">Correct</span>
                            </div>
                            <div class="stats-item">
                                <span class="stats-number" style="color: #e74c3c;">❌ {incorrect_answers}</span>
                                <span class="stats-label">Incorrect</span>
                            </div>
                            <div class="stats-item">
                                <span class="stats-number" style="color: #3498db;">🎯 {accuracy}%</span>
                                <span class="stats-label">Accuracy</span>
                            </div>
                            <div class="stats-item">
                                <span class="stats-number" style="color: #9b59b6;">📚 {total}</span>
                                <span class="stats-label">Total Questions</span>
                            </div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Enhanced performance message with beautiful styling
                if percentage >= 80:
                    st.markdown('''
                    <div class="performance-excellent">
                        <h4>🌟 Outstanding Performance!</h4>
                        <p>You have exceptional knowledge of our ancient epics! Your understanding of these timeless stories is truly impressive.</p>
                    </div>
                    ''', unsafe_allow_html=True)
                elif percentage >= 60:
                    st.markdown('''
                    <div class="performance-good">
                        <h4>👍 Great Job!</h4>
                        <p>You have a solid foundation in our cultural heritage. Keep exploring these magnificent epics to deepen your knowledge!</p>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="performance-improve">
                        <h4>📚 Keep Learning!</h4>
                        <p>Every journey begins with a single step. These epics contain infinite wisdom - continue your exploration and you'll discover amazing stories!</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Show detailed results
                st.subheader("📋 Detailed Results")
                
                # Add download option for quiz results
                col1, col2 = st.columns([3, 1])
                with col2:
                    # Prepare quiz results for download
                    results_data = []
                    for i, answer in enumerate(st.session_state.answers):
                        results_data.append({
                            'Question_No': i + 1,
                            'Question': answer['question'],
                            'Your_Answer': answer['selected'],
                            'Correct_Answer': answer['correct'],
                            'Is_Correct': 'Yes' if answer['is_correct'] else 'No',
                            'Explanation': answer['explanation']
                        })
                    
                    results_df = pd.DataFrame(results_data)
                    
                    # Add summary info
                    summary_info = f"""Quiz Summary:
Name: {st.session_state.user_name}
Quiz: {st.session_state.selected_quiz.title()}
Language: {st.session_state.language.title()}
Score: {score}/{total} ({percentage}%)
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
                    
                    csv_content = summary_info + results_df.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download Results",
                        data=csv_content,
                        file_name=f"quiz_results_{st.session_state.user_name}_{st.session_state.selected_quiz}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col1:
                    st.write(f"**Questions Answered:** {len(st.session_state.answers)}")
                
                for i, answer in enumerate(st.session_state.answers):
                    # Interface labels in English, content in selected language
                    with st.expander(f"Question {i+1}: {'✅' if answer['is_correct'] else '❌'}"):
                        st.write(f"**Question:** {answer['question']}")
                        st.write(f"**Your Answer:** {answer['selected']}")
                        st.write(f"**Correct Answer:** {answer['correct']}")
                        st.write(f"**Explanation:** {answer['explanation']}")
                
                # Restart button - Always in English interface
                if st.button("Take Another Quiz", use_container_width=True):
                    for key in ['quiz_started', 'selected_quiz', 'current_question', 'score', 'answers', 'quiz_questions', 'questions_used']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
    
    elif page == "Leaderboard":
        display_leaderboard()
    
    elif page == "About":
        # About section - Always in English
        st.subheader("About This App")
        st.write("""
        This bilingual quiz app tests your knowledge of two great Indian epics:
        
        **🏹 Mahabharata** - The longest epic poem in the world, containing the Bhagavad Gita
        **🐒 Ramayana** - The story of Lord Rama's journey and triumph of good over evil
        
        **Features:**
        - Bilingual support (English & Telugu)
        - 100 questions each for Mahabharata and Ramayana
        - 20 questions per quiz (6 Easy + 8 Medium + 6 Hard)
        - Score tracking and leaderboard with CSV download
        - Detailed explanations for each answer
        - Download your quiz results as CSV
        - User-friendly interface
        - Smart question selection to avoid repetition
        - Questions are displayed in your selected language while keeping the interface in English
        
        **How to use:**
        1. Select your preferred quiz language (English or Telugu)
        2. Enter your name
        3. Choose a quiz (Mahabharata or Ramayana)
        4. Answer 20 questions in your selected language
        5. View your score and download results as CSV
        6. Check the leaderboard and download full data!
        
        **Note:** The app interface remains in English for consistency, but quiz content (questions, options, explanations) will be displayed in your selected language.
        
        **Created with ❤️ to promote knowledge of our cultural heritage**
        """)

# Enhanced UI Functions
def show_login_page():
    """Display simple login/registration page"""
    st.markdown("## 👤 Welcome to Epic Quiz App")
    st.markdown("Please login or create an account to track your progress and earn achievements!")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        
        if st.button("Login", key="login_btn", use_container_width=True, type="primary"):
            if username:
                if len(username.strip()) < 3:
                    st.error("Username must be at least 3 characters long.")
                else:
                    profile = get_user_profile(username.strip())
                    if profile:
                        st.session_state.user_profile = profile
                        st.success(f"Welcome back, {username}! 🎉")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("User not found. Please register first.")
            else:
                st.warning("Please enter a username.")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Choose Username", key="register_username", placeholder="Enter a unique username")
        preferred_lang = st.selectbox("Preferred Language", ["english", "telugu"], key="register_lang")
        
        if st.button("Create Account", key="register_btn", use_container_width=True, type="primary"):
            if new_username:
                if len(new_username) < 3:
                    st.error("Username must be at least 3 characters long.")
                elif len(new_username) > 20:
                    st.error("Username must be less than 20 characters.")
                else:
                    profile = create_user_profile(new_username)
                    if profile:
                        profile.preferred_language = preferred_lang
                        update_user_profile(profile)
                        st.session_state.user_profile = profile
                        st.success(f"Account created successfully! Welcome, {new_username}! 🎉")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("Username already exists. Please choose a different one.")
            else:
                st.warning("Please enter a username.")

def show_user_profile():
    """Display user profile with stats and achievements"""
    profile = st.session_state.user_profile
    
    # Calculate XP progress
    xp_progress = calculate_xp_progress(profile)
    xp_progress_text = get_xp_progress_text(profile)
    
    st.markdown(f"""
    <div class="profile-card">
        <h2>👤 {profile.username}'s Profile</h2>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
            <div>
                <h3>Level {profile.level}</h3>
                <p>{profile.xp_points} XP Points</p>
            </div>
            <div style="text-align: right;">
                <p><strong>Quizzes Completed:</strong> {profile.total_quizzes}</p>
                <p><strong>Current Streak:</strong> {profile.streak_days} days 🔥</p>
            </div>
        </div>
        
        <div style="margin: 1rem 0;">
            <p><strong>XP Progress to Next Level:</strong></p>
            <div style="background: #e0e0e0; border-radius: 10px; height: 20px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: {xp_progress}%; transition: width 0.3s ease;"></div>
            </div>
            <p style="font-size: 0.9rem; color: #6c757d; margin-top: 0.5rem; text-align: center;">
                {xp_progress_text}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievements section
    if profile.achievements:
        st.subheader("🏆 Your Achievements")
        cols = st.columns(3)
        for i, achievement_id in enumerate(profile.achievements):
            achievement = AchievementSystem.ACHIEVEMENTS[achievement_id]
            with cols[i % 3]:
                st.markdown(f"""
                <div class="achievement-card" style="margin: 0.5rem 0;">
                    <h4>{achievement['name']}</h4>
                    <p style="font-size: 0.9rem; margin: 0;">{achievement['description']}</p>
                    <p style="font-size: 0.8rem; margin: 0.5rem 0 0 0;">+{achievement['xp']} XP</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Complete quizzes to earn achievements! 🎯")

def show_settings():
    """Display settings page for customization"""
    st.subheader("⚙️ Settings & Customization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Theme Settings")
        
        theme_options = {
            'default': '🌟 Default',
            'dark': '🌙 Dark Mode',
            'temple': '🏛️ Temple Theme',
            'forest': '🌲 Forest Theme'
        }
        
        selected_theme = st.selectbox(
            "Choose Theme",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(st.session_state.theme)
        )
        
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()
        
        font_size_options = {
            'small': '📝 Small',
            'medium': '📄 Medium',
            'large': '📰 Large',
            'extra-large': '📊 Extra Large'
        }
        
        selected_font_size = st.selectbox(
            "Font Size",
            options=list(font_size_options.keys()),
            format_func=lambda x: font_size_options[x],
            index=list(font_size_options.keys()).index(st.session_state.font_size)
        )
        
        if selected_font_size != st.session_state.font_size:
            st.session_state.font_size = selected_font_size
            st.rerun()
    
    with col2:
        st.markdown("### ♿ Accessibility Settings")
        
        accessibility_mode = st.checkbox(
            "High Contrast Mode",
            value=st.session_state.accessibility_mode,
            help="Improves visibility for users with visual impairments"
        )
        
        if accessibility_mode != st.session_state.accessibility_mode:
            st.session_state.accessibility_mode = accessibility_mode
            st.rerun()
        
        sound_enabled = st.checkbox(
            "Sound Effects",
            value=st.session_state.sound_enabled,
            help="Enable sound effects for interactions"
        )
        
        if sound_enabled != st.session_state.sound_enabled:
            st.session_state.sound_enabled = sound_enabled
        
        st.markdown("### 🌍 Language Preferences")
        if st.session_state.user_profile:
            current_lang = st.session_state.user_profile.preferred_language
            new_lang = st.selectbox(
                "Preferred Quiz Language",
                options=['english', 'telugu'],
                index=0 if current_lang == 'english' else 1,
                format_func=lambda x: 'English' if x == 'english' else 'తెలుగు (Telugu)'
            )
            
            if new_lang != current_lang:
                st.session_state.user_profile.preferred_language = new_lang
                update_user_profile(st.session_state.user_profile)
                st.success("Language preference updated!")

def show_enhanced_about():
    """Enhanced about page"""
    st.subheader("About Epic Quiz App - Enhanced")
    st.markdown("""
    ### 🌟 Enhanced Features:
    
    **👤 User Profiles & Authentication**
    - Personal accounts with progress tracking
    - XP points and level system (1-50+)
    - Achievement badges system
    
    **🎮 Gamification**
    - 10 different achievements to unlock
    - Daily streak tracking
    - Performance-based XP rewards
    
    **🎨 Customization**
    - 4 beautiful themes (Default, Dark, Temple, Forest)
    - Adjustable font sizes
    - High contrast accessibility mode
    
    **🎓 Certification**
    - Beautiful certificates for high scores (≥70%)
    - Achievement recognition
    - Progress validation
    
    **📱 Mobile-First Design**
    - Fully responsive layout
    - Touch-friendly interface
    - Optimized for all devices
    
    ### 📚 Educational Content:
    - 100+ authentic Mahabharata questions
    - 100+ authentic Ramayana questions
    - Bilingual support (English & Telugu)
    - Detailed explanations for learning
    
    **Created with ❤️ to promote knowledge of our cultural heritage**
    """)

def show_classic_about():
    """Classic about page"""
    st.subheader("About This App")
    st.write("""
    This bilingual quiz app tests your knowledge of two great Indian epics:
    
    **🏹 Mahabharata** - The longest epic poem in the world, containing the Bhagavad Gita
    **🏺 Ramayana** - The story of Lord Rama's journey and triumph of good over evil
    
    **Features:**
    - Bilingual support (English & Telugu)
    - 100 questions each for Mahabharata and Ramayana
    - 20 questions per quiz (6 Easy + 8 Medium + 6 Hard)
    - Score tracking and leaderboard with CSV download
    - Detailed explanations for each answer
    - Download your quiz results as CSV
    - User-friendly interface
    - Smart question selection to avoid repetition
    
    **Created with ❤️ to promote knowledge of our cultural heritage**
    """)

def show_enhanced_quiz_interface():
    """Enhanced quiz interface with gamification"""
    profile = st.session_state.user_profile
    
    # Language selection (use preferred language as default)
    st.markdown("### 🌐 Select Quiz Language")
    col1, col2 = st.columns(2)
    
    default_lang = profile.preferred_language
    
    with col1:
        if st.button("English", key="enhanced_lang_en", use_container_width=True, 
                    type="primary" if default_lang == "english" else "secondary"):
            st.session_state.selected_language = "english"
    
    with col2:
        if st.button("తెలుగు (Telugu)", key="enhanced_lang_te", use_container_width=True,
                    type="primary" if default_lang == "telugu" else "secondary"):
            st.session_state.selected_language = "telugu"
    
    # Auto-select preferred language if not already selected
    if not hasattr(st.session_state, 'selected_language'):
        st.session_state.selected_language = default_lang
    
    # Show selected language with proper spacing
    if hasattr(st.session_state, 'selected_language'):
        lang_display = "English" if st.session_state.selected_language == "english" else "Telugu"
        st.markdown("")  # Add spacing
        st.success(f"✅ Selected Language: {lang_display}")
        st.markdown("")  # Add spacing
        
        # Quiz selection with proper spacing
        st.markdown("---")
        st.subheader("📖 Choose Your Epic Adventure")
        st.markdown("")  # Add spacing
        st.info(f"🌐 Quiz will be displayed in: **{lang_display}**")
        st.info("📊 **Difficulty Distribution**: 6 Easy + 8 Medium + 6 Hard questions (20 total)")
        st.markdown("")  # Add spacing
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏹 Mahabharata Quiz", key="enhanced_maha", use_container_width=True):
                start_enhanced_quiz("mahabharata")
        
        with col2:
            if st.button("🏺 Ramayana Quiz", key="enhanced_rama", use_container_width=True):
                start_enhanced_quiz("ramayana")
        
        # Show quiz interface if quiz is started
        if hasattr(st.session_state, 'quiz_started') and st.session_state.quiz_started:
            show_enhanced_quiz_questions()

def show_classic_quiz_interface():
    """Classic quiz interface (original)"""
    # Language selection - Interface remains in English
    st.markdown("### 🌐 Select Quiz Language")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("English", key="classic_lang_en", use_container_width=True):
            st.session_state.selected_language = "english"
    
    with col2:
        if st.button("తెలుగు (Telugu)", key="classic_lang_te", use_container_width=True):
            st.session_state.selected_language = "telugu"
    
    # Show selected language with proper spacing
    if hasattr(st.session_state, 'selected_language'):
        if st.session_state.selected_language == "english":
            st.markdown("")  # Add spacing
            st.success("✅ Selected Language: English")
            language = "English"
        else:
            st.markdown("")  # Add spacing
            st.success("✅ Selected Language: Telugu")
            language = "Telugu"
        st.markdown("")  # Add spacing
    else:
        st.info("Please select a language first")
        return
    
    # User name input - Always in English interface
    st.subheader("👤 Enter Your Name")
    user_name = st.text_input("Name:", placeholder="Enter your name here...", key="classic_user_name")
    
    if user_name:
        # Quiz selection - Interface always in English
        st.subheader("📖 Select Quiz")
        st.info(f"Quiz will be displayed in: **{language}**")
        st.info("📊 **Difficulty Distribution**: 6 Easy + 8 Medium + 6 Hard questions (20 total)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏹 Mahabharata Quiz", key="classic_maha", use_container_width=True):
                start_classic_quiz("mahabharata", user_name)
        
        with col2:
            if st.button("🏺 Ramayana Quiz", key="classic_rama", use_container_width=True):
                start_classic_quiz("ramayana", user_name)
        
        # Show quiz interface if quiz is started
        if hasattr(st.session_state, 'quiz_started') and st.session_state.quiz_started:
            show_classic_quiz_questions()

def start_enhanced_quiz(quiz_type):
    """Start enhanced quiz with gamification"""
    profile = st.session_state.user_profile
    used_questions = get_user_history(profile.username, quiz_type)
    selected_questions = get_random_questions(quiz_type, 20, used_questions)
    
    st.session_state.selected_quiz = quiz_type
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = selected_questions
    st.session_state.questions_used = [qid for _, qid, _ in selected_questions]
    st.session_state.quiz_start_time = time.time()
    st.rerun()

def start_classic_quiz(quiz_type, user_name):
    """Start classic quiz"""
    used_questions = get_user_history(user_name, quiz_type)
    selected_questions = get_random_questions(quiz_type, 20, used_questions)
    
    st.session_state.selected_quiz = quiz_type
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.user_name = user_name
    st.session_state.language = st.session_state.selected_language
    st.session_state.quiz_questions = selected_questions
    st.session_state.questions_used = [qid for _, qid, _ in selected_questions]
    st.rerun()

def show_enhanced_quiz_questions():
    """Enhanced quiz questions with XP preview"""
    profile = st.session_state.user_profile
    questions = st.session_state.quiz_questions
    current_q = st.session_state.current_question
    lang = st.session_state.selected_language
    
    # Quiz header
    quiz_data = get_quiz_data()
    quiz_title = quiz_data[st.session_state.selected_quiz]["title"]["english"]
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <h2>🎯 {quiz_title}</h2>
        <p>Language: <strong>{'English' if lang == 'english' else 'Telugu'}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (current_q + 1) / len(questions) if len(questions) > 0 else 0
    progress = min(max(progress, 0.0), 1.0)  # Ensure progress is between 0 and 1
    st.progress(progress)
    st.markdown(f"**Question {current_q + 1} of {len(questions)}** • **Progress: {progress*100:.0f}%**")
    
    if current_q < len(questions):
        _, _, question = questions[current_q]
        
        # Compact question display
        difficulty = question.get('difficulty', 'medium')
        difficulty_colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
        difficulty_emoji = difficulty_colors.get(difficulty, '🟡')
        xp_preview = get_xp_for_quiz(1, 1, 1.0 + (0.5 if difficulty == 'hard' else 0.2 if difficulty == 'medium' else 0))
        
        # Clean question display like the image
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; 
                    margin: 1rem 0; border-left: 4px solid #6c5ce7;">
            <h3 style="color: #2d3436; margin-bottom: 1rem; font-size: 1.3rem;">
                📝 {question['question'][lang]}
            </h3>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #636e72; font-size: 0.9rem;">
                    <strong>Difficulty:</strong> {difficulty_emoji} {difficulty.title()}
                </span>
                <span style="color: #00b894; font-size: 0.9rem;">
                    <strong>Potential XP:</strong> +{xp_preview} points
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean options display
        options = question["options"][lang]
        
        with st.form(key=f"question_form_{current_q}"):
            st.markdown("### 🤔 Choose your answer:")
            selected_option = st.radio(
                "Select one option:",
                options,
                key=f"q_{current_q}",
                index=None,
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                submit_answer = st.form_submit_button("✅ Submit Answer", use_container_width=True)
            
            with col2:
                if st.form_submit_button("⏭️ Skip Question", use_container_width=True):
                    record_answer(question, options, "Skipped", False, lang)
                    st.session_state.current_question += 1
                    st.rerun()
            
            with col3:
                if st.form_submit_button("🔄 Restart Quiz", use_container_width=True):
                    restart_quiz()
                    st.rerun()
            
            if submit_answer and selected_option is not None:
                selected_index = options.index(selected_option)
                is_correct = selected_index == question["correct"]
                
                record_answer(question, options, selected_option, is_correct, lang)
                
                if is_correct:
                    st.session_state.score += 1
                    if st.session_state.sound_enabled:
                        st.success("🎉 Correct! Well done!")
                else:
                    if st.session_state.sound_enabled:
                        st.error("❌ Incorrect. Keep learning!")
                
                st.session_state.current_question += 1
                time.sleep(1)
                st.rerun()
            elif submit_answer and selected_option is None:
                st.warning("Please select an answer before submitting!")
    
    else:
        show_enhanced_quiz_results()

def show_classic_quiz_questions():
    """Classic quiz questions interface"""
    questions = st.session_state.quiz_questions
    current_q = st.session_state.current_question
    lang = st.session_state.language
    
    # Show quiz title
    quiz_data = get_quiz_data()
    quiz_title_en = quiz_data[st.session_state.selected_quiz]["title"]["english"]
    st.markdown(f"## {quiz_title_en}")
    st.info(f"Language: **{'English' if lang == 'english' else 'Telugu'}**")
    
    # Progress bar
    progress = min((current_q + 1) / len(questions), 1.0)
    st.progress(progress)
    st.write(f"Question {current_q + 1} of {len(questions)}")
    
    if current_q < len(questions):
        _, _, question = questions[current_q]
        
        # Compact classic question display
        difficulty = question.get('difficulty', 'medium')
        difficulty_colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
        difficulty_emoji = difficulty_colors.get(difficulty, '🟡')
        
        # Clean question display for classic mode
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; 
                    margin: 1rem 0; border-left: 4px solid #6c5ce7;">
            <h3 style="color: #2d3436; margin-bottom: 1rem; font-size: 1.3rem;">
                📝 {question['question'][lang]}
            </h3>
            <p style="color: #636e72; margin: 0; font-size: 0.9rem;">
                <strong>Difficulty:</strong> {difficulty_emoji} {difficulty.title()}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean options display
        options = question["options"][lang]
        
        with st.form(key=f"question_form_{current_q}"):
            st.markdown("### 🤔 Choose your answer:")
            selected_option = st.radio(
                "Select one option:",
                options,
                key=f"q_{current_q}",
                index=None,
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                submit_answer = st.form_submit_button("Submit Answer", use_container_width=True)
            
            with col2:
                if st.form_submit_button("Skip Question", use_container_width=True):
                    record_answer(question, options, "Skipped", False, lang)
                    st.session_state.current_question += 1
                    st.rerun()
            
            with col3:
                if st.form_submit_button("Restart Quiz", use_container_width=True):
                    restart_quiz()
                    st.rerun()
            
            if submit_answer and selected_option is not None:
                selected_index = options.index(selected_option)
                is_correct = selected_index == question["correct"]
                
                record_answer(question, options, selected_option, is_correct, lang)
                
                if is_correct:
                    st.session_state.score += 1
                
                st.session_state.current_question += 1
                st.rerun()
            elif submit_answer and selected_option is None:
                st.warning("Please select an answer before submitting!")
    
    else:
        show_classic_quiz_results()

def record_answer(question, options, selected, is_correct, lang):
    """Record quiz answer"""
    st.session_state.answers.append({
        "question": question["question"][lang],
        "selected": selected,
        "correct": options[question["correct"]],
        "is_correct": is_correct,
        "explanation": question["explanation"][lang]
    })

def restart_quiz():
    """Restart the current quiz"""
    for key in ['quiz_started', 'selected_quiz', 'current_question', 'score', 'answers', 'quiz_questions', 'questions_used', 'quiz_start_time']:
        if key in st.session_state:
            del st.session_state[key]

def show_enhanced_quiz_results():
    """Enhanced quiz results with achievements and certificates"""
    profile = st.session_state.user_profile
    questions = st.session_state.quiz_questions
    score = st.session_state.score
    total = len(questions)
    percentage = round((score/total)*100, 2)
    
    # Calculate quiz time
    quiz_time = int(time.time() - st.session_state.quiz_start_time)
    
    # Celebration effects
    if percentage >= 80:
        st.balloons()
    elif percentage >= 60:
        st.snow()
    
    # Update user profile
    profile.total_quizzes += 1
    profile.total_score += score
    
    # Calculate XP earned
    difficulty_bonus = 1.0
    xp_earned = get_xp_for_quiz(score, total, difficulty_bonus)
    profile.xp_points += xp_earned
    
    # Update level
    old_level = profile.level
    profile.level = calculate_level(profile.xp_points)
    level_up = profile.level > old_level
    
    # Update streak
    today = datetime.datetime.now().date()
    if profile.last_quiz_date:
        last_date = datetime.datetime.fromisoformat(profile.last_quiz_date).date()
        if (today - last_date).days == 1:
            profile.streak_days += 1
        elif (today - last_date).days > 1:
            profile.streak_days = 1
    else:
        profile.streak_days = 1
    
    profile.last_quiz_date = datetime.datetime.now().isoformat()
    
    # Check for achievements
    quiz_result = {
        'score': score,
        'total': total,
        'percentage': percentage,
        'quiz_type': st.session_state.selected_quiz,
        'language': st.session_state.selected_language
    }
    
    new_achievements = AchievementSystem.check_achievements(profile, quiz_result)
    
    # Save updated profile
    update_user_profile(profile)
    
    # Save score to leaderboard
    timestamp = datetime.datetime.now().isoformat()
    save_score(profile.username, st.session_state.selected_quiz, score, total, 
              st.session_state.selected_language, timestamp, st.session_state.questions_used)
    
    # Enhanced results display
    st.markdown(f'''
    <div class="score-card">
        <h2>🎉 Quiz Completed!</h2>
        <h3>Score: {score}/{total} ({percentage}%)</h3>
        <p>Amazing work, {profile.username}!</p>
        <p style="font-size: 1rem; margin-top: 1rem;">
            ⏱️ Time: {quiz_time//60}m {quiz_time%60}s • 
            ⭐ XP Earned: +{xp_earned} • 
            🔥 Streak: {profile.streak_days} days
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Level up notification
    if level_up:
        st.markdown(f'''
        <div class="achievement-card">
            <h2>🎊 LEVEL UP! 🎊</h2>
            <h3>You reached Level {profile.level}!</h3>
            <p>Keep up the excellent work!</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # New achievements
    if new_achievements:
        st.markdown("### 🏆 New Achievements Unlocked!")
        cols = st.columns(min(3, len(new_achievements)))
        for i, achievement_id in enumerate(new_achievements):
            achievement = AchievementSystem.ACHIEVEMENTS[achievement_id]
            with cols[i % len(cols)]:
                st.markdown(f'''
                <div class="achievement-card">
                    <h4>{achievement['name']}</h4>
                    <p>{achievement['description']}</p>
                    <p><strong>+{achievement['xp']} XP</strong></p>
                </div>
                ''', unsafe_allow_html=True)
    
    # Performance feedback
    if percentage >= 80:
        st.markdown('''
        <div class="performance-excellent">
            <h4>🌟 Outstanding Performance!</h4>
            <p>You have exceptional knowledge of our ancient epics!</p>
        </div>
        ''', unsafe_allow_html=True)
    elif percentage >= 60:
        st.markdown('''
        <div class="performance-good">
            <h4>👍 Great Job!</h4>
            <p>You have a solid foundation in our cultural heritage!</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="performance-improve">
            <h4>📚 Keep Learning!</h4>
            <p>Every journey begins with a single step. Keep exploring!</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Certificate for high scores
    if percentage >= 70:
        st.markdown("### 🎓 Certificate of Achievement")
        certificate_html = generate_certificate(
            profile.username, 
            st.session_state.selected_quiz, 
            score, 
            total, 
            percentage
        )
        st.markdown(certificate_html, unsafe_allow_html=True)
    
    # Detailed results
    show_detailed_results()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Take Another Quiz", use_container_width=True):
            restart_quiz()
            st.rerun()
    
    with col2:
        if st.button("👤 View Profile", use_container_width=True):
            st.session_state.nav_radio = "👤 Profile"
            st.rerun()

def show_classic_quiz_results():
    """Classic quiz results display"""
    score = st.session_state.score
    total = len(st.session_state.quiz_questions)
    percentage = round((score/total)*100, 2)
    
    # Save score
    timestamp = datetime.datetime.now().isoformat()
    save_score(st.session_state.user_name, st.session_state.selected_quiz, 
              score, total, st.session_state.language, timestamp, 
              st.session_state.questions_used)
    
    # Display results
    st.balloons()
    
    st.markdown(f'''
    <div class="score-card">
        <h2>🎉 Quiz Completed!</h2>
        <h3>Score: {score}/{total} ({percentage}%)</h3>
        <p>Great job, {st.session_state.user_name}!</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Performance message
    if percentage >= 80:
        st.markdown('''
        <div class="performance-excellent">
            <h4>🌟 Excellent! You have great knowledge of our epics!</h4>
        </div>
        ''', unsafe_allow_html=True)
    elif percentage >= 60:
        st.markdown('''
        <div class="performance-good">
            <h4>👍 Good job! Keep learning more about our heritage!</h4>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="performance-improve">
            <h4>📚 Keep studying! Our epics have so much wisdom to offer!</h4>
        </div>
        ''', unsafe_allow_html=True)
    
    # Detailed results
    show_detailed_results()
    
    # Restart button
    if st.button("Take Another Quiz", use_container_width=True):
        restart_quiz()
        st.rerun()

def show_detailed_results():
    """Show detailed question-by-question results"""
    st.subheader("📋 Detailed Results")
    
    # Statistics
    score = st.session_state.score
    total = len(st.session_state.answers)
    correct_answers = score
    incorrect_answers = total - score
    percentage = round((score/total)*100, 2)
    
    st.markdown(f'''
    <div class="stats-container">
        <h3 style="text-align: center; margin-bottom: 1rem;">📊 Quiz Statistics</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div class="stats-item">
                <span class="stats-number">✅ {correct_answers}</span>
                <span class="stats-label">Correct</span>
            </div>
            <div class="stats-item">
                <span class="stats-number">❌ {incorrect_answers}</span>
                <span class="stats-label">Incorrect</span>
            </div>
            <div class="stats-item">
                <span class="stats-number">🎯 {percentage}%</span>
                <span class="stats-label">Accuracy</span>
            </div>
            <div class="stats-item">
                <span class="stats-number">📚 {total}</span>
                <span class="stats-label">Total Questions</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Download results
    col1, col2 = st.columns([3, 1])
    with col2:
        results_data = []
        for i, answer in enumerate(st.session_state.answers):
            results_data.append({
                'Question_No': i + 1,
                'Question': answer['question'],
                'Your_Answer': answer['selected'],
                'Correct_Answer': answer['correct'],
                'Is_Correct': 'Yes' if answer['is_correct'] else 'No',
                'Explanation': answer['explanation']
            })
        
        results_df = pd.DataFrame(results_data)
        
        # Add summary info
        user_name = st.session_state.user_profile.username if st.session_state.enhanced_mode else st.session_state.user_name
        language = st.session_state.selected_language if st.session_state.enhanced_mode else st.session_state.language
        
        summary_info = f"""Quiz Summary:
Name: {user_name}
Quiz: {st.session_state.selected_quiz.title()}
Language: {language.title()}
Score: {score}/{total} ({percentage}%)
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
        
        csv_content = summary_info + results_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Results",
            data=csv_content,
            file_name=f"quiz_results_{user_name}_{st.session_state.selected_quiz}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col1:
        st.write(f"**Questions Answered:** {len(st.session_state.answers)}")
    
    # Question-by-question breakdown
    for i, answer in enumerate(st.session_state.answers):
        with st.expander(f"Question {i+1}: {'✅' if answer['is_correct'] else '❌'}"):
            st.write(f"**Question:** {answer['question']}")
            st.write(f"**Your Answer:** {answer['selected']}")
            st.write(f"**Correct Answer:** {answer['correct']}")
            st.write(f"**Explanation:** {answer['explanation']}")

def display_enhanced_leaderboard():
    """Enhanced leaderboard with user profiles"""
    scores = load_scores()
    if not scores:
        st.info("No scores yet! Take a quiz to see the leaderboard.")
        return
    
    df = pd.DataFrame(scores)
    df_best = df.loc[df.groupby(['name', 'quiz_type'])['percentage'].idxmax()]
    df_best = df_best.sort_values(['percentage', 'timestamp'], ascending=[False, False])
    
    st.subheader("🏆 Epic Quiz Champions")
    
    # Top 3 podium
    if len(df_best) >= 3:
        st.markdown("### 🥇🥈🥉 Top 3 Champions")
        cols = st.columns(3)
        
        for i, (_, row) in enumerate(df_best.head(3).iterrows()):
            medals = ['🥇', '🥈', '🥉']
            with cols[i]:
                st.markdown(f"""
                <div class="achievement-card">
                    <h2>{medals[i]}</h2>
                    <h3>{row['name']}</h3>
                    <p>{row['quiz_type'].title()}</p>
                    <h4>{row['percentage']}%</h4>
                </div>
                """, unsafe_allow_html=True)
    
    # Full leaderboard
    st.markdown("### 📊 Full Leaderboard")
    if len(df_best) > 0:
        display_df = df_best.head(20)[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']]
        display_df['Quiz'] = display_df['quiz_type'].str.title()
        display_df['Score'] = display_df['score'].astype(str) + '/' + display_df['total'].astype(str) + ' (' + display_df['percentage'].astype(str) + '%)'
        display_df['Date'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d')
        
        final_df = display_df[['name', 'Quiz', 'Score', 'language', 'Date']].rename(columns={
            'name': 'Player',
            'language': 'Language',
            'Date': 'Date'
        })
        
        st.dataframe(final_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()