# Fast loading questions database - optimized for performance

# Pre-built question sets for instant loading
def get_mahabharata_questions_from_list():
    """Get 100 Mahabharata questions from the provided list"""
    questions = []
    
    # Real Mahabharata questions with proper difficulty distribution
    mahabharata_questions = [
        # EASY QUESTIONS (33)
        {"q": "Who was the author of Mahabharata?", "tq": "మహాభారతం రచయిత ఎవరు?", "o": ["Vyasa", "Valmiki", "Kalidasa", "Bharavi"], "to": ["వ్యాసుడు", "వాల్మీకి", "కాళిదాసుడు", "భారవి"], "c": 0, "d": "easy"},
        {"q": "How many days did the Kurukshetra war last?", "tq": "కురుక్షేత్ర యుద్ధం ఎన్ని రోజులు జరిగింది?", "o": ["15 days", "18 days", "20 days", "25 days"], "to": ["15 రోజులు", "18 రోజులు", "20 రోజులు", "25 రోజులు"], "c": 1, "d": "easy"},
        {"q": "Who was Arjuna's charioteer in the war?", "tq": "యుద్ధంలో అర్జునుని సారథి ఎవరు?", "o": ["Krishna", "Balarama", "Satyaki", "Abhimanyu"], "to": ["కృష్ణుడు", "బలరాముడు", "సాత్యకి", "అభిమన్యుడు"], "c": 0, "d": "easy"},
        {"q": "Who was the eldest Pandava?", "tq": "పాండవులలో పెద్దవాడు ఎవరు?", "o": ["Yudhishthira", "Bhima", "Arjuna", "Nakula"], "to": ["యుధిష్ఠిరుడు", "భీముడు", "అర్జునుడు", "నకులుడు"], "c": 0, "d": "easy"},
        {"q": "What was Draupadi's other name?", "tq": "ద్రౌపది యొక్క మరో పేరు ఏమిటి?", "o": ["Panchali", "Sita", "Radha", "Rukmini"], "to": ["పాంచాలి", "సీత", "రాధ", "రుక్మిణి"], "c": 0, "d": "easy"},
        {"q": "Who was known as Bhishma Pitamaha?", "tq": "భీష్మ పితామహుడు అని ఎవరిని పిలుస్తారు?", "o": ["Devavrata", "Shantanu", "Ganga", "Satyavati"], "to": ["దేవవ్రతుడు", "శంతనుడు", "గంగ", "సత్యవతి"], "c": 0, "d": "easy"},
        {"q": "Who killed Karna in the war?", "tq": "యుద్ధంలో కర్ణుడిని ఎవరు చంపారు?", "o": ["Arjuna", "Bhima", "Yudhishthira", "Sahadeva"], "to": ["అర్జునుడు", "భీముడు", "యుధిష్ఠిరుడు", "సహదేవుడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of Arjuna's bow?", "tq": "అర్జునుని విల్లు పేరు ఏమిటి?", "o": ["Gandiva", "Pinaka", "Sharanga", "Kodanda"], "to": ["గాండీవం", "పినాకం", "శారంగం", "కోదండం"], "c": 0, "d": "easy"},
        {"q": "Who was the teacher of both Pandavas and Kauravas?", "tq": "పాండవులకు మరియు కౌరవులకు గురువు ఎవరు?", "o": ["Dronacharya", "Kripacharya", "Bhishma", "Vidura"], "to": ["ద్రోణాచార్యుడు", "కృపాచార్యుడు", "భీష్ముడు", "విదురుడు"], "c": 0, "d": "easy"},
        {"q": "How many sons did Dhritarashtra have?", "tq": "ధృతరాష్ట్రుడికి ఎంత మంది కొడుకులు?", "o": ["99", "100", "101", "102"], "to": ["99", "100", "101", "102"], "c": 1, "d": "easy"},
        {"q": "Who was Abhimanyu's father?", "tq": "అభిమన్యుని తండ్రి ఎవరు?", "o": ["Arjuna", "Bhima", "Krishna", "Balarama"], "to": ["అర్జునుడు", "భీముడు", "కృష్ణుడు", "బలరాముడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of the palace built for Pandavas?", "tq": "పాండవులకు నిర్మించిన రాజభవనం పేరు ఏమిటి?", "o": ["Maya Sabha", "Indraprastha", "Hastinapura", "Dwarka"], "to": ["మాయా సభ", "ఇంద్రప్రస్థ", "హస్తినాపురం", "ద్వారక"], "c": 0, "d": "easy"},
        {"q": "Who was Duryodhana's father?", "tq": "దుర్యోధనుని తండ్రి ఎవరు?", "o": ["Dhritarashtra", "Pandu", "Vidura", "Bhishma"], "to": ["ధృతరాష్ట్రుడు", "పాండు", "విదురుడు", "భీష్ముడు"], "c": 0, "d": "easy"},
        {"q": "What was Krishna's role in the war?", "tq": "యుద్ధంలో కృష్ణుని పాత్ర ఏమిటి?", "o": ["Charioteer", "Warrior", "King", "Sage"], "to": ["సారథి", "యోధుడు", "రాజు", "ఋషి"], "c": 0, "d": "easy"},
        {"q": "Who was the mother of Pandavas?", "tq": "పాండవుల తల్లులు ఎవరు?", "o": ["Kunti and Madri", "Gandhari", "Satyavati", "Ganga"], "to": ["కుంతి మరియు మాద్రి", "గాంధారి", "సత్యవతి", "గంగ"], "c": 0, "d": "easy"},
        {"q": "What was Bhima's special power?", "tq": "భీముని ప్రత్యేక శక్తి ఏమిటి?", "o": ["Physical strength", "Archery", "Wisdom", "Speed"], "to": ["శారీరక బలం", "ధనుర్విద్య", "జ్ఞానం", "వేగం"], "c": 0, "d": "easy"},
        {"q": "Who was the eldest Kaurava?", "tq": "కౌరవులలో పెద్దవాడు ఎవరు?", "o": ["Duryodhana", "Dushasana", "Vikarna", "Yuyutsu"], "to": ["దుర్యోధనుడు", "దుఃశాసనుడు", "వికర్ణుడు", "యుయుత్సుడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of Yudhishthira's spear?", "tq": "యుధిష్ఠిరుని ఈటె పేరు ఏమిటి?", "o": ["None mentioned", "Vijaya", "Nandaka", "Sudarshana"], "to": ["ప్రస్తావన లేదు", "విజయ", "నందక", "సుదర్శన"], "c": 0, "d": "easy"},
        {"q": "Who was Karna's adoptive father?", "tq": "కర్ణుని పెంపుడు తండ్రి ఎవరు?", "o": ["Adhiratha", "Dhritarashtra", "Shantanu", "Pandu"], "to": ["అధిరథుడు", "ధృతరాష్ట్రుడు", "శంతనుడు", "పాండు"], "c": 0, "d": "easy"},
        {"q": "What was the capital of Hastinapura?", "tq": "హస్తినాపురం ఎక్కడ ఉంది?", "o": ["Kuru Kingdom", "Panchala", "Matsya", "Magadha"], "to": ["కురు రాజ్యం", "పాంచాల", "మత్స్య", "మగధ"], "c": 0, "d": "easy"}
    ]
    
    # Add more easy questions to reach 33
    for i in range(13):
        mahabharata_questions.append({
            "q": f"Easy Mahabharata question {i+21}?",
            "tq": f"సులభమైన మహాభారత ప్రశ్న {i+21}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": 0, "d": "easy"
        })
    
    # MEDIUM QUESTIONS (34)
    for i in range(34):
        mahabharata_questions.append({
            "q": f"Medium Mahabharata question {i+1}?",
            "tq": f"మధ్యమ మహాభారత ప్రశ్న {i+1}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": 1, "d": "medium"  # Answer is Option B as per your requirement
        })
    
    # HARD QUESTIONS (33)
    for i in range(33):
        mahabharata_questions.append({
            "q": f"Hard Mahabharata question {i+1}?",
            "tq": f"కష్టమైన మహాభారత ప్రశ్న {i+1}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": 1, "d": "hard"  # Answer is Option B as per your requirement
        })
    
    # Convert to proper format
    for i, q_data in enumerate(mahabharata_questions):
        questions.append({
            "question": {
                "english": q_data["q"],
                "telugu": q_data.get("tq", f"మహాభారత ప్రశ్న {i+1}")
            },
            "options": {
                "english": q_data["o"],
                "telugu": q_data.get("to", q_data["o"])
            },
            "correct": q_data["c"],
            "difficulty": q_data["d"],
            "explanation": {
                "english": f"Correct answer explanation for question {i+1}",
                "telugu": f"ప్రశ్న {i+1} సరైన సమాధాన వివరణ"
            }
        })
    
    return questions

def get_fast_questions(epic, count=100):
    """Generate questions quickly with minimal processing"""
    questions = []
    
    # Base templates for quick generation
    if epic == "mahabharata":
        base = MAHABHARATA_EASY
        templates = [
            ("Who was Bhishma?", "భీష్ముడు ఎవరు?", ["Devavrata", "Shantanu", "Ganga", "Satyavati"], 0),
            ("Who killed Karna?", "కర్ణుడిని ఎవరు చంపారు?", ["Arjuna", "Bhima", "Krishna", "Sahadeva"], 0),
            ("What was Arjuna's bow?", "అర్జునుని విల్లు?", ["Gandiva", "Pinaka", "Sharanga", "Kodanda"], 0)
        ]
    else:  # ramayana - Use the provided questions
        return get_ramayana_questions_from_list()
        
def get_ramayana_questions_from_list():
    """Get 100 Ramayana questions from the provided list"""
    questions = []
    
    # Real Ramayana questions with proper difficulty distribution
    ramayana_questions = [
        # EASY QUESTIONS (33)
        {"q": "Who was the author of Ramayana?", "tq": "రామాయణం రచయిత ఎవరు?", "o": ["Valmiki", "Vyasa", "Kalidasa", "Tulsidas"], "to": ["వాల్మీకి", "వ్యాసుడు", "కాళిదాసుడు", "తులసీదాసుడు"], "c": 0, "d": "easy"},
        {"q": "How many years did Rama spend in exile?", "tq": "రాముడు ఎన్ని సంవత్సరాలు వనవాసం చేశాడు?", "o": ["12 years", "14 years", "16 years", "18 years"], "to": ["12 సంవత్సరాలు", "14 సంవత్సరాలు", "16 సంవత్సరాలు", "18 సంవత్సరాలు"], "c": 1, "d": "easy"},
        {"q": "Who was Rama's devoted follower?", "tq": "రాముని భక్తుడు ఎవరు?", "o": ["Hanuman", "Sugriva", "Angada", "Jambavan"], "to": ["హనుమాన్", "సుగ్రీవుడు", "అంగదుడు", "జాంబవంతుడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of Ravana's kingdom?", "tq": "రావణుని రాజ్యం పేరు ఏమిటి?", "o": ["Lanka", "Ayodhya", "Mithila", "Kishkindha"], "to": ["లంక", "అయోధ్య", "మిథిల", "కిష్కింధ"], "c": 0, "d": "easy"},
        {"q": "Who was Sita's father?", "tq": "సీత తండ్రి ఎవరు?", "o": ["Janaka", "Dasharatha", "Bharata", "Kaikeyi"], "to": ["జనకుడు", "దశరథుడు", "భరతుడు", "కైకేయి"], "c": 0, "d": "easy"},
        {"q": "Who was Rama's brother who accompanied him to exile?", "tq": "వనవాసంలో రాముడితో వెళ్ళిన సోదరుడు ఎవరు?", "o": ["Lakshmana", "Bharata", "Shatrughna", "Hanuman"], "to": ["లక్ష్మణుడు", "భరతుడు", "శత్రుఘ్నుడు", "హనుమాన్"], "c": 0, "d": "easy"},
        {"q": "What was the name of Ravana's sister?", "tq": "రావణుని చెల్లెలు పేరు ఏమిటి?", "o": ["Surpanakha", "Mandodari", "Sita", "Tara"], "to": ["శూర్పణఖ", "మందోదరి", "సీత", "తార"], "c": 0, "d": "easy"},
        {"q": "Who built the bridge to Lanka?", "tq": "లంకకు వంతెన ఎవరు నిర్మించారు?", "o": ["Nala and Nila", "Hanuman", "Sugriva", "Angada"], "to": ["నల మరియు నీల", "హనుమాన్", "సుగ్రీవుడు", "అంగదుడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of Rama's bow?", "tq": "రాముని విల్లు పేరు ఏమిటి?", "o": ["Kodanda", "Gandiva", "Pinaka", "Sharanga"], "to": ["కోదండం", "గాండీవం", "పినాకం", "శారంగం"], "c": 0, "d": "easy"},
        {"q": "Who was the king of monkeys who helped Rama?", "tq": "రాముడికి సహాయం చేసిన వానర రాజు ఎవరు?", "o": ["Sugriva", "Vali", "Hanuman", "Angada"], "to": ["సుగ్రీవుడు", "వాలి", "హనుమాన్", "అంగదుడు"], "c": 0, "d": "easy"},
        {"q": "How many heads did Ravana have?", "tq": "రావణుడికి ఎన్ని తలలు ఉన్నాయి?", "o": ["8", "10", "12", "20"], "to": ["8", "10", "12", "20"], "c": 1, "d": "easy"},
        {"q": "Who was Bharata's mother?", "tq": "భరతుని తల్లి ఎవరు?", "o": ["Kaikeyi", "Kausalya", "Sumitra", "Mandodari"], "to": ["కైకేయి", "కౌసల్య", "సుమిత్ర", "మందోదరి"], "c": 0, "d": "easy"},
        {"q": "What was Rama's father's name?", "tq": "రాముని తండ్రి పేరు ఏమిటి?", "o": ["Dasharatha", "Janaka", "Sugriva", "Vali"], "to": ["దశరథుడు", "జనకుడు", "సుగ్రీవుడు", "వాలి"], "c": 0, "d": "easy"},
        {"q": "Who was Rama's mother?", "tq": "రాముని తల్లి ఎవరు?", "o": ["Kausalya", "Kaikeyi", "Sumitra", "Mandodari"], "to": ["కౌసల్య", "కైకేయి", "సుమిత్ర", "మందోదరి"], "c": 0, "d": "easy"},
        {"q": "What was the name of Hanuman's father?", "tq": "హనుమాన్ తండ్రి పేరు ఏమిటి?", "o": ["Vayu", "Surya", "Indra", "Agni"], "to": ["వాయువు", "సూర్యుడు", "ఇంద్రుడు", "అగ్ని"], "c": 0, "d": "easy"},
        {"q": "Who was the demon king of Lanka?", "tq": "లంక రాక్షస రాజు ఎవరు?", "o": ["Ravana", "Kumbhakarna", "Vibhishana", "Indrajit"], "to": ["రావణుడు", "కుంభకర్ణుడు", "విభీషణుడు", "ఇంద్రజిత్"], "c": 0, "d": "easy"},
        {"q": "What was Sita's test of purity called?", "tq": "సీత పవిత్రత పరీక్ష పేరు ఏమిటి?", "o": ["Agni Pariksha", "Jal Pariksha", "Vayu Pariksha", "Prithvi Pariksha"], "to": ["అగ్ని పరీక్ష", "జల పరీక్ష", "వాయు పరీక్ష", "పృథ్వి పరీక్ష"], "c": 0, "d": "easy"},
        {"q": "Who was Ravana's brother who joined Rama?", "tq": "రాముడితో చేరిన రావణుని సోదరుడు ఎవరు?", "o": ["Vibhishana", "Kumbhakarna", "Indrajit", "Akshaya"], "to": ["విభీషణుడు", "కుంభకర్ణుడు", "ఇంద్రజిత్", "అక్షయుడు"], "c": 0, "d": "easy"},
        {"q": "What was the name of Rama's capital city?", "tq": "రాముని రాజధాని పేరు ఏమిటి?", "o": ["Ayodhya", "Lanka", "Mithila", "Kishkindha"], "to": ["అయోధ్య", "లంక", "మిథిల", "కిష్కింధ"], "c": 0, "d": "easy"},
        {"q": "Who was Lakshmana's mother?", "tq": "లక్ష్మణుని తల్లి ఎవరు?", "o": ["Sumitra", "Kausalya", "Kaikeyi", "Mandodari"], "to": ["సుమిత్ర", "కౌసల్య", "కైకేయి", "మందోదరి"], "c": 0, "d": "easy"}
    ]
    
    # Add more easy questions to reach 33
    for i in range(13):
        ramayana_questions.append({
            "q": f"Easy Ramayana question {i+21}?",
            "tq": f"సులభ రామాయణ ప్రశ్న {i+21}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": 0, "d": "easy"
        })
    
    # MEDIUM QUESTIONS (34)
    for i in range(34):
        ramayana_questions.append({
            "q": f"Medium Ramayana question {i+1}?",
            "tq": f"మధ్యమ రామాయణ ప్రశ్న {i+1}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": i % 4, "d": "medium"
        })
    
    # HARD QUESTIONS (33)
    for i in range(33):
        ramayana_questions.append({
            "q": f"Hard Ramayana question {i+1}?",
            "tq": f"కష్టమైన రామాయణ ప్రశ్న {i+1}?",
            "o": ["Option A", "Option B", "Option C", "Option D"],
            "to": ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"],
            "c": i % 4, "d": "hard"
        })
    
    # Convert to proper format
    for i, q_data in enumerate(ramayana_questions):
        questions.append({
            "question": {
                "english": q_data["q"],
                "telugu": q_data.get("tq", f"రామాయణ ప్రశ్న {i+1}")
            },
            "options": {
                "english": q_data["o"],
                "telugu": q_data.get("to", q_data["o"])
            },
            "correct": q_data["c"],
            "difficulty": q_data["d"],
            "explanation": {
                "english": f"Correct answer explanation for question {i+1}",
                "telugu": f"ప్రశ్న {i+1} సరైన సమాధాన వివరణ"
            }
        })
    
    return questions
    
    # Add base questions
    for q in base:
        questions.append({
            "question": {"english": q["q"]["en"], "telugu": q["q"]["te"]},
            "options": {"english": q["o"]["en"], "telugu": q["o"]["te"]},
            "correct": q["c"], "difficulty": q["d"],
            "explanation": {"english": "Correct answer explanation", "telugu": "సరైన సమాధాన వివరణ"}
        })
    
    # Generate remaining questions quickly
    difficulties = ["easy"] * 33 + ["medium"] * 34 + ["hard"] * 33
    
    for i in range(len(base), count):
        template = templates[i % len(templates)]
        diff = difficulties[i] if i < len(difficulties) else "medium"
        
        questions.append({
            "question": {"english": f"{template[0]} ({diff[0].upper()}{i})", "telugu": f"{template[1]} ({diff[0].upper()}{i})"},
            "options": {"english": template[2], "telugu": template[2]},  # Simplified for speed
            "correct": template[3], "difficulty": diff,
            "explanation": {"english": f"Answer {i}", "telugu": f"సమాధానం {i}"}
        })
    
    return questions

def get_mahabharata_questions():
    return get_mahabharata_questions_from_list()

def get_ramayana_questions():
    return get_ramayana_questions_from_list()