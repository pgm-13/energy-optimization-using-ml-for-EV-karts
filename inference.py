import pandas as pd
import numpy as np
import joblib
import serial
import time

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

# LOAD MODELS
energy_model = joblib.load("energy_model.pkl")
driver_model = joblib.load("driver_model.pkl")

# SELECT LATEST LAP
latest_lap = lap_df.index.max()

energy_features = lap_df.loc[[latest_lap], ["distance", "energy"]]
driver_features = lap_df.loc[[latest_lap], ["avg_speed", "speed_consistency", "acc_variability"]]

energy_pred = energy_model.predict(energy_features)[0]
driver_pred = driver_model.predict(driver_features)[0]

# Normalize to 0-100
energy_score = 100 * (energy_pred - lap_df["raw_efficiency"].min()) / (
    lap_df["raw_efficiency"].max() - lap_df["raw_efficiency"].min()
)

driver_score = 100 * (driver_pred - raw_driver_score.min()) / (
    raw_driver_score.max() - raw_driver_score.min()
)

energy_score = np.clip(energy_score, 0, 100)
driver_score = np.clip(driver_score, 0, 100)

print("Energy Score:", int(energy_score))
print("Driver Score:", int(driver_score))

"""
# SEND TO ARDUINO
import serial
import time

energy_score = int(energy_score)
driver_score = int(driver_score)

ser = serial.Serial("COM4", 9600)
time.sleep(2)

ser.write(f"{energy_score},{driver_score}\n".encode())

ser.close()
"""

#SEND TO ARD AND ESP
import serial
import time

energy_score = int(energy_score)
driver_score = int(driver_score)

arduino = serial.Serial("COM4",9600)
esp32 = serial.Serial("COM3",9600)

time.sleep(2)

arduino.write(f"{energy_score},{driver_score}\n".encode())
esp32.write(f"{energy_score}\n".encode())

arduino.close()
esp32.close()