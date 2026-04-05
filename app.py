import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# UI STYLING
# -------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #F2EAE4;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FAF6F2;
}

/* Big card */
.card {
    background-color: #D9C9D4;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* Inner white card */
.inner-card {
    background-color: #FFFFFF;
    padding: 15px;
    border-radius: 15px;
}

/* Text */
.title {
    color: #2D2D2D;
    font-size: 26px;
    font-weight: bold;
}

.subtext {
    color: #7A7A7A;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# In-memory storage
# -------------------------------
if "health_logs" not in st.session_state:
    st.session_state.health_logs = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# -------------------------------
# AI LOGIC
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
# USER INPUT
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

    st.markdown("<div class='title'>📊 Health Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Monitor your health insights</div>", unsafe_allow_html=True)

    data = st.session_state.health_logs

    if not data:
        st.warning("No data yet. Please enter health data first.")
    else:
        df = pd.DataFrame(data)
        result = analyze_health(data)

        # MAIN CARD
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='inner-card'>", unsafe_allow_html=True)
            st.markdown("### Risk Score")
            st.metric("", result["risk_score"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='inner-card'>", unsafe_allow_html=True)
            st.markdown("### Diagnosis")
            st.write(result["diagnosis"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # RISK COLOR
        risk = result["risk_score"]

        if risk < 40:
            st.markdown("<h4 style='color:#6DBFB8;'>● Low Risk</h4>", unsafe_allow_html=True)
        elif risk < 70:
            st.markdown("<h4 style='color:#E8C44A;'>● Moderate Risk</h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='color:#E07070;'>● High Risk</h4>", unsafe_allow_html=True)

        # INSIGHTS
        st.write("### Insights:")
        for i in result["insights"]:
            st.write("-", i)

        # GRAPH CARD
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("### Sleep Trend")

        plt.figure()
        plt.plot(df["sleep"])
        plt.xlabel("Entries")
        plt.ylabel("Sleep Hours")

        st.pyplot(plt)
        plt.clf()

        st.markdown("</div>", unsafe_allow_html=True)

        # ALERT
        if result["alert"]:
            alert_msg = {
                "message": "🚨 High Risk Patient Detected",
                "risk_score": result["risk_score"]
            }

            st.session_state.alerts.append(alert_msg)

            st.markdown("""
            <div style="
                background-color:#FFFFFF;
                padding:15px;
                border-radius:15px;
                border-left:6px solid #E07070;">
                <h4 style="color:#2D2D2D;">🚨 Critical Alert</h4>
                <p style="color:#7A7A7A;">Doctor has been notified.</p>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------
# DOCTOR PANEL
# -------------------------------
elif page == "Doctor Panel":

    st.markdown("<div class='title'>🩺 Doctor Dashboard</div>", unsafe_allow_html=True)

    alerts = st.session_state.alerts

    if not alerts:
        st.success("No critical alerts 🎉")
    else:
        for i, alert in enumerate(alerts):
            st.markdown(f"""
            <div style="
                background-color:#FFFFFF;
                padding:15px;
                border-radius:15px;
                border-left:6px solid #C4A8BC;
                margin-bottom:10px;">
                <h4>Patient {i+1}</h4>
                <p>Risk Score: {alert['risk_score']}</p>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
