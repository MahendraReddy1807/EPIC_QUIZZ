# 📚 Epic Quiz App

A fast, bilingual quiz application for testing knowledge of Mahabharata and Ramayana epics with authentic questions and comprehensive features.

![Quiz App Demo](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features

- **🎯 200 Authentic Questions**: 100 each for Mahabharata and Ramayana
- **🌐 Bilingual Support**: Complete English and Telugu translations
- **📊 20 Questions per Quiz**: 6 Easy + 8 Medium + 6 Hard for comprehensive testing
- **🔄 Anti-Repetition System**: Smart algorithm avoids repeated questions
- **📈 Score Tracking**: Complete leaderboard with performance history
- **📥 CSV Export**: Download leaderboard data and individual quiz results
- **⚡ Fast Performance**: Optimized with caching for instant loading
- **🎨 User-Friendly Interface**: Clean, responsive design with progress indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/epic-quiz-app.git
   cd epic-quiz-app
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit pandas
   ```

3. **Run the application**:
   ```bash
   streamlit run quiz_app.py
   ```

4. **Test functionality** (optional):
   ```bash
   python test_quiz.py
   ```

## 📖 How to Use

1. **🌐 Select Language**: Choose English or Telugu for quiz content
2. **👤 Enter Name**: Provide your name for score tracking
3. **📚 Choose Quiz**: Select between Mahabharata or Ramayana
4. **❓ Answer Questions**: Complete 20 questions with difficulty indicators
5. **📊 View Results**: See detailed score, explanations, and download results
6. **🏆 Check Leaderboard**: Compare with other participants and download data

## 🎯 Quiz Structure

### Difficulty Distribution (20 Questions Total)
- **🟢 Easy Questions (6)**: Basic knowledge about main characters and events
- **🟡 Medium Questions (8)**: Intermediate details about relationships and stories
- **🔴 Hard Questions (6)**: Advanced knowledge and specific cultural details

### Sample Questions
#### Mahabharata
- Who was the author of Mahabharata? → **Vyasa**
- How many days did the Kurukshetra war last? → **18 days**
- Who was Arjuna's charioteer? → **Krishna**

#### Ramayana
- Who was the author of Ramayana? → **Valmiki**
- How many years did Rama spend in exile? → **14 years**
- Who was Rama's devoted follower? → **Hanuman**

## 📊 Technical Features

- **⚡ Performance**: Questions load in <0.001 seconds
- **💾 Caching**: Streamlit @st.cache_data for optimal performance
- **🔀 Smart Selection**: Difficulty-based question distribution algorithm
- **💾 Data Storage**: JSON-based score and history tracking
- **📱 Responsive**: Works on desktop and mobile devices

## 🗂️ Project Structure

```
epic-quiz-app/
├── quiz_app.py              # Main Streamlit application
├── fast_questions.py        # Optimized question database
├── test_quiz.py            # Functionality test script
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── quiz_scores.json       # User scores (auto-generated)
```

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas
- **Caching**: Streamlit built-in caching
- **Export**: CSV format for data portability

## 🌟 Key Highlights

- **Authentic Content**: Real questions about Indian epics
- **Cultural Preservation**: Digital format for ancient knowledge
- **Educational Value**: Comprehensive testing with explanations
- **Data Export**: Full tracking and analysis capabilities
- **Bilingual Access**: Supports both English and Telugu speakers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ancient Indian literature and cultural heritage
- Streamlit community for the amazing framework
- Contributors to the question database
- Telugu language community for translations

## 📞 Contact

Your Name - [@yourusername](https://twitter.com/yourusername) - your.email@example.com

Project Link: [https://github.com/yourusername/epic-quiz-app](https://github.com/yourusername/epic-quiz-app)

---

⭐ **Star this repository if you found it helpful!** ⭐