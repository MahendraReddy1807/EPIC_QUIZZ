import streamlit as st
import json
import datetime
import pandas as pd
import os
import random
import hashlib

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
    """Display leaderboard with CSV download option"""
    scores = load_scores()
    if not scores:
        st.info("No scores yet! Take a quiz to see the leaderboard.")
        return
    
    df = pd.DataFrame(scores)
    df = df.sort_values(['percentage', 'timestamp'], ascending=[False, False])
    
    st.subheader("🏆 Leaderboard")
    
    # Add download button for full leaderboard
    col1, col2 = st.columns([3, 1])
    with col2:
        # Prepare CSV data
        csv_data = df[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']].copy()
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
            label="📥 Download CSV",
            data=csv_export.to_csv(index=False),
            file_name=f"quiz_leaderboard_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col1:
        st.write(f"**Total Participants:** {len(df['name'].unique())}")
    
    # Top 10 scores - Use dataframe display for better performance
    top_scores = df.head(10)[['name', 'quiz_type', 'score', 'total', 'percentage', 'language', 'timestamp']]
    top_scores['Quiz'] = top_scores['quiz_type'].str.title()
    top_scores['Score'] = top_scores['score'].astype(str) + '/' + top_scores['total'].astype(str) + ' (' + top_scores['percentage'].astype(str) + '%)'
    top_scores['Date'] = pd.to_datetime(top_scores['timestamp']).dt.strftime('%Y-%m-%d')
    
    display_df = top_scores[['name', 'Quiz', 'Score', 'language', 'Date']].rename(columns={
        'name': 'Name',
        'language': 'Language',
        'Date': 'Date'
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

def main():
    st.set_page_config(
        page_title="Epic Quiz App",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"  # Start with sidebar collapsed for faster load
    )
    
    # Minimal CSS for faster loading
    st.markdown("""
    <style>
    .score-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header - simplified for faster rendering
    st.title("📚 Epic Quiz App")
    st.caption("Test your knowledge of Mahabharata & Ramayana")
    
    # Sidebar for navigation - Always in English
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose an option:", ["Take Quiz", "Leaderboard", "About"])
    
    # Performance indicator
    st.sidebar.markdown("---")
    st.sidebar.caption("⚡ Fast Mode: Optimized for speed")
    
    if page == "Take Quiz":
        # Language selection - Interface remains in English
        st.markdown("### 🌐 Select Quiz Language")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🇺🇸 English", key="lang_en", use_container_width=True):
                st.session_state.selected_language = "english"
        
        with col2:
            if st.button("🇮🇳 తెలుగు (Telugu)", key="lang_te", use_container_width=True):
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
        user_name = st.text_input("Name:", placeholder="Enter your name here...")
        
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
                
                # Display results - Interface in English
                st.markdown(f'''
                <div class="score-card">
                    <h2>🎉 Quiz Completed!</h2>
                    <h3>Score: {score}/{total} ({percentage}%)</h3>
                    <p>Great job, {st.session_state.user_name}!</p>
                </div>
                ''', unsafe_allow_html=True)
                
                # Performance message - Always in English interface
                if percentage >= 80:
                    st.success("🌟 Excellent! You have great knowledge of our epics!")
                elif percentage >= 60:
                    st.info("👍 Good job! Keep learning more about our heritage!")
                else:
                    st.warning("📚 Keep studying! Our epics have so much wisdom to offer!")
                
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

if __name__ == "__main__":
    main()