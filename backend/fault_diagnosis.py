import numpy as np
import pandas as pd


def diagnose_fault(group):

    readings = group.sort_values("Timestamp")["Reading"]

    # 1. Sensor disconnection
    if readings.isna().any():
        return "Sensor Disconnection"

    # 2. Stuck sensor
    if readings.nunique() <= 2:
        return "Stuck Sensor"

    mean = readings.mean()
    std = readings.std()

    # 3. Sudden spike
    if std > 0 and readings.max() > mean + 4 * std:
        return "Sudden Spike"

    # 4. Sudden drop
    if std > 0 and readings.min() < mean - 4 * std:
        return "Sudden Drop"

    # 5. Sensor drift
    if len(readings) > 10:

        first = readings.iloc[:5].mean()
        last = readings.iloc[-5:].mean()

        if abs(last - first) > 2 * std:
            return "Possible Sensor Drift"

    return "Abnormal Behaviour"


def get_fault_report(df):

    report = []

    for sensor, group in df.groupby("Sensor_ID"):

        faulty = group[group["Anomaly"] == 1]

        if len(faulty) > 0:

            fault_type = diagnose_fault(group)

            report.append({

                "Sensor_ID": sensor,

                "Sensor_Type": group["Sensor_Type"].iloc[0],

                "Fault_Type": fault_type,

                "Faulty_Readings": len(faulty),

                "Fault_Percentage": round(
                    len(faulty) / len(group) * 100, 2
                ),

                "Status": "Fault Detected"

            })

    return pd.DataFrame(report)


if __name__ == "__main__":

    from .sensor_data import generate_sensor_data
    from .anomaly_detection import detect_anomalies

    df = generate_sensor_data()

    df = detect_anomalies(df)

    report = get_fault_report(df)

    print("\nFAULT DIAGNOSIS REPORT")

    print(report.to_string(index=False))