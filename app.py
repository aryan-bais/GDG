import streamlit as st
from parser import extract_text
from anonymizer import anonymize
from feature_extractor import extract_skills
from embedder import get_similarity
from ranker import rank_candidates
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="FairHire", layout="wide")

st.title("⚖️ FairHire — Blind AI Hiring System")

# Sidebar
mode = st.sidebar.radio("Screening Mode", ["Normal", "Blind"])

uploaded_files = st.file_uploader("Upload Resumes", accept_multiple_files=True)
job_desc = st.text_area("Paste Job Description")

if uploaded_files and job_desc:

    normal_candidates = []
    blind_candidates = []

    for file in uploaded_files:
        text = extract_text(file)

        # NORMAL
        skills = extract_skills(text)
        sim = get_similarity(text, job_desc)
        normal_score = len(skills) + sim

        normal_candidates.append({
            "name": file.name,
            "skills": skills,
            "score": normal_score
        })

        # BLIND
        anon_text = anonymize(text)
        skills_b = extract_skills(anon_text)
        sim_b = get_similarity(anon_text, job_desc)
        blind_score = len(skills_b) + sim_b

        blind_candidates.append({
            "name": file.name,
            "skills": skills_b,
            "score": blind_score
        })

    normal_ranked = sorted(normal_candidates, key=lambda x: x["score"], reverse=True)
    blind_ranked = sorted(blind_candidates, key=lambda x: x["score"], reverse=True)

    # SIDE BY SIDE VIEW
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Normal Ranking")
        for i, c in enumerate(normal_ranked):
            st.write(f"{i+1}. {c['name']} | Score: {round(c['score'],2)}")

    with col2:
        st.subheader("🔒 Blind Ranking")
        for i, c in enumerate(blind_ranked):
            st.write(f"{i+1}. {c['name']} | Score: {round(c['score'],2)}")

    # Bias visualization
    st.subheader("📊 Bias Comparison")

    df = pd.DataFrame({
        "Candidate": [c["name"] for c in normal_ranked],
        "Normal Score": [c["score"] for c in normal_ranked],
        "Blind Score": [c["score"] for c in blind_ranked]
    })

    st.dataframe(df)

    fig, ax = plt.subplots()
    df.set_index("Candidate").plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.success("Blind screening reduces potential bias in ranking!")