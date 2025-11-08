import streamlit as st
import google.generativeai as genai
import math

# ---------- Gemini Setup ----------
GEMINI_API_KEY = "AIzaSyB-SDO4lq0qA9536gljSkXUhN96wojd9_4"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------- Streamlit UI ----------
st.title("💰 Personal Financial Planning Platform")

st.sidebar.header("📋 Enter Your Details")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, step=1000)
expenses = st.sidebar.number_input("Monthly Expenses (₹)", min_value=0, step=500)
goal_amount = st.sidebar.number_input("Savings Goal (₹)", min_value=1000, step=1000)
years = st.sidebar.number_input("Goal Timeline (in years)", min_value=1, max_value=50, step=1)
interest_rate = st.sidebar.number_input("Expected Annual Interest Rate (%)", min_value=0.0, max_value=50.0, step=0.1)

if st.sidebar.button("Calculate Plan"):
    st.subheader("📈 Financial Summary")

    monthly_saving = income - expenses
    months = years * 12
    rate_monthly = interest_rate / 100 / 12

    # Future Value of a series formula
    future_value = monthly_saving * (((1 + rate_monthly) ** months - 1) / rate_monthly) if rate_monthly > 0 else monthly_saving * months

    shortfall = max(0, goal_amount - future_value)
    enough = shortfall == 0

    st.markdown(f"**Monthly Saving Capacity:** ₹{monthly_saving:,.2f}")
    st.markdown(f"**Projected Savings in {years} years:** ₹{future_value:,.2f}")
    st.markdown(f"**Savings Goal:** ₹{goal_amount:,.2f}")
    
    if enough:
        st.success("🎉 You are on track to meet your goal!")
    else:
        st.warning(f"⚠️ You may fall short by ₹{shortfall:,.2f}. Consider increasing your monthly savings or extending your timeline.")

    # ---------- Gemini Chat Response ----------
    with st.spinner("Getting expert tips from Gemini..."):
        prompt = (
            f"My monthly income is ₹{income}, expenses are ₹{expenses}, and I want to save ₹{goal_amount} in {years} years. "
            f"Assuming an interest rate of {interest_rate}%, what suggestions do you have for better financial planning?"
        )
        try:
            response = model.generate_content(prompt)
            st.subheader("🤖 Gemini's Advice:")
            st.write(response.text)
        except Exception as e:
            st.error("Gemini API error: Please check your API key or network connection.")
