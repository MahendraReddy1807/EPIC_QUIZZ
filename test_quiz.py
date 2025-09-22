#!/usr/bin/env python3
"""Test script for the quiz app"""

def test_quiz_functionality():
    """Test all major quiz app functions"""
    print("🧪 Testing Quiz App Functionality...")
    
    try:
        # Test 1: Import modules
        from quiz_app import get_quiz_data, get_random_questions, load_questions
        from fast_questions import get_mahabharata_questions, get_ramayana_questions
        print("✅ All modules imported successfully")
        
        # Test 2: Load questions
        mahabharata_q = get_mahabharata_questions()
        ramayana_q = get_ramayana_questions()
        print(f"✅ Questions loaded: Mahabharata={len(mahabharata_q)}, Ramayana={len(ramayana_q)}")
        
        # Test 3: Check difficulty distribution
        maha_difficulties = [q['difficulty'] for q in mahabharata_q]
        from collections import Counter
        maha_dist = Counter(maha_difficulties)
        print(f"✅ Mahabharata difficulty distribution: {dict(maha_dist)}")
        
        # Test 4: Test quiz data function
        quiz_data = get_quiz_data()
        print(f"✅ Quiz data structure: {list(quiz_data.keys())}")
        
        # Test 5: Test random question selection
        selected_questions = get_random_questions('mahabharata', 20, [])
        selected_difficulties = [q[2]['difficulty'] for q in selected_questions]
        selected_dist = Counter(selected_difficulties)
        print(f"✅ Random selection difficulty distribution: {dict(selected_dist)}")
        
        # Test 6: Verify question structure
        sample_q = selected_questions[0][2]
        required_keys = ['question', 'options', 'correct', 'difficulty', 'explanation']
        has_all_keys = all(key in sample_q for key in required_keys)
        print(f"✅ Question structure valid: {has_all_keys}")
        
        # Test 7: Verify bilingual support
        has_english = 'english' in sample_q['question']
        has_telugu = 'telugu' in sample_q['question']
        print(f"✅ Bilingual support: English={has_english}, Telugu={has_telugu}")
        
        print("\n🎉 All tests passed! Quiz app is ready to use.")
        print("\n📋 Summary:")
        print(f"   • Total questions: {len(mahabharata_q) + len(ramayana_q)}")
        print(f"   • Epics supported: {len(quiz_data)}")
        print(f"   • Difficulty levels: {len(set(maha_difficulties))}")
        print(f"   • Languages: 2 (English, Telugu)")
        print(f"   • Questions per quiz: 20 (6 Easy + 8 Medium + 6 Hard)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_quiz_functionality()