import streamlit as st
import plotly.graph_objects as go

from app.monitoring.system_monitor import SystemMonitor

if "logged_in" not in st.session_state:
    st.error("Please Login")
    st.stop()

allowed = [
    "Admin",
    "Manager"
]

if st.session_state.role not in allowed:
    st.error("Access Denied")
    st.stop()

st.set_page_config(
    page_title="System Health",
    layout="wide"
)
st.title("🖥 Enterprise System Health Dashboard")
st.divider()

monitor = SystemMonitor()
cpu = monitor.cpu_usage()
memory = monitor.memory_usage()
disk = monitor.disk_usage()

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "CPU",
        f"{cpu}%"
    )

with col2:
    st.metric(
        "Memory",
        f"{memory}%"
    )

with col3:
    st.metric(
        "Disk",
        f"{disk}%"
    )

st.subheader("Services")
services = {
    "FastAPI": monitor.fastapi_status(),
    "MongoDB": monitor.mongodb_status(),
    "ML Model": monitor.model_status(),
    "Groq AI": monitor.groq_status()
}
st.table(services)
def gauge(title, value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0,100]
                }
            }
        )
    )
    return fig

st.plotly_chart(
    gauge("CPU", cpu),
    use_container_width=True
)

st.plotly_chart(
    gauge("Memory", memory),
    use_container_width=True
)

st.plotly_chart(
    gauge("Disk", disk),
    use_container_width=True
)
st.subheader("Environment")
st.json(
    {
        "Python": monitor.python_version(),
        "Operating System": monitor.operating_system(),
        "Model": monitor.model_status(),
        "Groq": monitor.groq_status()
    }
)

if st.button(
    "🔄 Refresh Dashboard"

):
    st.rerun()
