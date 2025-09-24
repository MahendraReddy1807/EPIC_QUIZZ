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
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

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
        'level_10': {'name': '👑 Master', 'description': 'Reach Level 10', 'xp': 1000},
        'admin_access': {'name': '👑 Administrator', 'description': 'System Administrator Access', 'xp': 0}
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

def get_xp_needed_for_next_level(current_level: int) -> int:
    """Get XP needed to reach the next level"""
    level_thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
    if current_level < len(level_thresholds):
        return level_thresholds[current_level]
    else:
        return 4500 + (current_level - 9) * 1000

def get_xp_progress_percentage(xp_points: int, current_level: int) -> float:
    """Calculate XP progress percentage for current level"""
    if current_level == 1:
        current_level_start = 0
        next_level_threshold = 100
    elif current_level <= 9:
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
        current_level_start = level_thresholds[current_level - 1]
        next_level_threshold = level_thresholds[current_level]
    else:
        current_level_start = 4500 + (current_level - 10) * 1000
        next_level_threshold = 4500 + (current_level - 9) * 1000
    
    progress = ((xp_points - current_level_start) / (next_level_threshold - current_level_start)) * 100
    return min(max(progress, 0), 100)

def get_xp_for_quiz(score: int, total: int, difficulty_bonus: float = 1.0) -> int:
    """Calculate XP earned for a quiz"""
    base_xp = (score / total) * 100
    return int(base_xp * difficulty_bonus)

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
    /* Base styling */
    .stApp {{
        background-color: {theme['background']};
        color: {theme['text']};
        font-size: {fs['base']};
    }}
    
    /* Headers */
    h1 {{ font-size: {fs['h1']} !important; color: {theme['primary']} !important; }}
    h2 {{ font-size: {fs['h2']} !important; color: {theme['secondary']} !important; }}
    h3 {{ font-size: {fs['h3']} !important; color: {theme['text']} !important; }}
    
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
        transform: translateY(0);
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
    
    /* XP Progress bar */
    .xp-progress {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        height: 20px;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: progressFill 1s ease-out;
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
    
    /* Radio buttons */
    .stRadio > div {{
        background: {theme['surface']};
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }}
    
    .stRadio > div:hover {{
        border-color: {theme['primary']};
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* Progress bar */
    .stProgress > div > div {{
        background: linear-gradient(90deg, {theme['primary']} 0%, {theme['accent']} 100%);
        height: 15px;
        border-radius: 10px;
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: linear-gradient(180deg, {theme['surface']} 0%, {theme['background']} 100%);
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
    
    @keyframes progressFill {{
        from {{
            width: 0%;
        }}
        to {{
            width: 100%;
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
    
    /* High contrast mode */
    {'.high-contrast *' if accessibility_mode else ''} {{
        border: 1px solid #000000 !important;
        background: #ffffff !important;
        color: #000000 !important;
    }}
    </style>
    """

# Certificate Generation
def generate_certificate(username: str, quiz_type: str, score: int, total: int, percentage: float) -> str:
    """Generate a certificate for the user"""
    certificate_html = f"""
    <div style="
        width: 800px;
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
        <h1 style="font-size: 3rem; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🏆 CERTIFICATE OF ACHIEVEMENT 🏆
        </h1>
        
        <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0;">
            <h2 style="font-size: 1.5rem; margin-bottom: 20px;">This is to certify that</h2>
            
            <h1 style="font-size: 2.5rem; color: #FFD700; margin: 20px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                {username.upper()}
            </h1>
            
            <h2 style="font-size: 1.3rem; margin: 20px 0;">
                has successfully completed the<br>
                <strong style="font-size: 1.8rem; color: #FFD700;">{quiz_type.title()} Quiz</strong>
            </h2>
            
            <h2 style="font-size: 1.5rem; margin: 20px 0;">
                with a score of <strong style="color: #FFD700;">{score}/{total} ({percentage}%)</strong>
            </h2>
            
            <p style="font-size: 1rem; margin-top: 30px; opacity: 0.9;">
                Demonstrating knowledge of ancient Indian epics and cultural heritage
            </p>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-top: 40px; font-size: 0.9rem;">
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

# Load original functions (simplified versions)
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
        if "questions_used" in score and isinstance(score["questions_used"], list):
            used_questions.extend(score["questions_used"])
    
    # Remove duplicates and return
    unique_used = list(set(used_questions))
    
    # Limit history to prevent running out of questions (keep last 100 questions)
    if len(unique_used) > 100:
        # Keep only the most recent questions by sorting scores by timestamp
        user_scores.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        recent_used = []
        for score in user_scores[:5]:  # Last 5 quizzes
            if "questions_used" in score and isinstance(score["questions_used"], list):
                recent_used.extend(score["questions_used"])
        unique_used = list(set(recent_used))
    
    return unique_used

def get_random_questions(quiz_type, num_questions=20, exclude_questions=None):
    """Get random questions with difficulty distribution - No caching to ensure randomness"""
    if exclude_questions is None:
        exclude_questions = []
    
    quiz_data = get_quiz_data()
    all_questions = quiz_data[quiz_type]["questions"]
    
    # Create unique question IDs using both question text and index
    available_questions = []
    for i, q in enumerate(all_questions):
        # Create more unique ID using question text + index + first option
        question_text = q["question"]["english"]
        first_option = q["options"]["english"][0] if q["options"]["english"] else ""
        unique_content = f"{i}_{question_text}_{first_option}"
        question_id = hashlib.md5(unique_content.encode()).hexdigest()[:12]
        
        # Only include if not in excluded questions
        if question_id not in exclude_questions:
            difficulty = q.get("difficulty", "medium")
            available_questions.append((i, question_id, q, difficulty))
    
    # If we don't have enough unique questions, reset the exclusion list partially
    if len(available_questions) < num_questions:
        st.warning(f"Only {len(available_questions)} unique questions available. Including some previously seen questions.")
        # Include all questions but prioritize unseen ones
        all_with_ids = []
        for i, q in enumerate(all_questions):
            question_text = q["question"]["english"]
            first_option = q["options"]["english"][0] if q["options"]["english"] else ""
            unique_content = f"{i}_{question_text}_{first_option}"
            question_id = hashlib.md5(unique_content.encode()).hexdigest()[:12]
            difficulty = q.get("difficulty", "medium")
            priority = 0 if question_id in exclude_questions else 1  # Prioritize unseen
            all_with_ids.append((i, question_id, q, difficulty, priority))
        
        # Sort by priority (unseen first) then shuffle within priority groups
        all_with_ids.sort(key=lambda x: x[4], reverse=True)
        available_questions = [(i, qid, q, diff) for i, qid, q, diff, _ in all_with_ids]
    
    # Separate by difficulty
    easy_questions = [q for q in available_questions if q[3] == "easy"]
    medium_questions = [q for q in available_questions if q[3] == "medium"]
    hard_questions = [q for q in available_questions if q[3] == "hard"]
    
    # If no difficulty specified, treat as medium
    if not easy_questions and not medium_questions and not hard_questions:
        medium_questions = available_questions
    
    selected_questions = []
    
    # Target distribution: 6 easy, 8 medium, 6 hard (adjustable based on availability)
    easy_target = min(6, len(easy_questions))
    medium_target = min(8, len(medium_questions))
    hard_target = min(6, len(hard_questions))
    
    # Select questions by difficulty
    if easy_questions and easy_target > 0:
        selected_questions.extend(random.sample(easy_questions, easy_target))
    
    if medium_questions and medium_target > 0:
        # Avoid duplicates from easy selection
        available_medium = [q for q in medium_questions if q not in selected_questions]
        if available_medium:
            medium_target = min(medium_target, len(available_medium))
            selected_questions.extend(random.sample(available_medium, medium_target))
    
    if hard_questions and hard_target > 0:
        # Avoid duplicates from previous selections
        available_hard = [q for q in hard_questions if q not in selected_questions]
        if available_hard:
            hard_target = min(hard_target, len(available_hard))
            selected_questions.extend(random.sample(available_hard, hard_target))
    
    # Fill remaining slots with any available questions
    while len(selected_questions) < num_questions and len(selected_questions) < len(available_questions):
        remaining_questions = [q for q in available_questions if q not in selected_questions]
        if remaining_questions:
            additional_needed = min(num_questions - len(selected_questions), len(remaining_questions))
            selected_questions.extend(random.sample(remaining_questions, additional_needed))
        else:
            break
    
    # Final shuffle and return
    random.shuffle(selected_questions)
    final_questions = selected_questions[:num_questions]
    
    # Debug info
    difficulties = [q[3] for q in final_questions]
    easy_count = difficulties.count("easy")
    medium_count = difficulties.count("medium") 
    hard_count = difficulties.count("hard")
    
    return final_questions

# Continue in next part due to length...
# User Authentication UI
def show_login_page():
    """Display login/registration page"""
    # Create centered header with proper spacing from toolbar
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #667eea; margin-bottom: 0.5rem;">📚 Epic Quiz App</h1>
        <p style="color: #6c757d; font-size: 1.1rem;">Please login or create an account to track your progress and earn achievements!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Register", "👑 Admin"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        
        if st.button("Login", key="login_btn", use_container_width=True):
            if username:
                profile = get_user_profile(username)
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
        
        if st.button("Create Account", key="register_btn", use_container_width=True):
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
    
    with tab3:
        st.subheader("🔐 Admin Access")
        admin_username = st.text_input("Admin Username", key="admin_username", placeholder="Enter admin username")
        admin_password = st.text_input("Admin Password", key="admin_password", type="password", placeholder="Enter admin password")
        
        if st.button("Admin Login", key="admin_login_btn", use_container_width=True):
            if admin_username == "Mahi07" and admin_password == "1477":
                st.session_state.admin_logged_in = True
                st.session_state.user_profile = create_admin_profile()
                st.success("Welcome Admin! 👑")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid admin credentials!")
        
        st.info("🔒 Admin access is restricted to authorized personnel only.")

# Admin Functions
def create_admin_profile():
    """Create admin profile"""
    admin = UserProfile("Admin_Mahi07")
    admin.level = 999
    admin.xp_points = 999999
    admin.total_quizzes = 0
    admin.achievements = ["admin_access"]
    admin.streak_days = 365
    return admin

def delete_user_from_leaderboard(username):
    """Delete user from leaderboard and scores"""
    scores = load_scores()
    original_count = len(scores)
    scores = [s for s in scores if s.get("name", "").lower() != username.lower()]
    
    if len(scores) < original_count:
        with open("quiz_scores.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        load_scores.clear()
        return True
    return False

def delete_user_profile(username):
    """Delete user profile completely"""
    users = load_users()
    deleted = False
    
    # Find and delete user (case insensitive)
    for stored_username in list(users.keys()):
        if stored_username.lower() == username.lower():
            del users[stored_username]
            deleted = True
            break
    
    if deleted:
        save_users(users)
        # Also delete from leaderboard
        delete_user_from_leaderboard(username)
        return True
    return False

def get_all_users_data():
    """Get comprehensive data for all users"""
    users = load_users()
    scores = load_scores()
    
    user_data = []
    for username, profile_data in users.items():
        profile = UserProfile.from_dict(profile_data)
        user_scores = [s for s in scores if s.get("name", "").lower() == username.lower()]
        
        # Calculate stats
        total_attempts = len(user_scores)
        avg_score = sum(s.get("percentage", 0) for s in user_scores) / total_attempts if total_attempts > 0 else 0
        best_score = max((s.get("percentage", 0) for s in user_scores), default=0)
        last_activity = max((s.get("timestamp", "") for s in user_scores), default="Never")
        
        user_data.append({
            "username": username,
            "level": profile.level,
            "xp_points": profile.xp_points,
            "total_quizzes": profile.total_quizzes,
            "achievements": len(profile.achievements),
            "streak_days": profile.streak_days,
            "total_attempts": total_attempts,
            "avg_score": round(avg_score, 1),
            "best_score": best_score,
            "last_activity": last_activity,
            "created_date": profile.created_date
        })
    
    return user_data

def show_admin_dashboard():
    """Display comprehensive admin dashboard"""
    try:
        st.markdown("# 👑 Admin Dashboard")
        st.markdown("Welcome to the admin control panel!")
        st.markdown("---")
        
        # Admin navigation
        admin_tab = st.selectbox(
            "Select Admin Function",
            ["📊 Overview", "👥 User Management", "🏆 Leaderboard Management", "📈 Analytics", "🔧 System Tools"],
            key="admin_nav"
        )
        
        if admin_tab == "📊 Overview":
            show_admin_overview()
        elif admin_tab == "👥 User Management":
            show_user_management()
        elif admin_tab == "🏆 Leaderboard Management":
            show_leaderboard_management()
        elif admin_tab == "� AnaTlytics":
            show_admin_analytics()
        elif admin_tab == "🔧 System Tools":
            show_system_tools()
            
    except Exception as e:
        st.error(f"Error in admin dashboard: {e}")
        st.error("Please check the logs for more details")

def show_admin_overview():
    """Show admin overview dashboard"""
    st.subheader("📊 System Overview")
    
    # Get system stats
    users = load_users()
    scores = load_scores()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(users))
    
    with col2:
        st.metric("Total Quiz Attempts", len(scores))
    
    with col3:
        active_users = len(set(s.get("name", "") for s in scores if s.get("timestamp", "").startswith("2024")))
        st.metric("Active Users (2024)", active_users)
    
    with col4:
        avg_score = sum(s.get("percentage", 0) for s in scores) / len(scores) if scores else 0
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    if scores:
        recent_scores = sorted(scores, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
        for score in recent_scores:
            st.write(f"**{score.get('name', 'Unknown')}** - {score.get('quiz_type', 'Unknown').title()} Quiz - {score.get('percentage', 0)}% - {score.get('timestamp', 'Unknown time')}")
    else:
        st.info("No recent activity")

def show_user_management():
    """Show user management interface"""
    st.subheader("👥 User Management")
    
    # Get all users data
    user_data = get_all_users_data()
    
    if not user_data:
        st.info("No users found")
        return
    
    # Display users table
    df = pd.DataFrame(user_data)
    st.dataframe(df, use_container_width=True)
    
    # User actions
    st.subheader("🔧 User Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### View User Profile")
        selected_user = st.selectbox("Select User", [u["username"] for u in user_data], key="view_user")
        
        if st.button("View Profile", key="view_profile_btn"):
            user_profile_data = next((u for u in user_data if u["username"] == selected_user), None)
            if user_profile_data:
                st.json(user_profile_data)
    
    with col2:
        st.markdown("#### Delete User")
        delete_user = st.selectbox("Select User to Delete", [u["username"] for u in user_data], key="delete_user")
        
        if st.button("🗑️ Delete User", key="delete_user_btn", type="secondary"):
            if delete_user_profile(delete_user):
                st.success(f"User '{delete_user}' deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete user")

def show_leaderboard_management():
    """Show leaderboard management interface"""
    st.subheader("🏆 Leaderboard Management")
    
    scores = load_scores()
    if not scores:
        st.info("No scores found")
        return
    
    # Display current leaderboard
    df = pd.DataFrame(scores)
    df_sorted = df.sort_values(['percentage', 'timestamp'], ascending=[False, False])
    
    st.markdown("#### Current Leaderboard")
    st.dataframe(df_sorted[['name', 'quiz_type', 'score', 'total', 'percentage', 'timestamp']], use_container_width=True)
    
    # Leaderboard actions
    st.subheader("🔧 Leaderboard Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Remove User from Leaderboard")
        users_in_leaderboard = list(set(s.get("name", "") for s in scores))
        selected_user = st.selectbox("Select User", users_in_leaderboard, key="remove_from_leaderboard")
        
        if st.button("Remove from Leaderboard", key="remove_leaderboard_btn", type="secondary"):
            if delete_user_from_leaderboard(selected_user):
                st.success(f"Removed '{selected_user}' from leaderboard!")
                st.rerun()
            else:
                st.error("Failed to remove user from leaderboard")
    
    with col2:
        st.markdown("#### Clear All Scores")
        if st.button("🗑️ Clear All Scores", key="clear_all_scores", type="secondary"):
            if st.button("⚠️ Confirm Clear All", key="confirm_clear_all"):
                with open("quiz_scores.json", "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
                load_scores.clear()
                st.success("All scores cleared!")
                st.rerun()

def show_admin_analytics():
    """Show detailed analytics"""
    st.subheader("📈 Analytics Dashboard")
    
    scores = load_scores()
    users = load_users()
    
    if not scores:
        st.info("No data available for analytics")
        return
    
    # Quiz type distribution
    st.markdown("#### Quiz Type Distribution")
    quiz_types = {}
    for score in scores:
        quiz_type = score.get("quiz_type", "Unknown")
        quiz_types[quiz_type] = quiz_types.get(quiz_type, 0) + 1
    
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(quiz_types)
    
    # Score distribution
    with col2:
        st.markdown("#### Score Distribution")
        score_ranges = {"0-20%": 0, "21-40%": 0, "41-60%": 0, "61-80%": 0, "81-100%": 0}
        for score in scores:
            percentage = score.get("percentage", 0)
            if percentage <= 20:
                score_ranges["0-20%"] += 1
            elif percentage <= 40:
                score_ranges["21-40%"] += 1
            elif percentage <= 60:
                score_ranges["41-60%"] += 1
            elif percentage <= 80:
                score_ranges["61-80%"] += 1
            else:
                score_ranges["81-100%"] += 1
        
        st.bar_chart(score_ranges)
    
    # Top performers
    st.markdown("#### Top Performers")
    df = pd.DataFrame(scores)
    if not df.empty:
        top_scores = df.nlargest(10, 'percentage')[['name', 'quiz_type', 'percentage', 'timestamp']]
        st.dataframe(top_scores, use_container_width=True)

def show_system_tools():
    """Show system management tools"""
    st.subheader("🔧 System Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Data Management")
        
        if st.button("📥 Export All Data", key="export_data"):
            users = load_users()
            scores = load_scores()
            
            export_data = {
                "users": users,
                "scores": scores,
                "export_timestamp": datetime.datetime.now().isoformat()
            }
            
            st.download_button(
                label="Download Data Export",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"quiz_app_data_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        if st.button("🔄 Reset All Data", key="reset_all_data", type="secondary"):
            if st.button("⚠️ Confirm Reset", key="confirm_reset_all"):
                # Reset all data files
                with open("quiz_scores.json", "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
                with open("user_profiles.json", "w", encoding="utf-8") as f:
                    json.dump({}, f, indent=2)
                load_scores.clear()
                load_users.clear()
                st.success("All data reset successfully!")
                st.rerun()
    
    with col2:
        st.markdown("#### System Information")
        
        users = load_users()
        scores = load_scores()
        
        st.info(f"""
        **System Status:**
        - Total Users: {len(users)}
        - Total Scores: {len(scores)}
        - Data Files: ✅ Accessible
        - Admin Access: ✅ Active
        """)
        
        if st.button("🧹 Clear Cache", key="clear_cache"):
            load_scores.clear()
            load_users.clear()
            st.success("Cache cleared!")

# User Profile Display
def show_user_profile():
    """Display user profile with stats and achievements"""
    profile = st.session_state.user_profile
    
    # Use Streamlit native components instead of HTML to avoid rendering issues
    st.subheader(f"👤 {profile.username}'s Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Level", profile.level)
        st.metric("XP Points", profile.xp_points)
    
    with col2:
        st.metric("Quizzes Completed", profile.total_quizzes)
        st.metric("Current Streak", f"{profile.streak_days} days 🔥")
    
    # Achievements section
    if profile.achievements:
        st.subheader("🏆 Your Achievements")
        cols = st.columns(3)
        for i, achievement_id in enumerate(profile.achievements):
            achievement = AchievementSystem.ACHIEVEMENTS[achievement_id]
            with cols[i % 3]:
                with st.container():
                    st.success(f"**{achievement['name']}**")
                    st.caption(achievement['description'])
                    st.caption(f"+{achievement['xp']} XP")
    else:
        st.info("Complete quizzes to earn achievements! 🎯")

# Settings Page
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
        
        st.info("🎨 Theme customization temporarily disabled for better consistency across platforms")
        
        st.info("📝 Font size customization temporarily disabled for better consistency")
    
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
        
        st.markdown("### 🔧 Debug Tools")
        if st.button("🔄 Reset Session State", help="Clear all session data except login"):
            reset_session_state()
        
        if st.button("�️ Cleare Quiz History", help="Reset question history to see all questions again"):
            clear_user_quiz_history(st.session_state.user_profile.username)
            st.success("Quiz history cleared! You'll now see fresh questions.")
        
        if st.button("📊 Show Session State", help="Display current session state for debugging"):
            st.json(dict(st.session_state))

# Enhanced Leaderboard (simplified version)
def display_enhanced_leaderboard():
    """Display enhanced leaderboard with user profiles"""
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

# Main Application
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
    
    # Apply consistent styling for both localhost and cloud
    st.markdown("""
    <style>
    /* Base app styling */
    .stApp {
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    /* Keep toolbar visible but move content down 3cm */
    .main .block-container {
        padding-top: 3cm !important;
        max-width: 1200px;
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Button consistency */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Form styling */
    .stForm {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 6px;
        margin: 0.25rem 0;
        border: 1px solid #dee2e6;
    }
    
    /* Sidebar consistency */
    .css-1d391kg {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Keep Streamlit toolbar visible */
    .stApp > header {
        display: block !important;
    }
    
    /* Ensure proper spacing from top toolbar */
    .stApp > div:first-child {
        margin-top: 0 !important;
    }
    
    /* Compact tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        margin-top: 0.5rem;
    }
    
    /* Compact form elements */
    .stTextInput > div > div > input {
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.user_profile:
        show_login_page()
        return
    
    # Main header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>📚 Epic Quiz App - Enhanced</h1>
        <p style="font-size: 1.2rem; opacity: 0.8;">Welcome back, {st.session_state.user_profile.username}! Level {st.session_state.user_profile.level} • {st.session_state.user_profile.xp_points} XP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_profile.username}")
        st.markdown(f"**Level:** {st.session_state.user_profile.level}")
        st.markdown(f"**XP:** {st.session_state.user_profile.xp_points}")
        st.markdown(f"**Streak:** {st.session_state.user_profile.streak_days} days 🔥")
        
        st.markdown("---")
        
        # Check if user is admin
        if hasattr(st.session_state, 'admin_logged_in') and st.session_state.admin_logged_in:
            nav_options = ["� AdPmin Dashboard", "🎯 Take Quiz", "👤 Profile", "🏆 Leaderboard", "⚙️ Settings", "📜 About", "🚪 Logout"]
        else:
            nav_options = ["🎯 Take Quiz", "👤 Profile", "🏆 Leaderboard", "⚙️ Settings", "📜 About", "🚪 Logout"]
        
        page = st.radio(
            "Navigation",
            nav_options,
            key="nav_radio"
        )
    
    # Page routing
    if page == "🚪 Logout":
        st.session_state.user_profile = None
        st.success("Logged out successfully!")
        time.sleep(1)
        st.rerun()
    
    elif page == "👑 Admin Dashboard":
        if hasattr(st.session_state, 'admin_logged_in') and st.session_state.admin_logged_in:
            show_admin_dashboard()
        else:
            st.error("❌ Admin access denied. Please login as admin first.")
            st.info("💡 Use the Admin tab in the login page to access admin features.")
    
    elif page == "👤 Profile":
        show_user_profile()
    
    elif page == "🏆 Leaderboard":
        display_enhanced_leaderboard()
    
    elif page == "⚙️ Settings":
        show_settings()
    
    elif page == "📜 About":
        st.subheader("About Epic Quiz App - Enhanced")
        st.markdown("""
        ### 🌟 New Features in Enhanced Version:
        
        **👤 User Profiles & Authentication**
        - Personal accounts with progress tracking
        - XP points and level system
        - Achievement badges
        
        **🎨 Theme Customization**
        - Multiple beautiful themes
        - Dark mode support
        - Adjustable font sizes
        
        **♿ Accessibility Features**
        - High contrast mode
        - Screen reader support
        - Keyboard navigation
        
        **🏆 Gamification**
        - XP points and levels
        - Achievement system
        - Daily streaks
        
        **📱 Mobile-First Design**
        - Responsive layout
        - Touch-friendly interface
        - Optimized for all devices
        
        **🎓 Certification System**
        - Downloadable certificates
        - Achievement recognition
        - Progress validation
        
        ### 📚 Educational Content:
        - 100+ authentic Mahabharata questions
        - 100+ authentic Ramayana questions
        - Bilingual support (English & Telugu)
        - Detailed explanations
        
        **Created with ❤️ to promote knowledge of our cultural heritage**
        """)
    
    elif page == "🎯 Take Quiz":
        show_quiz_interface()

def show_quiz_interface():
    """Enhanced quiz interface with gamification"""
    profile = st.session_state.user_profile
    
    # Show quiz interface if quiz is already started
    if hasattr(st.session_state, 'quiz_started') and st.session_state.quiz_started:
        # Check if quiz questions have the correct format
        if hasattr(st.session_state, 'quiz_questions') and st.session_state.quiz_questions:
            sample_question = st.session_state.quiz_questions[0]
            if len(sample_question) != 4:
                st.warning("Detected old quiz format. Restarting quiz with new format...")
                restart_quiz()
                st.rerun()
        show_quiz_questions()
        return
    
    # Initialize language selection state if not present
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = profile.preferred_language
    
    # Language selection (use preferred language as default)
    st.markdown("### 🌐 Select Quiz Language")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("English", key="enhanced_lang_en", use_container_width=True, 
                    type="primary" if st.session_state.selected_language == "english" else "secondary"):
            st.session_state.selected_language = "english"
            st.rerun()
    
    with col2:
        if st.button("తెలుగు (Telugu)", key="enhanced_lang_te", use_container_width=True,
                    type="primary" if st.session_state.selected_language == "telugu" else "secondary"):
            st.session_state.selected_language = "telugu"
            st.rerun()
    
    # Show selected language and quiz selection
    lang_display = "English" if st.session_state.selected_language == "english" else "Telugu"
    st.success(f"✅ Selected Language: {lang_display}")
    
    # Quiz selection
    st.subheader("📖 Choose Your Epic Adventure")
    st.info(f"Quiz will be displayed in: **{lang_display}**")
    st.info("📊 **Difficulty Distribution**: 6 Easy + 8 Medium + 6 Hard questions (20 total)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏹 Mahabharata Quiz", key="enhanced_maha", use_container_width=True):
            start_quiz("mahabharata")
    
    with col2:
        if st.button("🏺 Ramayana Quiz", key="enhanced_rama", use_container_width=True):
            start_quiz("ramayana")

def start_quiz(quiz_type):
    """Start a new quiz with enhanced features"""
    profile = st.session_state.user_profile
    
    # Get user's previous questions to avoid repetition
    used_questions = get_user_history(profile.username, quiz_type)
    selected_questions = get_random_questions(quiz_type, 20, used_questions)
    
    st.session_state.selected_quiz = quiz_type
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = selected_questions
    st.session_state.questions_used = [qid for _, qid, _, _ in selected_questions]
    st.session_state.quiz_start_time = time.time()
    st.rerun()

def show_quiz_questions():
    """Enhanced quiz questions interface"""
    profile = st.session_state.user_profile
    questions = st.session_state.quiz_questions
    current_q = st.session_state.current_question
    lang = st.session_state.selected_language
    
    # Debug: Check question format
    if questions and len(questions) > 0:
        sample_question = questions[0]
        if len(sample_question) != 4:
            st.error(f"Question format error: Expected 4 elements, got {len(sample_question)}. Restarting quiz...")
            restart_quiz()
            st.rerun()
    
    # Quiz header
    quiz_data = get_quiz_data()
    quiz_title = quiz_data[st.session_state.selected_quiz]["title"]["english"]
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <h2>🎯 {quiz_title}</h2>
        <p>Language: <strong>{'English' if lang == 'english' else 'Telugu'}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if quiz is complete first
    if current_q >= len(questions):
        show_quiz_results()
        return
    
    # Progress bar with animation
    progress = min((current_q + 1) / len(questions), 1.0) if len(questions) > 0 else 0.0
    st.progress(progress)
    st.markdown(f"**Question {current_q + 1} of {len(questions)}** • **Progress: {progress*100:.0f}%**")
    
    # Display current question
    if current_q < len(questions):
        _, _, question, _ = questions[current_q]
        
        # Question display with enhanced styling
        difficulty = question.get('difficulty', 'medium')
        difficulty_colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
        difficulty_emoji = difficulty_colors.get(difficulty, '🟡')
        
        st.markdown("---")
        st.markdown(f"### 📝 {question['question'][lang]}")
        st.markdown(f"**Difficulty**: {difficulty_emoji} {difficulty.title()}")
        
        # XP preview
        xp_preview = get_xp_for_quiz(1, 1, 1.0 + (0.5 if difficulty == 'hard' else 0.2 if difficulty == 'medium' else 0))
        st.markdown(f"**Potential XP**: +{xp_preview} points")
        st.markdown("---")
        
        # Options with enhanced styling
        options = question["options"][lang]
        
        with st.form(key=f"enhanced_question_form_{current_q}"):
            selected_option = st.radio(
                "Choose your answer:",
                options,
                key=f"enhanced_q_{current_q}",
                index=None
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
                # Check if quiz is complete after incrementing
                if st.session_state.current_question >= len(questions):
                    time.sleep(1)
                    st.rerun()  # This will trigger show_quiz_results()
                else:
                    time.sleep(1)
                    st.rerun()
            elif submit_answer and selected_option is None:
                st.warning("Please select an answer before submitting!")

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

def reset_session_state():
    """Reset all session state for debugging"""
    keys_to_keep = ['user_profile']  # Keep user logged in
    keys_to_remove = [key for key in st.session_state.keys() if key not in keys_to_keep]
    for key in keys_to_remove:
        del st.session_state[key]
    st.rerun()

def clear_user_quiz_history(username):
    """Clear a user's quiz history to allow fresh questions"""
    scores = load_scores()
    # Remove questions_used from all user's scores
    for score in scores:
        if score.get("name", "").lower() == username.lower():
            if "questions_used" in score:
                del score["questions_used"]
    
    # Save updated scores
    with open("quiz_scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
    load_scores.clear()  # Clear cache

def show_quiz_results():
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
    
    # Performance feedback with enhanced styling
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
    
    # Certificate generation for high scores
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
        
        # Download certificate button
        if st.button("📥 Download Certificate", use_container_width=True):
            st.success("Certificate feature will be enhanced in future updates!")
    
    # Detailed results
    st.subheader("📋 Detailed Results")
    
    # Statistics
    correct_answers = score
    incorrect_answers = total - score
    
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
                <span class="stats-number">⭐ {xp_earned}</span>
                <span class="stats-label">XP Earned</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Question-by-question breakdown
    for i, answer in enumerate(st.session_state.answers):
        with st.expander(f"Question {i+1}: {'✅' if answer['is_correct'] else '❌'}"):
            st.write(f"**Question:** {answer['question']}")
            st.write(f"**Your Answer:** {answer['selected']}")
            st.write(f"**Correct Answer:** {answer['correct']}")
            st.write(f"**Explanation:** {answer['explanation']}")
    
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

if __name__ == "__main__":
    main()