import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.read_csv("tele_data.csv")
data["power"] = data["v"] * data["i"]

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

# ENERGY MODEL
X_energy = lap_df[["distance", "energy"]]
y_energy = lap_df["raw_efficiency"]

energy_model = RandomForestRegressor(n_estimators=150, random_state=42)
energy_model.fit(X_energy, y_energy)

# DRIVER MODEL
X_driver = lap_df[["avg_speed", "speed_consistency", "acc_variability"]]
y_driver = raw_driver_score

driver_model = RandomForestRegressor(n_estimators=150, random_state=42)
driver_model.fit(X_driver, y_driver)

# SAVE MODELS
joblib.dump(energy_model, "energy_model.pkl")
joblib.dump(driver_model, "driver_model.pkl")

print("Models trained and saved successfully.")