# climate_explorer.py

import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ---------------------------
# 🔑 Load Environment Variables
# ---------------------------
load_dotenv()  # load from .env file if present

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Expect API key from env
if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Please set it as an environment variable or in a .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(page_title="🌍 Climate Initiatives Explorer", layout="wide")
st.title("🌍 Climate Initiatives Explorer")
st.write("Enter the name of a project, initiative, city, or country to learn about climate-related efforts.")

# ---------------------------
# User Input
# ---------------------------
query = st.text_input("🔍 Search for a project, initiative, city, or country:", "")

if st.button("Get Information"):
    if query.strip():
        with st.spinner("Fetching information..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # ✅ supported model
                    messages=[
                        {"role": "system", "content": "You are an expert on global climate initiatives, sustainability, and clean energy projects."},
                        {"role": "user", "content": f"Give me a short summary of climate-related initiatives in {query}. Include key programs, organizations, or efforts."}
                    ],
                    temperature=0.6,
                    max_tokens=400
                )
                summary = response.choices[0].message.content.strip()
                st.subheader(f"🌱 AI-Generated Summary for: {query}")
                st.write(summary)
            except Exception as e:
                st.error(f"⚠️ Error generating info: {str(e)}")
    else:
        st.warning("⚠️ Please enter a project, city, or country first.")