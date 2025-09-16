# carbon_footprint_tracker_app.py

import streamlit as st
import requests

# Optional: Climate news API (e.g., NewsAPI.org)
NEWS_API_KEY = "your_api_key_here"  # Replace with your key or leave empty

def get_climate_news():
    """Fetch latest climate news (if API key available)."""
    if not NEWS_API_KEY:
        return []
    try:
        url = f"https://newsapi.org/v2/everything?q=climate change&apiKey={NEWS_API_KEY}&pageSize=5"
        res = requests.get(url).json()
        articles = res.get("articles", [])
        return [{"title": a["title"], "url": a["url"]} for a in articles]
    except:
        return []

def calculate_footprint(km_driven, flights, electricity, meat_meals):
    """Calculate annual CO2 emissions (kg)."""
    car_emission = km_driven * 0.12 * 52
    flight_emission = flights * 250
    electricity_emission = electricity * 0.5 * 12
    diet_emission = meat_meals * 7 * 2.5 * 52
    return car_emission, flight_emission, electricity_emission, diet_emission

def footprint_tips(km_driven, flights, electricity, meat_meals):
    """Generate personalized tips."""
    tips = []
    if km_driven > 50:
        tips.append("🚲 Use public transport, cycle, or carpool to cut down car emissions.")
    if flights > 2:
        tips.append("✈️ Reduce air travel or choose trains for shorter trips.")
    if electricity > 200:
        tips.append("💡 Switch to energy-efficient appliances and renewable energy.")
    if meat_meals > 5:
        tips.append("🥗 Try adding more plant-based meals each week.")
    if not tips:
        tips.append("✅ You’re already keeping your footprint low. Great job!")
    return tips

# 🌍 Streamlit UI
st.set_page_config(page_title="Carbon Footprint Tracker", page_icon="🌍", layout="centered")

st.title("🌍 Carbon Footprint Tracker")
st.write("Estimate your annual carbon footprint and get personalized tips to reduce it.")

with st.form("footprint_form"):
    km_driven = st.number_input("🚗 Kilometers driven per week", min_value=0.0, step=1.0)
    flights = st.number_input("✈️ Flights (short-haul) per year", min_value=0, step=1)
    electricity = st.number_input("💡 Electricity use (kWh per month)", min_value=0.0, step=1.0)
    meat_meals = st.number_input("🍖 Meat-based meals per week", min_value=0, step=1)
    submitted = st.form_submit_button("Calculate Footprint")

if submitted:
    car, flight, elec, diet = calculate_footprint(km_driven, flights, electricity, meat_meals)
    total = car + flight + elec + diet

    st.subheader("📊 Your Annual Carbon Footprint")
    st.metric("Total Emissions", f"{total:,.0f} kg CO₂")

    # Breakdown chart
    st.write("### Emission Breakdown")
    st.bar_chart({
        "Emissions (kg CO₂)": {
            "Car": car,
            "Flights": flight,
            "Electricity": elec,
            "Diet": diet
        }
    })

    # Personalized tips
    st.write("### ✅ Tips to Reduce Your Footprint")
    for tip in footprint_tips(km_driven, flights, electricity, meat_meals):
        st.markdown(f"- {tip}")