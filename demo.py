#!/usr/bin/env python3
"""
Demo script for Epic Quiz App
Shows basic functionality and question samples
"""

def demo_questions():
    """Display sample questions from both epics"""
    from fast_questions import get_mahabharata_questions, get_ramayana_questions
    
    print("🎯 Epic Quiz App Demo")
    print("=" * 50)
    
    # Load questions
    maha_questions = get_mahabharata_questions()
    rama_questions = get_ramayana_questions()
    
    print(f"📚 Total Questions Available:")
    print(f"   • Mahabharata: {len(maha_questions)} questions")
    print(f"   • Ramayana: {len(rama_questions)} questions")
    
    # Show difficulty distribution
    from collections import Counter
    maha_diff = Counter([q['difficulty'] for q in maha_questions])
    rama_diff = Counter([q['difficulty'] for q in rama_questions])
    
    print(f"\n📊 Difficulty Distribution:")
    print(f"   Mahabharata: {dict(maha_diff)}")
    print(f"   Ramayana: {dict(rama_diff)}")
    
    # Show sample questions
    print(f"\n🔍 Sample Questions:")
    print(f"\n🏹 Mahabharata Sample:")
    sample_maha = maha_questions[0]
    print(f"   Q: {sample_maha['question']['english']}")
    print(f"   Telugu: {sample_maha['question']['telugu']}")
    print(f"   Options: {sample_maha['options']['english']}")
    print(f"   Answer: {sample_maha['options']['english'][sample_maha['correct']]}")
    print(f"   Difficulty: {sample_maha['difficulty']}")
    
    print(f"\n🐒 Ramayana Sample:")
    sample_rama = rama_questions[0]
    print(f"   Q: {sample_rama['question']['english']}")
    print(f"   Telugu: {sample_rama['question']['telugu']}")
    print(f"   Options: {sample_rama['options']['english']}")
    print(f"   Answer: {sample_rama['options']['english'][sample_rama['correct']]}")
    print(f"   Difficulty: {sample_rama['difficulty']}")
    
    print(f"\n🚀 To run the full app:")
    print(f"   streamlit run quiz_app.py")
    
    print(f"\n🧪 To run tests:")
    print(f"   python test_quiz.py")

if __name__ == "__main__":
    demo_questions()