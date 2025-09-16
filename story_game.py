import streamlit as st

# -------------------------
# Initialize session state
# -------------------------
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "role" not in st.session_state:
    st.session_state.role = None
if "eco_score" not in st.session_state:
    st.session_state.eco_score = 50  # start at neutral
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Helper functions
# -------------------------
def add_decision(text, score_change, fact=None):
    st.session_state.history.append(text)
    st.session_state.eco_score += score_change
    if st.session_state.eco_score < 0:
        st.session_state.eco_score = 0
    if st.session_state.eco_score > 100:
        st.session_state.eco_score = 100
    if fact:
        st.info(f"🌍 Fact: {fact}")

def go_to_step(step_name):
    st.session_state.step = step_name
    try:
        st.rerun()
    except AttributeError:  # backward compatibility
        st.experimental_rerun()

# -------------------------
# UI Header
# -------------------------
st.set_page_config(page_title="Climate Story Game", page_icon="🌱", layout="wide")
st.title("🌍 Interactive Climate Story Game")
st.write("Make choices to protect your world and learn about sustainability.")

st.progress(st.session_state.eco_score / 100)
st.caption(f"🌱 Eco Score: {st.session_state.eco_score}/100")

# -------------------------
# Story Steps
# -------------------------
if st.session_state.step == "intro":
    st.subheader("Welcome Hero!")
    st.write("Choose your role for this mission:")
    role = st.radio("Select your character:", ["Scientist", "Activist", "Mayor"])
    if st.button("Start Adventure 🚀"):
        st.session_state.role = role
        go_to_step("scene1")

elif st.session_state.step == "scene1":
    st.subheader("Scene 1: The Energy Crisis ⚡")
    st.write("Your city faces frequent blackouts. What will you propose?")
    if st.button("Build more coal plants"):
        add_decision("Built more coal plants", -20,
                     "Coal energy is the largest contributor to CO2 emissions.")
        go_to_step("scene2")
    if st.button("Invest in solar & wind farms"):
        add_decision("Invested in renewables", +20,
                     "Renewable energy reduces emissions and creates jobs.")
        go_to_step("scene2")

elif st.session_state.step == "scene2":
    st.subheader("Scene 2: Food Choices 🍔🥦")
    st.write("Dietary habits impact emissions. What campaign do you launch?")
    if st.button("Promote plant-based meals"):
        add_decision("Promoted plant-based meals", +15,
                     "Shifting to plant-based diets can cut food emissions by up to 50%.")
        go_to_step("scene3")
    if st.button("Encourage fast-food chains"):
        add_decision("Encouraged fast food", -15,
                     "Fast food often relies on high-emission meat production.")
        go_to_step("scene3")

elif st.session_state.step == "scene3":
    st.subheader("Scene 3: Transportation 🚗🚲")
    st.write("The city is clogged with traffic. What’s your solution?")
    if st.button("Expand highways for more cars"):
        add_decision("Expanded highways", -20,
                     "More roads = more cars = more emissions (induced demand).")
        go_to_step("ending")
    if st.button("Invest in public transport & cycling"):
        add_decision("Invested in public transport", +20,
                     "Public transport reduces emissions and congestion.")
        go_to_step("ending")

elif st.session_state.step == "ending":
    st.subheader("🌟 Your Climate Journey Ends Here")
    st.write("Here’s what you achieved as a", st.session_state.role)

    st.markdown("### 📝 Decisions You Made:")
    for i, d in enumerate(st.session_state.history, 1):
        st.write(f"{i}. {d}")

    st.progress(st.session_state.eco_score / 100)
    st.caption(f"Final Eco Score: {st.session_state.eco_score}/100")

    if st.session_state.eco_score >= 70:
        st.success("🎉 Amazing! Your city thrives in harmony with nature.")
    elif st.session_state.eco_score >= 40:
        st.warning("⚖️ Mixed outcomes. Some progress, but challenges remain.")
    else:
        st.error("💀 Disaster! Your city suffers from climate breakdown.")

    if st.button("🔄 Play Again"):
        st.session_state.step = "intro"
        st.session_state.eco_score = 50
        st.session_state.history = []
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()
