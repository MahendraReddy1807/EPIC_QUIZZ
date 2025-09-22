# Contributing to Epic Quiz App

Thank you for your interest in contributing to the Epic Quiz App! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Provide detailed information about the issue
- Include steps to reproduce the problem
- Mention your operating system and Python version

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Explain how it fits with the project's goals

### Contributing Code

1. **Fork the Repository**
   ```bash
   git fork https://github.com/yourusername/epic-quiz-app.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test Your Changes**
   ```bash
   python test_quiz.py
   streamlit run quiz_app.py
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "Add: your feature description"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots if UI changes are made

## 📝 Code Style Guidelines

- Use Python PEP 8 style guide
- Add docstrings to functions and classes
- Use meaningful variable and function names
- Keep functions focused and small
- Add comments for complex logic

## 🧪 Testing

- Run the test suite before submitting: `python test_quiz.py`
- Test the Streamlit app manually: `streamlit run quiz_app.py`
- Ensure all features work in both English and Telugu
- Test CSV download functionality

## 📚 Adding Questions

When adding new questions:

1. **Follow the existing format** in `fast_questions.py`
2. **Include both English and Telugu** translations
3. **Provide accurate answers** with explanations
4. **Maintain difficulty balance** (Easy/Medium/Hard)
5. **Verify cultural accuracy** for epic-related content

### Question Format
```python
{
    "q": "English question text",
    "tq": "Telugu question text",
    "o": ["Option A", "Option B", "Option C", "Option D"],
    "to": ["Telugu Option A", "Telugu Option B", "Telugu Option C", "Telugu Option D"],
    "c": 0,  # Correct answer index (0-3)
    "d": "easy"  # Difficulty: easy, medium, hard
}
```

## 🌐 Translation Guidelines

- Maintain cultural context in translations
- Use appropriate Telugu script and terminology
- Ensure consistency in character names
- Verify translations with native speakers when possible

## 📋 Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass successfully
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] No unnecessary files are included
- [ ] Feature works in both languages
- [ ] CSV export functionality is tested

## 🎯 Areas for Contribution

- **Question Database**: Add more authentic questions
- **UI/UX Improvements**: Enhance user interface
- **Performance Optimization**: Improve loading times
- **Language Support**: Add more Indian languages
- **Testing**: Improve test coverage
- **Documentation**: Enhance user guides

## 📞 Getting Help

- Open an issue for questions
- Join discussions in existing issues
- Contact maintainers for major changes

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features

Thank you for helping preserve and share Indian cultural heritage through technology! 🙏