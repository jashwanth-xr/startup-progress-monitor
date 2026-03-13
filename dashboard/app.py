import streamlit as st
import pandas as pd

from charts import revenue_chart, user_chart, burn_chart, momentum_chart
from components import health_score, alert_section

st.set_page_config(
    page_title="Startup Progress Monitor",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Startup Progress Monitor")

page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Startup Detail", "Leaderboard"]
)

# -----------------------------
# Sample startup datasets
# -----------------------------
startup_data = {

    "Zepto": {
        "month": ["Jan","Feb","Mar","Apr"],
        "revenue": [10000,15000,21000,26000],
        "users": [1000,1400,2000,2600],
        "burn_rate": [5000,6000,6500,7000],
        "score": 86
    },

    "Boat": {
        "month": ["Jan","Feb","Mar","Apr"],
        "revenue": [18000,20000,23000,24000],
        "users": [2200,2500,2700,3000],
        "burn_rate": [7000,7200,7300,7400],
        "score": 78
    },

    "CRED": {
        "month": ["Jan","Feb","Mar","Apr"],
        "revenue": [12000,14000,16000,17000],
        "users": [1500,1700,1900,2100],
        "burn_rate": [6500,6600,6700,6800],
        "score": 72
    },

    "Razorpay": {
        "month": ["Jan","Feb","Mar","Apr"],
        "revenue": [20000,24000,27000,32000],
        "users": [3000,3400,3800,4200],
        "burn_rate": [8000,8200,8500,8800],
        "score": 91
    }
}

# =============================
# Overview Page
# =============================
if page == "Overview":

    st.header("Startup Ecosystem Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Startups Monitored", len(startup_data))

    avg_score = sum(s["score"] for s in startup_data.values()) / len(startup_data)
    col2.metric("Average Health Score", round(avg_score))

    high_risk = sum(1 for s in startup_data.values() if s["score"] < 75)
    col3.metric("High Risk Startups", high_risk)

    compare = pd.DataFrame({
        "startup": list(startup_data.keys()),
        "growth": [85,60,55,90],
        "burn": [70,40,50,65]
    })

    fig = momentum_chart(compare)
    st.plotly_chart(fig, use_container_width=True)


# =============================
# Startup Detail Page
# =============================
elif page == "Startup Detail":

    st.header("Startup Performance")

    startup = st.selectbox(
        "Select Startup",
        list(startup_data.keys())
    )

    data = startup_data[startup]

    df = pd.DataFrame({
        "month": data["month"],
        "revenue": data["revenue"],
        "users": data["users"],
        "burn_rate": data["burn_rate"]
    })

    score = data["score"]

    # health score component
    health_score(score)

    # charts
    fig1 = revenue_chart(df)
    fig2 = user_chart(df)
    fig3 = burn_chart(df)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    st.plotly_chart(fig3, use_container_width=True)

    # alerts component
    alert_section(df)


# =============================
# Leaderboard Page
# =============================
elif page == "Leaderboard":

    st.header("Top Startups")

    leaderboard = pd.DataFrame({
        "Startup": list(startup_data.keys()),
        "Health Score": [s["score"] for s in startup_data.values()]
    }).sort_values(by="Health Score", ascending=False)

    st.dataframe(leaderboard, use_container_width=True)
