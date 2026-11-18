import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"

# PAGE CONFIGURATION
st.set_page_config(
    page_title="HealSense AI",
    page_icon="🩺",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #07111f;
    color: #eaf4ff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #101e30;
}

[data-testid="stSidebar"] * {
    color: #eaf4ff !important;
}

/* Main headings */
h1, h2, h3 {
    color: #00d4ff !important;
}

/* Normal text */
p, label {
    color: #cbd8e6;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #14243a;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #203b56;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #9bb4cc !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #00d4ff !important;
}

/* Buttons */
.stButton > button {
    background-color: #00bcd4;
    color: #07111f;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    padding: 10px 20px;
}

.stButton > button:hover {
    background-color: #00e5ff;
    color: #07111f;
}

/* Divider */
hr {
    border-color: #29435e;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #203b56;
    border-radius: 10px;
}

/* Select box */
[data-baseweb="select"] > div {
    background-color: #14243a;
}

</style>
""", unsafe_allow_html=True)


# CHART THEME
def apply_dark_theme(fig):

    fig.update_layout(
        paper_bgcolor="#0b1728",
        plot_bgcolor="#0b1728",
        font=dict(
            color="#eaf4ff",
            family="Arial"
        ),
        title_font=dict(
            color="#00d4ff",
            size=20
        ),
        xaxis=dict(
            gridcolor="#203b56",
            zerolinecolor="#203b56"
        ),
        yaxis=dict(
            gridcolor="#203b56",
            zerolinecolor="#203b56"
        ),
        legend=dict(
            font=dict(color="#eaf4ff")
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


# SIDEBAR
st.sidebar.title("🩺 HealSense AI")
st.sidebar.caption("Intelligent Sensor Network")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Sensor Monitoring",
        "AI Diagnosis",
        "Self Healing",
        "Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("System Interface Active")


# BACKEND CONNECTION
def get_data(endpoint):

    try:
        response = requests.get(
            f"{API}/{endpoint}",
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        st.error(
            "Backend connection failed. "
            "Please start FastAPI."
        )

        return None


def post_data(endpoint):

    try:
        response = requests.post(
            f"{API}/{endpoint}",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        st.error("Unable to communicate with the backend.")

        return None


# DASHBOARD
if page == "Dashboard":

    st.title("🩺 HealSense AI")

    st.caption(
        "AI-Powered Self-Healing Sensor Network"
    )

    data = get_data("analytics")

    if data:

        st.subheader("Network Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Sensors",
            data["total_sensors"]
        )

        col2.metric(
            "Total Readings",
            data["total_readings"]
        )

        col3.metric(
            "Anomalies",
            data["anomalies"]
        )

        col4.metric(
            "Recovered",
            data["recovered_readings"]
        )

        st.markdown("---")

        st.subheader("📡 Sensor Network Overview")

        sensor_data = get_data("sensors")

        if sensor_data:

            df = pd.DataFrame(sensor_data["data"])

            fig = px.line(
                df,
                x="Timestamp",
                y="Reading",
                color="Sensor_ID",
                title="Sensor Reading Trends",
                template="plotly_dark"
            )

            fig = apply_dark_theme(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# SENSOR MONITORING
elif page == "Sensor Monitoring":

    st.title("📡 Sensor Monitoring")

    st.caption(
        "Monitor individual sensor readings and performance."
    )

    data = get_data("sensors")

    if data:

        df = pd.DataFrame(data["data"])

        st.metric(
            "Connected Sensors",
            data["total_sensors"]
        )

        st.markdown("---")

        sensor = st.selectbox(
            "Select Sensor",
            df["Sensor_ID"].unique()
        )

        filtered = df[
            df["Sensor_ID"] == sensor
        ]

        st.subheader(f"{sensor} Monitoring")

        fig = px.line(
            filtered,
            x="Timestamp",
            y="Reading",
            title=f"{sensor} Reading History",
            template="plotly_dark"
        )

        fig = apply_dark_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Sensor Reading Details")

        st.dataframe(
            filtered,
            use_container_width=True
        )


# AI DIAGNOSIS
elif page == "AI Diagnosis":

    st.title("🧠 AI Fault Diagnosis")

    st.caption(
        "Identify abnormal behaviour in the sensor network."
    )

    if st.button("Run Fault Diagnosis"):

        result = get_data("diagnose")

        if result:

            st.success(result["message"])

            report = pd.DataFrame(
                result["report"]
            )

            if not report.empty:

                st.subheader("Fault Diagnosis Report")

                st.dataframe(
                    report,
                    use_container_width=True
                )

            else:

                st.info("No faults detected.")


# SELF HEALING
elif page == "Self Healing":

    st.title("⚡ Self-Healing System")

    st.caption(
        "Recover abnormal sensor readings using AI-based "
        "data recovery."
    )

    st.markdown("---")

    if st.button("Start Self Healing"):

        result = post_data("heal")

        if result:

            st.success(result["message"])

            report = result["recovery_report"]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Faulty Readings",
                report["Total_Faulty_Readings"]
            )

            col2.metric(
                "Recovered Readings",
                report["Recovered_Readings"]
            )

            col3.metric(
                "Recovery Rate",
                f'{report["Recovery_Success_Rate"]}%'
            )

            st.markdown("---")

            st.subheader("Recovered Sensor Data")

            recovered = pd.DataFrame(
                result["recovered_data"]
            )

            st.dataframe(
                recovered,
                use_container_width=True
            )


# ANALYTICS
elif page == "Analytics":

    st.title("📊 Network Analytics")

    st.caption(
        "Visual analysis of sensor network performance."
    )

    data = get_data("analytics")

    if data:

        st.subheader("System Statistics")

        stats = pd.DataFrame({
            "Category": [
                "Normal Readings",
                "Anomalies",
                "Recovered Readings"
            ],

            "Count": [
                data["normal_readings"],
                data["anomalies"],
                data["recovered_readings"]
            ]
        })

        fig = px.bar(
            stats,
            x="Category",
            y="Count",
            color="Category",
            title="Sensor Network Performance",
            template="plotly_dark"
        )

        fig = apply_dark_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("Recovery Statistics")

        report = data["recovery_report"]

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Faults",
            report["Total_Faulty_Readings"]
        )

        col2.metric(
            "Recovery Success Rate",
            f'{report["Recovery_Success_Rate"]}%'
        )