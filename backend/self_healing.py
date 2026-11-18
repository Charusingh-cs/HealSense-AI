import pandas as pd
import numpy as np


def self_heal(df):

    df = df.copy()

    # Preserve original readings
    df["Original_Reading"] = df["Reading"]

    # Create recovered readings
    df["Recovered_Value"] = df["Reading"]

    df["Status"] = "Healthy"

    for sensor in df["Sensor_ID"].unique():

        mask = df["Sensor_ID"] == sensor

        group = df.loc[mask].sort_values("Timestamp")

        readings = group["Reading"]

        # Identify faulty readings
        faulty = (
            (group["Anomaly"] == 1) |
            (readings.isna())
        )

        faulty_indices = group.index[faulty]

        # Estimate replacement values
        for index in faulty_indices:

            position = group.index.get_loc(index)

            start = max(0, position - 5)
            end = min(len(group), position + 6)

            nearby_values = group.iloc[start:end]["Reading"]

            nearby_values = nearby_values.dropna()

            if len(nearby_values) > 0:
                recovered = nearby_values.median()

            else:
                recovered = readings.median()

            df.loc[index, "Recovered_Value"] = recovered

            df.loc[index, "Status"] = "Recovered"

    return df


def recovery_report(df):

    total_faults = int((df["Anomaly"] == 1).sum())

    recovered = int(
        (df["Status"] == "Recovered").sum()
    )

    success_rate = (
        recovered / total_faults * 100
        if total_faults > 0 else 0
    )

    return {
        "Total_Faulty_Readings": total_faults,
        "Recovered_Readings": recovered,
        "Recovery_Success_Rate": round(success_rate, 2)
    }


if __name__ == "__main__":

    from .sensor_data import generate_sensor_data
    from .anomaly_detection import detect_anomalies

    df = generate_sensor_data()

    df = detect_anomalies(df)

    healed_df = self_heal(df)

    report = recovery_report(healed_df)

    print("\nSELF-HEALING REPORT")

    print(report)

    print("\nRECOVERED SENSOR READINGS")

    print(
        healed_df[
            healed_df["Status"] == "Recovered"
        ][
            ["Sensor_ID", "Timestamp",
             "Original_Reading", "Recovered_Value", "Status"]
        ].head(15)
    )