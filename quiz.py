# climate_quiz.py

import os
import streamlit as st
import json
import re
from dotenv import load_dotenv

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------
# Groq AI Setup
# --------------------------
try:
    from groq import Groq
    if not GROQ_API_KEY:
        st.error("❌ Missing GROQ_API_KEY. Please set it in your .env file or environment variables.")
        groq_client = None
    else:
        groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Error importing Groq: {e}")
    groq_client = None

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="🌱 Climate Quiz", page_icon="📝", layout="wide")
st.title("📝 Climate Change Quiz")
st.subheader("Test your knowledge and learn while having fun!")

# --------------------------
# Quiz Settings
# --------------------------
num_questions = st.sidebar.slider("Number of questions", 3, 10, 5)
difficulty = st.sidebar.selectbox("Difficulty", ["easy", "medium", "hard"])

# Initialize session state
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --------------------------
# Generate Quiz Button
# --------------------------
if st.button("Generate Quiz"):
    if not groq_client:
        st.error("Groq client not available. Check your API key.")
    else:
        with st.spinner("Generating quiz questions..."):
            prompt = f"""
Generate {num_questions} multiple-choice questions about climate change.
Difficulty level: {difficulty}.
Each question should have 4 options labeled A, B, C, D.
Provide the correct answer.
Return ONLY valid JSON as an array of objects:

[
  {{
    "question": "Question text",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A"
  }}
]
"""
            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a helpful climate quiz generator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=600
                )

                raw_content = response.choices[0].message.content.strip()
                match = re.search(r"(\[.*\])", raw_content, re.DOTALL)
                if match:
                    quiz_json = match.group(1)
                    st.session_state.quiz_data = json.loads(quiz_json)
                    st.session_state.answers = {}
                else:
                    st.error("Failed to extract JSON from AI response.")
                    st.session_state.quiz_data = []
            except Exception as e:
                st.error(f"Error generating quiz: {e}")
                st.session_state.quiz_data = []

# --------------------------
# Display Quiz
# --------------------------
if st.session_state.quiz_data:
    st.success(f"✅ Quiz Generated! {len(st.session_state.quiz_data)} Questions")

    for i, q in enumerate(st.session_state.quiz_data, 1):
        st.markdown(f"**Q{i}: {q['question']}**")
        options = q.get("options", [])
        key = f"q{i}"
        # default to stored answer if exists, otherwise first option
        default_index = options.index(st.session_state.answers.get(key, options[0])) if options else 0
        st.session_state.answers[key] = st.radio(
            "Select an answer:",
            options,
            index=default_index,
            key=key
        )
        st.markdown("---")

    if st.button("Submit Quiz"):
        score = 0
        for i, q in enumerate(st.session_state.quiz_data, 1):
            key = f"q{i}"
            user_ans = st.session_state.answers.get(key, "")
            correct_ans = q.get("answer", "")
            if user_ans.startswith(correct_ans):
                score += 1
        st.success(f"🎉 You scored {score}/{len(st.session_state.quiz_data)}")
