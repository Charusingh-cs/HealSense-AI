from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from .sensor_data import generate_sensor_data
from .anomaly_detection import detect_anomalies
from .fault_diagnosis import get_fault_report
from .self_healing import self_heal, recovery_report


app = FastAPI(
    title="HealSense AI",
    description="AI-Powered Self-Healing Sensor Network",
    version="1.0"
)

# Generate sensor data
sensor_df = generate_sensor_data()

# Store processed data
detected_df = None
healed_df = None


def convert_to_json(df):
    return json.loads(df.to_json(orient="records"))


@app.get("/")
def home():
    return {
        "message": "HealSense AI Backend is Running",
        "status": "Online"
    }


@app.get("/sensors")
def get_sensors():
    return {
        "total_sensors": int(sensor_df["Sensor_ID"].nunique()),
        "total_readings": len(sensor_df),
        "data": convert_to_json(sensor_df)
    }


@app.post("/detect")
def detect():
    global detected_df

    detected_df = detect_anomalies(sensor_df)

    total_anomalies = int(detected_df["Anomaly"].sum())

    return {
        "message": "Anomaly Detection Completed",
        "total_anomalies": total_anomalies,
        "data": convert_to_json(detected_df)
    }


@app.get("/diagnose")
def diagnose():
    global detected_df

    if detected_df is None:
        detected_df = detect_anomalies(sensor_df)

    report = get_fault_report(detected_df)

    return {
        "message": "Fault Diagnosis Completed",
        "report": convert_to_json(report)
    }


@app.post("/heal")
def heal():
    global detected_df, healed_df

    if detected_df is None:
        detected_df = detect_anomalies(sensor_df)

    healed_df = self_heal(detected_df)

    report = recovery_report(healed_df)

    return {
        "message": "Self-Healing Completed",
        "recovery_report": report,
        "recovered_data": convert_to_json(
            healed_df[healed_df["Status"] == "Recovered"]
        )
    }


@app.get("/analytics")
def analytics():
    global detected_df, healed_df

    if detected_df is None:
        detected_df = detect_anomalies(sensor_df)

    if healed_df is None:
        healed_df = self_heal(detected_df)

    return {
        "total_sensors": int(sensor_df["Sensor_ID"].nunique()),
        "total_readings": len(sensor_df),
        "normal_readings": int(
            (detected_df["Anomaly"] == 0).sum()
        ),
        "anomalies": int(detected_df["Anomaly"].sum()),
        "recovered_readings": int(
            (healed_df["Status"] == "Recovered").sum()
        ),
        "recovery_report": recovery_report(healed_df)
    }