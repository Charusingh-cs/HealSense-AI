
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    df = df.copy()

    df["Anomaly"] = 0

    # Analyse each sensor independently
    for sensor in df["Sensor_ID"].unique():

        mask = df["Sensor_ID"] == sensor

        readings = df.loc[mask, "Reading"]

        # Handle missing readings
        missing = readings.isna()

        df.loc[readings[missing].index, "Anomaly"] = 1

        # Select valid readings
        valid_readings = readings.dropna()

        if len(valid_readings) < 10:
            continue

        # Train Isolation Forest
        model = IsolationForest(
            n_estimators=100,
            contamination=0.08,
            random_state=42
        )

        predictions = model.fit_predict(
            valid_readings.values.reshape(-1, 1)
        )

        # -1 means anomaly, 1 means normal
        df.loc[valid_readings.index, "Anomaly"] = (
            predictions == -1
        ).astype(int)

    return df


if __name__ == "__main__":

    from .sensor_data import generate_sensor_data

    df = generate_sensor_data()

    result = detect_anomalies(df)

    print("AI Anomaly Detection Completed!")

    print("\nTotal abnormal readings:",
          result["Anomaly"].sum())

    print("\nSensor-wise anomaly report:")

    print(
        result.groupby("Sensor_ID")["Anomaly"].sum()
    )

    print("\nDetected abnormal readings:")

    print(
        result[result["Anomaly"] == 1][
            ["Sensor_ID", "Timestamp", "Reading", "Anomaly"]
        ].head(15)
    )
