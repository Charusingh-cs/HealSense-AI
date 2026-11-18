import pandas as pd
import numpy as np


def generate_sensor_data():

    np.random.seed(42)

    sensors = {
        "S1": ["Temperature", 30, 3],
        "S2": ["Humidity", 55, 8],
        "S3": ["Pressure", 1000, 10],
        "S4": ["Gas", 300, 30],
        "S5": ["Vibration", 5, 1],
        "S6": ["Temperature", 32, 3],
        "S7": ["Humidity", 60, 8],
        "S8": ["Pressure", 990, 10],
        "S9": ["Gas", 250, 30],
        "S10": ["Vibration", 4, 1]
    }

    data = []

    for sensor_id, values in sensors.items():

        sensor_type, mean, std = values

        readings = np.random.normal(mean, std, 100)

        for i in range(100):

            data.append({
                "Sensor_ID": sensor_id,
                "Sensor_Type": sensor_type,
                "Timestamp": i,
                "Reading": readings[i],
                "Injected_Fault": "Normal"
            })

    df = pd.DataFrame(data)

    # 1. Sudden spike
    mask = (
        (df["Sensor_ID"] == "S1") &
        (df["Timestamp"].between(20, 25))
    )

    df.loc[mask, "Reading"] = 150
    df.loc[mask, "Injected_Fault"] = "Sudden Spike"

    # 2. Sensor drift
    mask = (
        (df["Sensor_ID"] == "S2") &
        (df["Timestamp"].between(50, 70))
    )

    df.loc[mask, "Reading"] += np.linspace(
        0, 50, mask.sum()
    )

    df.loc[mask, "Injected_Fault"] = "Sensor Drift"

    # 3. Sensor disconnection
    mask = (
        (df["Sensor_ID"] == "S3") &
        (df["Timestamp"].between(40, 45))
    )

    df.loc[mask, "Reading"] = np.nan
    df.loc[mask, "Injected_Fault"] = "Disconnection"

    # 4. Stuck sensor
    mask = (
        (df["Sensor_ID"] == "S4") &
        (df["Timestamp"].between(60, 75))
    )

    df.loc[mask, "Reading"] = 400
    df.loc[mask, "Injected_Fault"] = "Stuck Sensor"

    return df


if __name__ == "__main__":

    df = generate_sensor_data()

    df.to_csv("backend/sensor_data.csv", index=False)

    print("Synthetic sensor data generated!")
    print("Total sensors:", df["Sensor_ID"].nunique())
    print("Total readings:", len(df))

    print("\nFault distribution:")
    print(df["Injected_Fault"].value_counts())

    print("\nDataset preview:")
    print(df.head())