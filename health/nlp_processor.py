def simple_health_nlp(query):
    keywords = {
        "fever": "Drink plenty of fluids and rest. If the fever persists, consider consulting a doctor.",
        "headache": "Rest in a quiet, dark room and possibly take a mild pain reliever.",
    }
    for keyword, advice in keywords.items():
        if keyword in query.lower():
            return advice
    return "Sorry, I couldn't find any advice related to your symptoms. Please consult a professional."


import random

# Predefined symptoms and potential query formulations
symptoms_queries = {
    "fever": [
        "I feel like I have a fever, what should I do?",
        "What can I do if I have a high fever?",
        "Is there a remedy for a persistent fever?",
        "How to reduce a fever quickly?",
        "Feeling feverish, need advice.",
    ],
    "headache": [
        "I have a terrible headache, how can I relieve it?",
        "What's good for a migraine?",
        "Best treatment for a severe headache?",
        "Home remedies for a headache?",
        "How do I get rid of a headache?",
    ],
    "cough": [
        "I can't stop coughing, what should I take?",
        "Is there a natural remedy for a cough?",
        "What to do if you have a chronic cough?",
        "Best way to treat a dry cough?",
        "Recommendations for a bad cough?",
    ],
}

# Generate 50 queries
data_entries = []
for _ in range(50):
    symptom, queries = random.choice(list(symptoms_queries.items()))
    query = random.choice(queries)
    data_entries.append(query)
