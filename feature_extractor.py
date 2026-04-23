skills_list = ["python", "machine learning", "data analysis", "java"]

def extract_features(text):
    text_lower = text.lower()
    skills = [skill for skill in skills_list if skill in text_lower]
    score = len(skills)
    return {
        "skills": skills,
        "score": score
    }