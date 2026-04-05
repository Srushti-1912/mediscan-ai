import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# In-memory storage (instead of Firebase)
# -------------------------------
if "health_logs" not in st.session_state:
    st.session_state.health_logs = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# -------------------------------
# AI LOGIC (Simple but effective)
# -------------------------------
def analyze_health(data):
    risk = 0
    insights = []

    for entry in data:
        if entry["sleep"] < 5:
            risk += 30
            insights.append("Low sleep detected")

        if entry["mood"] <= 2:
            risk += 20
            insights.append("Low mood pattern")

        if "Headache" in entry["symptoms"]:
            risk += 20

        if "Fever" in entry["symptoms"]:
            risk += 25

    diagnosis = "Normal"
    if risk > 70:
        diagnosis = "High fatigue / possible illness"
    elif risk > 40:
        diagnosis = "Moderate health risk"

    return {
        "risk_score": risk,
        "insights": list(set(insights)),
        "diagnosis": diagnosis,
        "alert": risk > 70
    }

# -------------------------------
# NAVIGATION
# -------------------------------
st.sidebar.title("MediScan AI")
page = st.sidebar.selectbox("Go to", ["User Input", "Dashboard", "Doctor Panel"])

# -------------------------------
# USER INPUT PAGE
# -------------------------------
if page == "User Input":
    st.title("🧾 Daily Health Check-in")

    sleep = st.slider("Sleep Hours", 0, 12, 6)
    mood = st.slider("Mood (1=Low, 5=High)", 1, 5, 3)
    symptoms = st.multiselect(
        "Symptoms",
        ["Fever", "Headache", "Cough", "Fatigue"]
    )

    if st.button("Submit"):
        data = {
            "sleep": sleep,
            "mood": mood,
            "symptoms": symptoms
        }

        st.session_state.health_logs.append(data)
        st.success("Data saved successfully!")

# -------------------------------
# DASHBOARD
# -------------------------------
elif page == "Dashboard":
    st.title("📊 Health Dashboard")

    data = st.session_state.health_logs

    if not data:
        st.warning("No data yet. Please enter health data first.")
    else:
        df = pd.DataFrame(data)

        # Analyze
        result = analyze_health(data)

        # Display metrics
        st.metric("Risk Score", result["risk_score"])
        st.write("### Diagnosis:", result["diagnosis"])

        st.write("### Insights:")
        for i in result["insights"]:
            st.write("-", i)

        # Plot sleep trend
        st.write("### Sleep Trend")
        plt.figure()
        plt.plot(df["sleep"])
        plt.xlabel("Entries")
        plt.ylabel("Sleep Hours")
        st.pyplot(plt)
        plt.clf()

        # ALERT SYSTEM
        if result["alert"]:
            alert_msg = {
                "message": "🚨 High Risk Patient Detected",
                "risk_score": result["risk_score"]
            }

            st.session_state.alerts.append(alert_msg)
            st.error("High Risk Detected! Doctor Alert Triggered 🚨")

# -------------------------------
# DOCTOR PANEL
# -------------------------------
elif page == "Doctor Panel":
    st.title("🩺 Doctor Dashboard")

    alerts = st.session_state.alerts

    if not alerts:
        st.success("No critical alerts 🎉")
    else:
        for i, alert in enumerate(alerts):
            st.warning(f"Patient {i+1}")
            st.write("Risk Score:", alert["risk_score"])
            st.write(alert["message"])

            if st.button(f"Call Patient {i+1}"):
                st.success("📞 Calling patient... (simulated)")
