# awareness_hub.py

import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ---------------------------
# 🔑 Load environment variables from .env
# ---------------------------
load_dotenv()  # This will read .env file in your project root

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Please create a .env file with GROQ_API_KEY=<your_key>")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(page_title="📢 Awareness Hub", layout="wide")

st.title("📢 Awareness Hub")
st.write("Get climate news, tips, and campaign updates in one place — powered by AI 🌍")

# ---------------------------
# User Options
# ---------------------------
option = st.selectbox(
    "What would you like to explore?",
    ["🌍 Latest Climate News", "🌱 Eco-Friendly Tips", "📢 Campaign Updates"]
)

if st.button("Generate"):
    with st.spinner("Fetching AI-powered insights..."):
        try:
            if option == "🌍 Latest Climate News":
                prompt = "Give me the 3 most recent global climate news highlights with clear titles and short summaries."

            elif option == "🌱 Eco-Friendly Tips":
                prompt = "Share 5 practical eco-friendly lifestyle tips for individuals and households to reduce carbon footprint."

            elif option == "📢 Campaign Updates":
                prompt = "Summarize 3 ongoing climate action campaigns or movements worldwide, with a short call-to-action for each."

            # ---------------------------
            # Groq API Call
            # ---------------------------
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert climate journalist and sustainability advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Extract AI response safely
            if response and response.choices:
                output = response.choices[0].message.content.strip()
                st.subheader(option)
                st.write(output)
            else:
                st.error("⚠️ No response received from Groq API.")

        except Exception as e:
            st.error(f"⚠️ Error fetching data: {str(e)}")
