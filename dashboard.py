import streamlit as st
import pandas as pd
from database import query_latest
from processor import check_alert
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🌡 Live Temperature Monitoring System")

sensor_id = st.selectbox(
    "Select Sensor",
    ["sensor-01"],
    key="sensor"
)

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="refresh")

rows = query_latest(sensor_id, 20)

if rows:
    df = pd.DataFrame(rows, columns=rows[0].keys())
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")

    st.metric("🌡 Temperature", f"{df.iloc[0]['temperature']} °C")
    st.metric("💧 Humidity", f"{df.iloc[0]['humidity']} %")

    alert = check_alert(sensor_id)
    if "⚠" in alert:
        st.warning(alert)
    else:
        st.success(alert)

    st.line_chart(df.set_index("ts")["temperature"])
else:
    st.info("Waiting for sensor data...")