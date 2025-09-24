# 👑 Admin Dashboard Documentation

## Overview
The Epic Quiz App now includes a comprehensive admin dashboard for system management and user administration.

## Admin Access
- **Username:** `Mahi07`
- **Password:** `1477`
- **Access:** Login page → Admin tab → Enter credentials

## Dashboard Features

### 📊 System Overview
- **Total Users:** Display count of registered users
- **Total Scores:** Display count of quiz attempts
- **Average Score:** Calculate and display average performance across all users

### 👥 User Management
- **View All Users:** Display complete list of registered users with:
  - Username
  - Level
  - XP Points
  - Quiz completion count
- **Delete User:** Remove user profile and all associated data
  - Removes from user profiles
  - Removes from leaderboard
  - Complete data cleanup

### 🏆 Leaderboard Management
- **View Recent Scores:** Display last 10 quiz attempts with:
  - Player name
  - Quiz type (Mahabharata/Ramayana)
  - Score percentage
  - Timestamp
- **Clear All Scores:** Remove all quiz scores from leaderboard
  - Requires confirmation
  - Irreversible action
  - Clears quiz_scores.json

### 🔧 System Tools
- **Real-time Statistics:** Live data from user profiles and scores
- **Error Handling:** Graceful error management for all operations
- **Data Validation:** Ensures data integrity during operations

## Technical Implementation

### Files Modified
- `enhanced_quiz_app.py` - Main application with admin functionality
- `quiz_app.py` - Entry point with redirect to enhanced version
- Login system enhanced with admin tab

### Admin Functions
```python
def delete_user_profile(username):
    """Delete user profile completely"""
    
def load_users():
    """Load user profiles from JSON"""
    
def load_scores():
    """Load quiz scores from JSON"""
```

### Security Features
- Admin credentials hardcoded for security
- Session-based admin authentication
- Admin-only navigation options
- Protected admin routes

## Data Management

### User Profiles (`user_profiles.json`)
```json
{
  "username": {
    "level": 1,
    "xp_points": 0,
    "total_quizzes": 0,
    "achievements": [],
    "streak_days": 0,
    "created_date": "2024-09-24T..."
  }
}
```

### Quiz Scores (`quiz_scores.json`)
```json
[
  {
    "name": "username",
    "quiz_type": "mahabharata",
    "score": 15,
    "total": 20,
    "percentage": 75.0,
    "language": "english",
    "timestamp": "2024-09-24T..."
  }
]
```

## Admin Workflow

1. **Login as Admin**
   - Go to login page
   - Click "Admin" tab
   - Enter: Mahi07 / 1477
   - Click "Admin Login"

2. **Access Dashboard**
   - Navigate to "👑 Admin Dashboard" in sidebar
   - View system overview automatically

3. **Manage Users**
   - Click "📋 Show All Users" to view all registered users
   - Enter username in delete field to remove user
   - Click "Delete User" to confirm removal

4. **Manage Leaderboard**
   - Click "📊 Show Recent Scores" to view recent activity
   - Click "🗑️ Clear All Scores" to reset leaderboard

## Version History
- **v2.1** - Admin dashboard implementation
- **v2.0** - Enhanced quiz app with user profiles
- **v1.0** - Basic quiz functionality

## Deployment
- Deployed on Streamlit Cloud
- Auto-updates from GitHub repository
- Entry point: `quiz_app.py` → `enhanced_quiz_app.py`

## Support
For admin dashboard issues:
1. Check Streamlit Cloud logs
2. Verify file permissions
3. Ensure JSON files are writable
4. Check admin credentials

---
**Last Updated:** September 24, 2024
**Version:** 2.1
**Status:** ✅ Active and Working