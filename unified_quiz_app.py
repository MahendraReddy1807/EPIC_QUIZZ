import streamlit as st
import json
import datetime
import pandas as pd
import os
import random
import hashlib
import time
from typing import Dict, List, Optional

# Initialize session state for unified app
def init_session_state():
    """Initialize session state variables for unified app"""
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = None  # None, 'simple', 'enhanced'
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

# Enhanced Mode Classes (from enhanced_quiz_app.py)
class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.created_date = datetime.datetime.now().isoformat()
        self.total_quizzes = 0
        self.total_score = 0
        self.achievements = []
        self.streak_days = 0
        self.last_quiz_date = None
        self.xp_points = 0
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
        
        if profile.total_quizzes == 1 and 'first_quiz' not in profile.achievements:
            new_achievements.append('first_quiz')
        if quiz_result['percentage'] == 100 and 'perfect_score' not in profile.achievements:
            new_achievements.append('perfect_score')
        if quiz_result['percentage'] >= 80 and 'high_scorer' not in profile.achievements:
            new_achievements.append('high_scorer')
        if profile.total_quizzes >= 10 and 'quiz_master' not in profile.achievements:
            new_achievements.append('quiz_master')
        if profile.streak_days >= 3 and 'streak_3' not in profile.achievements:
            new_achievements.append('streak_3')
        if profile.streak_days >= 7 and 'streak_7' not in profile.achievements:
            new_achievements.append('streak_7')
        if profile.level >= 5 and 'level_5' not in profile.achievements:
            new_achievements.append('level_5')
        if profile.level >= 10 and 'level_10' not in profile.achievements:
            new_achievements.append('level_10')
        
        for achievement in new_achievements:
            profile.achievements.append(achievement)
            profile.xp_points += AchievementSystem.ACHIEVEMENTS[achievement]['xp']
        
        return new_achievements

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
        return None
    
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

# Utility Functions
def calculate_level(xp_points: int) -> int:
    """Calculate user level based on XP points"""
    if xp_points < 100: return 1
    elif xp_points < 300: return 2
    elif xp_points < 600: return 3
    elif xp_points < 1000: return 4
    elif xp_points < 1500: return 5
    elif xp_points < 2100: return 6
    elif xp_points < 2800: return 7
    elif xp_points < 3600: return 8
    elif xp_points < 4500: return 9
    else: return min(10 + (xp_points - 4500) // 1000, 50)

def get_xp_for_quiz(score: int, total: int, difficulty_bonus: float = 1.0) -> int:
    """Calculate XP earned for a quiz"""
    base_xp = (score / total) * 100
    return int(base_xp * difficulty_bonus)

# Theme System
def get_theme_css(theme_name: str, font_size: str, accessibility_mode: bool, is_enhanced: bool = True) -> str:
    """Generate CSS for different themes"""
    
    font_sizes = {
        'small': {'base': '14px', 'h1': '1.8rem', 'h2': '1.5rem', 'h3': '1.3rem'},
        'medium': {'base': '16px', 'h1': '2.2rem', 'h2': '1.8rem', 'h3': '1.5rem'},
        'large': {'base': '18px', 'h1': '2.5rem', 'h2': '2rem', 'h3': '1.7rem'},
        'extra-large': {'base': '20px', 'h1': '2.8rem', 'h2': '2.3rem', 'h3': '2rem'}
    }
    
    fs = font_sizes[font_size]
    
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
    
    if accessibility_mode:
        theme['text'] = '#000000'
        theme['background'] = '#ffffff'
        theme['surface'] = '#f0f0f0'
    
    # Enhanced CSS for enhanced mode, simpler for simple mode
    enhanced_css = f"""
    /* Enhanced animations and effects */
    @keyframes slideInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes bounceIn {{
        0% {{ opacity: 0; transform: scale(0.3); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
        70% {{ transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
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
    
    .profile-card {{
        background: linear-gradient(135deg, {theme['surface']} 0%, {theme['background']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid {theme['primary']};
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    
    .xp-progress {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        height: 20px;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: progressFill 1s ease-out;
    }}
    
    @keyframes progressFill {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
    }}
    """ if is_enhanced else ""
    
    return f"""
    <style>
    .stApp {{
        background-color: {theme['background']};
        color: {theme['text']};
        font-size: {fs['base']};
    }}
    
    h1 {{ font-size: {fs['h1']} !important; color: {theme['primary']} !important; }}
    h2 {{ font-size: {fs['h2']} !important; color: {theme['secondary']} !important; }}
    h3 {{ font-size: {fs['h3']} !important; color: {theme['text']} !important; }}
    
    .score-card {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 1.5rem 0;
        {'animation: slideInUp 0.6s ease-out;' if is_enhanced else ''}
    }}
    
    .score-card h2 {{
        margin: 0;
        font-size: 2.8rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        {'animation: pulse 2s infinite;' if is_enhanced else ''}
    }}
    
    .score-card h3 {{
        margin: 0.5rem 0;
        font-size: 2.2rem !important;
        color: #FFD700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
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
        {'transition: transform 0.3s ease;' if is_enhanced else ''}
    }}
    
    {'.stats-item:hover { transform: scale(1.05); }' if is_enhanced else ''}
    
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
    
    .performance-excellent {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    
    .performance-good {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    
    .performance-improve {{
        background: linear-gradient(135deg, {theme['accent']} 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: {fs['base']};
        font-weight: 600;
        {'transition: all 0.3s ease;' if is_enhanced else ''}
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    {'.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }' if is_enhanced else ''}
    
    .stProgress > div > div {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        height: 15px;
        border-radius: 10px;
    }}
    
    @media (max-width: 768px) {{
        .score-card {{ padding: 1.5rem; margin: 1rem 0; }}
        .score-card h2 {{ font-size: 2.2rem !important; }}
        .score-card h3 {{ font-size: 1.8rem !important; }}
        .stats-container {{ padding: 1.5rem; }}
        .stats-item {{ margin: 0.5rem; }}
        .stats-number {{ font-size: 2rem; }}
    }}
    
    .stButton > button:focus,
    .stRadio > div:focus-within {{
        outline: 3px solid {theme['accent']};
        outline-offset: 2px;
    }}
    
    {enhanced_css}
    </style>
    """

# Core Quiz Functions (from original quiz_app.py)
@st.cache_data
def load_questions():
    """Load and cache questions for better performance"""
    from fast_questions import get_mahabharata_questions, get_ramayana_questions
    return {
        "mahabharata": get_mahabharata_questions(),
        "ramayana": get_ramayana_questions()
    }

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
    load_scores.clear()

def get_user_history(name, quiz_type):
    """Get user's quiz history to avoid repeated questions"""
    scores = load_scores()
    user_scores = [s for s in scores if s["name"].lower() == name.lower() and s["quiz_type"] == quiz_type]
    used_questions = []
    for score in user_scores:
        if "questions_used" in score:
            used_questions.extend(score["questions_used"])
    return list(set(used_questions))

@st.cache_data
def get_random_questions(quiz_type, num_questions=20, exclude_questions=None):
    """Get random questions with difficulty distribution"""
    if exclude_questions is None:
        exclude_questions = []
    
    quiz_data = get_quiz_data()
    all_questions = quiz_data[quiz_type]["questions"]
    
    easy_questions = []
    medium_questions = []
    hard_questions = []
    
    for i, q in enumerate(all_questions):
        question_id = hashlib.md5(q["question"]["english"].encode()).hexdigest()[:8]
        difficulty = q.get("difficulty", "medium")
        
        if question_id not in exclude_questions:
            if difficulty == "easy":
                easy_questions.append((i, question_id, q))
            elif difficulty == "medium":
                medium_questions.append((i, question_id, q))
            elif difficulty == "hard":
                hard_questions.append((i, question_id, q))
    
    selected_questions = []
    
    if len(easy_questions) >= 6:
        selected_questions.extend(random.sample(easy_questions, 6))
    else:
        selected_questions.extend(easy_questions)
    
    available_medium = [q for q in medium_questions if q not in selected_questions]
    if len(available_medium) >= 8:
        selected_questions.extend(random.sample(available_medium, 8))
    else:
        selected_questions.extend(available_medium)
    
    available_hard = [q for q in hard_questions if q not in selected_questions]
    if len(available_hard) >= 6:
        selected_questions.extend(random.sample(available_hard, 6))
    else:
        selected_questions.extend(available_hard)
    
    while len(selected_questions) < num_questions:
        all_available = [q for q in easy_questions + medium_questions + hard_questions if q not in selected_questions]
        if all_available:
            selected_questions.extend(random.sample(all_available, min(num_questions - len(selected_questions), len(all_available))))
        else:
            break
    
    random.shuffle(selected_questions)
    return selected_questions[:num_questions]

# Continue in next part...