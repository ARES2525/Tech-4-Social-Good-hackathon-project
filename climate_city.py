# climate_hub.py

import os
import streamlit as st
import requests
from dotenv import load_dotenv

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --------------------------
# Streamlit app setup
# --------------------------
st.set_page_config(page_title="Climate Hub 🌱", page_icon="🌍", layout="wide")

# --------------------------
# Custom CSS for climate theme
# --------------------------
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(to right, #a8e063, #56ab2f);
}

/* Main title styling */
h1 {
    color: #ffffff;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    text-shadow: 2px 2px 4px #000000;
}

/* Subheader styling */
h2, h3 {
    color: #f0f9f0;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #2e7d32;
    color: white;
}

/* Buttons */
.stButton>button {
    background-color: #4caf50;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #81c784;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Page content
# --------------------------
st.title("🌍 Climate Hub")
st.subheader("Track your local climate, learn eco-friendly tips, and take action!")

# Sidebar settings
st.sidebar.header("📌 Quick Actions")
feature = st.sidebar.radio(
    "Choose a feature:",
    ["Local Climate Dashboard", "Environmental Tips", "Gamification Challenges"]
)

# 1️⃣ Local Climate Dashboard
if feature == "Local Climate Dashboard":
    st.header("📊 Local Climate Data Dashboard")
    st.write("Fetch current weather and temperature trends for your city.")

    city = st.text_input("Enter city", "Delhi")

    if st.button("Fetch Climate Data"):
        if not OPENWEATHER_API_KEY:
            st.error("❌ OpenWeatherMap API key is missing! Please set it in your .env file or environment variables.")
        else:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
                resp = requests.get(url).json()

                if resp.get("cod") != 200:
                    st.error(f"API Error: {resp.get('message', 'Unknown error')}")
                else:
                    st.write(f"🌡️ Temperature: {resp['main']['temp']}°C")
                    st.write(f"💨 Wind Speed: {resp['wind']['speed']} m/s")
                    st.write(f"🌫️ Weather: {resp['weather'][0]['description'].title()}")
                    st.write(f"📍 Location: {resp['name']}, {resp['sys']['country']}")
            except Exception as e:
                st.error(f"Error fetching data: {e}")

# 2️⃣ Environmental Tips
elif feature == "Environmental Tips":
    st.header("🌱 Eco-Friendly Tips")
    tips = [
        "Reduce single-use plastic and recycle properly.",
        "Use energy-efficient LED lights and appliances.",
        "Plant trees in your local community.",
        "Conserve water: fix leaks and use water-saving devices.",
        "Walk, cycle, or use public transport instead of cars.",
        "Compost kitchen waste to reduce landfill usage."
    ]
    for tip in tips:
        st.markdown(f"- {tip}")

# 3️⃣ Gamification Challenges
elif feature == "Gamification Challenges":
    st.header("🎮 Climate Gamification")
    st.write("Complete these eco-friendly challenges and track your impact:")

    challenges = {
        "Plant a tree": "Reward: 10 points",
        "Reduce plastic use for a week": "Reward: 20 points",
        "Use public transport for 3 days": "Reward: 15 points",
        "Organize a community cleanup": "Reward: 25 points"
    }

    for challenge, reward in challenges.items():
        if st.button(f"Mark '{challenge}' as done"):
            st.success(f"✅ {challenge} completed! {reward} earned.")

# Suggested Actions
st.markdown("---")
st.markdown("💡 **Suggested Actions:**")
examples = [
    "Check local air quality before outdoor activities.",
    "Track your weekly energy consumption.",
    "Participate in a local tree planting drive.",
    "Organize a neighborhood cleanup."
]
for ex in examples:
    st.code(ex, language="text")

st.markdown("🌱 *Powered by OpenWeatherMap & Climate Hub*")