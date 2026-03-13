import streamlit as st


def health_score(score: int):
    if score >= 85:
        st.success(f"Health Score: {score} (Low Risk)")
    elif score >= 70:
        st.warning(f"Health Score: {score} (Moderate Risk)")
    else:
        st.error(f"Health Score: {score} (High Risk)")


def alert_section(alerts: list[str]):
    st.subheader("Alerts")

    if not alerts:
        st.info("No alerts — startup looks stable.")
        return

    for message in alerts:
        if message.startswith("⛔"):
            st.error(message)
        elif message.startswith("⚠"):
            st.warning(message)
        else:
            st.info(message)
