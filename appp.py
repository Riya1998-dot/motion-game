import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(
    page_title="Energy AI",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy AI")
st.caption("Real-Time Electricity Usage Predictor")

# Live simulated electricity reading
power = round(random.uniform(2.0, 7.0), 2)

# Simulated daily consumption
daily_usage = round(random.uniform(18, 35), 2)

# Simple prediction
predicted_usage = round(daily_usage * random.uniform(1.05, 1.20), 2)

# Electricity rate
rate = 8

estimated_bill = round(predicted_usage * rate, 2)

# Status
if power < 3.5:
    status = "🟢 NORMAL"
elif power < 5.5:
    status = "🟠 MODERATE"
else:
    status = "🔴 HIGH USAGE"

# Dashboard
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Power",
    f"{power} kW"
)

col2.metric(
    "Today's Usage",
    f"{daily_usage} kWh"
)

col3.metric(
    "AI Prediction",
    f"{predicted_usage} kWh"
)

col4.metric(
    "Estimated Bill",
    f"₹{estimated_bill}"
)

st.divider()

st.subheader("🤖 AI Energy Analysis")

st.markdown(f"### {status}")

if power >= 5.5:
    st.warning(
        "AI detected high electricity consumption. "
        "Consider checking high-power appliances."
    )
elif power >= 3.5:
    st.info(
        "Electricity consumption is moderate. "
        "Continue monitoring the usage pattern."
    )
else:
    st.success(
        "Electricity consumption is currently normal."
    )

st.divider()

st.caption(
    f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
)

# Auto refresh
time.sleep(2)
st.rerun()
