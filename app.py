import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Go-Kart ML Dashboard", layout="centered")

st.title("Electric Go-Kart Performance Dashboard")

# Load telemetry data
data = pd.read_csv("tele_data.csv")
data["power"] = data["v"] * data["i"]

# Aggregate lap-wise features
lap_df = data.groupby("lap_id").agg(
    distance=("speed", "sum"),
    energy=("power", "sum"),
    avg_speed=("speed", "mean"),
    speed_consistency=("speed", "std"),
    acc_variability=("acceleration", "std")
)

lap_df.fillna(0, inplace=True)

lap_df["raw_efficiency"] = lap_df["distance"] / lap_df["energy"]

raw_driver_score = (
    0.4 * lap_df["avg_speed"]
    - 0.3 * lap_df["speed_consistency"]
    - 0.3 * lap_df["acc_variability"]
)

# Load trained models
energy_model = joblib.load("energy_model.pkl")
driver_model = joblib.load("driver_model.pkl")

# Lap selector
available_laps = lap_df.index.tolist()
selected_lap = st.selectbox("Select Lap", available_laps)

# Prepare features
energy_features = lap_df.loc[[selected_lap], ["distance", "energy"]]
driver_features = lap_df.loc[[selected_lap], ["avg_speed", "speed_consistency", "acc_variability"]]

# Predictions
energy_pred = energy_model.predict(energy_features)[0]
driver_pred = driver_model.predict(driver_features)[0]

# Normalize to 0–100
energy_score = 100 * (energy_pred - lap_df["raw_efficiency"].min()) / (
    lap_df["raw_efficiency"].max() - lap_df["raw_efficiency"].min()
)

driver_score = 100 * (driver_pred - raw_driver_score.min()) / (
    raw_driver_score.max() - raw_driver_score.min()
)

energy_score = np.clip(energy_score, 0, 100)
driver_score = np.clip(driver_score, 0, 100)

# -------- DRIVER STRATEGY (MATCHES YOUR ARDUINO CODE) --------

if driver_score >= 90:
    driver_strategy = "Push Hard on Straights"
elif driver_score >= 75:
    driver_strategy = "Increase Exit Speed"
elif driver_score >= 50:
    driver_strategy = "Improve Corner Flow"
elif driver_score >= 30:
    driver_strategy = "Reduce Steering Corrections"
else:
    driver_strategy = "Try smoother Inputs & Control"

# -------- ENERGY MODE (MATCHES YOUR TFT LOGIC) --------

if energy_score >= 80:
    energy_mode = "Full Performance Mode"
elif energy_score >= 60:
    energy_mode = "Mild Restriction"
elif energy_score >= 40:
    energy_mode = "Energy Protection Mode"
else:
    energy_mode = "Critical Energy Mode"

# -------- DISPLAY --------

st.subheader(f"Lap {selected_lap} Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Energy Efficiency Score", f"{int(energy_score)}")

with col2:
    st.metric("Driver Performance Score", f"{int(driver_score)}")

st.markdown("---")

st.subheader("Energy Mode")
st.info(energy_mode)

st.subheader("Driver Strategy Recommendation")
st.success(driver_strategy)

st.markdown("---")

st.subheader("Lap Metrics")

st.write("Distance Covered:", round(lap_df.loc[selected_lap, "distance"], 2))
st.write("Energy Used:", round(lap_df.loc[selected_lap, "energy"], 2))
st.write("Average Speed:", round(lap_df.loc[selected_lap, "avg_speed"], 2))
st.write("Speed Consistency:", round(lap_df.loc[selected_lap, "speed_consistency"], 2))
st.write("Acceleration Variability:", round(lap_df.loc[selected_lap, "acc_variability"], 2))