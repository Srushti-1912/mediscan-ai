import streamlit as st
import pandas as pd

# -------------------------------
# 🎨 UI
# -------------------------------
st.markdown("""
<style>
.stApp {background-color: #F2EAE4;}
section[data-testid="stSidebar"] {background-color: #FAF6F2;}

.card {
    background: #D9C9D4;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.inner {
    background: #FFFFFF;
    padding: 15px;
    border-radius: 15px;
}
.stButton>button {
    background-color: #B89BB0;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STORAGE
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "data" not in st.session_state:
    st.session_state.data = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# -------------------------------
# LOGIN
# -------------------------------
if st.session_state.user is None:
    st.title("💜 MediScan Login")

    role = st.selectbox("Login as", ["Patient", "Doctor"])
    name = st.text_input("Enter your name")

    if st.button("Login"):
        st.session_state.user = name
        st.session_state.role = role
        st.rerun()

    st.stop()

# -------------------------------
# AI LOGIC
# -------------------------------
def analyze(entry):
    risk = 0
    action = "You're fine 😊"

    if entry["sleep"] < 5:
        risk += 30
        action = "Get proper sleep"

    if entry["mood"] <= 2:
        risk += 20
        action = "Relax and reduce stress"

    if entry["meal"] == "Skipped":
        risk += 20
        action = "Eat immediately"

    if "Fever" in entry["symptoms"]:
        risk += 25
        action = "Take rest + hydrate"

    if risk > 70:
        action = "🚨 Visit doctor immediately"

    return risk, action

# -------------------------------
# PATIENT DASHBOARD
# -------------------------------
if st.session_state.role == "Patient":

    st.title(f"Hello {st.session_state.user} 👋")

    sleep = st.slider("Sleep Hours", 0, 12, 6)
    mood = st.slider("Mood", 1, 5, 3)
    meal = st.selectbox("Meal Timing", ["On time", "Late", "Skipped"])
    symptoms = st.multiselect("Symptoms", ["Fever", "Headache", "Cough"])

    if st.button("Submit"):
        entry = {
            "name": st.session_state.user,
            "sleep": sleep,
            "mood": mood,
            "meal": meal,
            "symptoms": symptoms
        }

        risk, action = analyze(entry)

        entry["risk"] = risk
        entry["action"] = action

        st.session_state.data.append(entry)

        if risk > 70:
            st.session_state.alerts.append(entry)

        st.success("Data saved!")

    # SHOW RESULTS
    if st.session_state.data:
        latest = st.session_state.data[-1]

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("<div class='inner'>", unsafe_allow_html=True)
        st.metric("Risk Score", latest["risk"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("### Immediate Action")
        st.info(latest["action"])

        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# DOCTOR PANEL
# -------------------------------
elif st.session_state.role == "Doctor":

    st.title("🩺 Doctor Dashboard")

    st.write("### Working Hours")
    start = st.time_input("Start Time")
    end = st.time_input("End Time")

    st.success(f"Available: {start} - {end}")

    alerts = sorted(st.session_state.alerts, key=lambda x: x["risk"], reverse=True)

    if not alerts:
        st.success("No high-risk patients")
    else:
        for i, p in enumerate(alerts):

            st.markdown(f"""
            <div style="
                background:#FFFFFF;
                padding:15px;
                border-radius:15px;
                margin-bottom:10px;
                border-left:6px solid red;">
                <h4>{p['name']}</h4>
                <p>Risk: {p['risk']}</p>
                <p>Symptoms: {p['symptoms']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Call {p['name']}"):
                st.success("Calling patient...")

            prescription = st.text_input(f"Prescription for {p['name']}")

            if st.button(f"Save {p['name']}"):
                st.success("Prescription saved")
