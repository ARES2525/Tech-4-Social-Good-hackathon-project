import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------
# Helper functions
# -------------------------

def calculate_footprint(miles, meat_meals, electricity, waste_kg):
    # Very simplified emission factors (tons CO2e/year)
    transport = miles * 0.000404 * 365   # 0.404 kg CO₂ per mile (car)
    diet = meat_meals * 1.5 * 52         # 1.5 kg CO₂ per meat meal
    energy = electricity * 0.92 * 12     # 0.92 kg CO₂ per kWh
    waste = waste_kg * 0.002 * 52        # 2 g CO₂ per kg waste (weekly)

    total = (transport + diet + energy + waste) / 1000  # convert kg → tons
    breakdown = {
        "Transport": transport / 1000,
        "Diet": diet / 1000,
        "Energy": energy / 1000,
        "Waste": waste / 1000
    }
    return total, breakdown

def eco_tips(breakdown):
    tips = []
    if breakdown["Transport"] > 2:
        tips.append("🚲 Try biking, public transport, or carpooling to cut transport emissions.")
    if breakdown["Diet"] > 1.5:
        tips.append("🥗 Reduce red meat meals — even 1 less meal per week makes impact.")
    if breakdown["Energy"] > 2:
        tips.append("💡 Switch to LED bulbs, unplug devices, and explore renewable energy.")
    if breakdown["Waste"] > 0.5:
        tips.append("♻️ Reduce single-use plastics, compost organic waste.")
    if not tips:
        tips.append("🌍 Great job! You're already eco-friendly. Keep inspiring others.")
    return tips

# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(page_title="🌍 Personal Climate Dashboard", layout="wide")

st.title("🌍 Personal Climate Dashboard")
st.write("Estimate your carbon footprint and learn how to live more sustainably.")

# User Inputs
st.sidebar.header("Your Lifestyle Data")
miles = st.sidebar.number_input("Daily travel (miles)", 0, 200, 20)
meat_meals = st.sidebar.number_input("Meat meals per week", 0, 21, 7)
electricity = st.sidebar.number_input("Monthly electricity use (kWh)", 0, 2000, 300)
waste_kg = st.sidebar.number_input("Weekly waste produced (kg)", 0, 100, 10)

# Calculate Footprint
total, breakdown = calculate_footprint(miles, meat_meals, electricity, waste_kg)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Your Annual Carbon Footprint")
    st.metric("Total CO₂", f"{total:.2f} tons/year")

    avg_world = 4.5   # tons/person
    target_paris = 2.0
    st.write(f"🌍 World Average: **{avg_world} tons**")
    st.write(f"🎯 Paris Agreement Target: **{target_paris} tons**")

    if total > avg_world:
        st.error("Your footprint is above the world average. Time for action! 🚀")
    elif total > target_paris:
        st.warning("You're below world average but above the Paris target.")
    else:
        st.success("Amazing! You're within the Paris climate goal. 🌱")

with col2:
    st.subheader("📊 Emission Breakdown")
    df = pd.DataFrame(list(breakdown.items()), columns=["Category", "Tons CO₂"])
    fig, ax = plt.subplots()
    ax.pie(df["Tons CO₂"], labels=df["Category"], autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)

# Extra visualization
st.subheader("📈 Category Comparison")
st.bar_chart(df.set_index("Category"))

# Eco Tips
st.subheader("💡 Personalized Eco-Tips")
tips = eco_tips(breakdown)
for tip in tips:
    st.write(tip)
