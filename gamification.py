import streamlit as st
import random
import datetime

# -----------------------------
# Initialize session state
# -----------------------------
if "points" not in st.session_state:
    st.session_state.points = 0
if "badges" not in st.session_state:
    st.session_state.badges = []
if "redeemed" not in st.session_state:
    st.session_state.redeemed = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_login" not in st.session_state:
    st.session_state.last_login = None

# -----------------------------
# Data
# -----------------------------
challenges = [
    "Go meatless for a day 🍃",
    "Cycle or walk instead of driving 🚲",
    "Turn off lights when not in use 💡",
    "Use a reusable water bottle ♻️",
    "Plant a tree 🌱",
    "Take a 5-min shower instead of 10 🚿",
    "Unplug devices when not in use 🔌",
]

rewards = {
    "Tree Planting Credit 🌳": 100,
    "Eco Badge 🏅": 50,
    "Reusable Bottle ♻️": 150,
    "Community Shoutout 📢": 200,
}

# -----------------------------
# Header
# -----------------------------
st.set_page_config(page_title="EcoGamify", page_icon="🌍", layout="wide")
st.title("🌍 EcoGamify – Gamification for Climate Action")

# -----------------------------
# Sidebar – User Dashboard
# -----------------------------
st.sidebar.header("Your Dashboard")
st.sidebar.write(f"🌱 Eco-Points: **{st.session_state.points}**")
st.sidebar.write(f"🏅 Badges: {', '.join(st.session_state.badges) if st.session_state.badges else 'None'}")
st.sidebar.write(f"🔥 Streak: {st.session_state.streak} days")

# -----------------------------
# Daily Login Streak
# -----------------------------
today = datetime.date.today()
if st.session_state.last_login != today:
    if st.session_state.last_login == today - datetime.timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.last_login = today
    st.session_state.points += 10
    st.success(f"✅ Daily Login Bonus! +10 points. Current streak: {st.session_state.streak} days")

# -----------------------------
# Section Navigation
# -----------------------------
menu = st.radio("Choose a section:", ["🎯 Daily Challenge", "🏫 Leaderboard", "🎁 Reward Shop", "📅 Weekly Challenge", "💬 Community Board"])

# -----------------------------
# Daily Challenge
# -----------------------------
if menu == "🎯 Daily Challenge":
    st.subheader("🌱 Today's Eco-Challenge")
    challenge = random.choice(challenges)
    st.info(challenge)

    if st.button("✅ Mark as Completed"):
        st.session_state.points += 20
        st.session_state.badges.append("Eco-Warrior")
        st.success("Great job! You earned +20 points and an Eco-Warrior badge! 🏅")

# -----------------------------
# Leaderboard
# -----------------------------
elif menu == "🏫 Leaderboard":
    st.subheader("🏆 Community Leaderboard")
    leaderboard = {
        "Green School": 820,
        "Eco Club": 740,
        "Climate Warriors": 690,
        "You": st.session_state.points
    }
    sorted_lb = dict(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True))
    for name, score in sorted_lb.items():
        st.write(f"{name}: {score} points")

# -----------------------------
# Reward Shop
# -----------------------------
elif menu == "🎁 Reward Shop":
    st.subheader("🎁 Reward Shop")
    for reward, cost in rewards.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{reward} - {cost} points")
        with col2:
            if st.button(f"Redeem {reward}", key=reward):
                if st.session_state.points >= cost:
                    st.session_state.points -= cost
                    st.session_state.redeemed.append(reward)
                    st.success(f"🎉 You redeemed {reward}!")
                else:
                    st.error("Not enough points!")

    if st.session_state.redeemed:
        st.subheader("🛒 Redeemed Items")
        for item in st.session_state.redeemed:
            st.write(f"- {item}")

# -----------------------------
# Weekly Challenge
# -----------------------------
elif menu == "📅 Weekly Challenge":
    st.subheader("📅 This Week's Challenge")
    weekly_challenge = "Organize a community clean-up event 🧹"
    st.info(weekly_challenge)

    if st.button("✅ Mark Weekly Challenge Completed"):
        st.session_state.points += 100
        st.session_state.badges.append("Community Hero")
        st.success("Amazing! You earned +100 points and a Community Hero badge! 🌟")

# -----------------------------
# Community Board
# -----------------------------
elif menu == "💬 Community Board":
    st.subheader("💬 Eco Community Board")
    st.write("Share your eco-achievements and inspire others!")

    post = st.text_input("Write your post:")
    if st.button("📢 Post"):
        if "posts" not in st.session_state:
            st.session_state.posts = []
        st.session_state.posts.append(post)
        st.success("Posted successfully!")

    if "posts" in st.session_state and st.session_state.posts:
        st.subheader("🌍 Community Posts")
        for p in reversed(st.session_state.posts):
            st.write(f"🔹 {p}")
