import streamlit as st
import pandas as pd
import plotly.express as px

from sensor_data import generate_sensor_data
from backend.anomaly_detection import detect_anomalies
from fault_diagnosis import get_fault_report
from backend.self_healing import self_heal


st.set_page_config(
    page_title="HealSense AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ HealSense AI")
st.subheader("AI-Powered Self-Healing Sensor Network")

st.write(
    "An intelligent system for sensor fault detection, "
    "diagnosis and automated data recovery."
)


# Generate data
if "data" not in st.session_state:

    st.session_state.data = generate_sensor_data()

    st.session_state.detected = False
    st.session_state.healed = False


df = st.session_state.data


# Sidebar
st.sidebar.title("Control Panel")

if st.sidebar.button("Generate New Sensor Data"):

    st.session_state.data = generate_sensor_data()

    st.session_state.detected = False
    st.session_state.healed = False

    st.rerun()


if st.sidebar.button("Run AI Fault Detection"):

    st.session_state.data = detect_anomalies(
        st.session_state.data
    )

    st.session_state.detected = True
    st.session_state.healed = False

    st.rerun()


if st.sidebar.button("Initiate Self-Healing"):

    if st.session_state.detected:

        st.session_state.data = self_heal(
            st.session_state.data
        )

        st.session_state.healed = True

    else:
        st.warning("Run fault detection first.")

    st.rerun()


df = st.session_state.data


# Metrics
total = df["Sensor_ID"].nunique()

faults = (
    int(df["Anomaly"].sum())
    if st.session_state.detected else 0
)

recovered = (
    int((df["Status"] == "Recovered").sum())
    if st.session_state.healed else 0
)

healthy = total - df[
    df["Anomaly"] == 1
]["Sensor_ID"].nunique() if st.session_state.detected else total


c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sensors", total)
c2.metric("Faulty Readings", faults)
c3.metric("Healthy Sensors", healthy)
c4.metric("Recovered Readings", recovered)


st.divider()


# Sensor Data
st.header("Live Sensor Monitoring")

st.dataframe(df, use_container_width=True)


# Graph
st.header("Sensor Reading Analysis")

selected = st.selectbox(
    "Select Sensor",
    df["Sensor_ID"].unique()
)

sensor_df = df[df["Sensor_ID"] == selected]

fig = px.line(
    sensor_df,
    x="Timestamp",
    y="Reading",
    title=f"{selected} Sensor Readings"
)

st.plotly_chart(fig, use_container_width=True)


# Fault Detection
if st.session_state.detected:

    st.header("AI Fault Detection")

    abnormal = df[df["Anomaly"] == 1]

    st.write("Detected abnormal readings:")

    st.dataframe(abnormal, use_container_width=True)

    report = get_fault_report(df)

    st.subheader("Fault Diagnosis Report")

    st.dataframe(
        pd.DataFrame(report),
        use_container_width=True
    )


# Self Healing
if st.session_state.healed:

    st.header("Self-Healing Report")

    st.success("Recovery simulation completed!")

    st.dataframe(
        df[df["Status"] == "Recovered"],
        use_container_width=True
    )

    st.subheader("Original vs Recovered Readings")

    fig2 = px.line(
        df[df["Sensor_ID"] == selected],
        x="Timestamp",
        y=["Reading", "Recovered_Value"],
        title="Sensor Recovery Analysis"
    )

    st.plotly_chart(fig2, use_container_width=True)


st.divider()

st.caption(
    "HealSense AI | Intelligent IoT Fault Detection and Recovery"
)