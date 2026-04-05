import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 🎨 UI STYLING
# -------------------------------
st.markdown("""
<style>

/* Page */
.stApp {
    background-color: #F2EAE4;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FAF6F2;
}

/* Header */
.header {
    font-size: 26px;
    font-weight: bold;
    color: #2D2D2D;
}

/* Card */
.card {
    background-color: #D9C9D4;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* Inner white */
.inner {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
}

/* Right panel cards */
.stat-card {
    background-color: #C4A8BC;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 15px;
}

/* Buttons */
.stButton>button {
    background-color: #B89BB0;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# STORAGE
# -------------------------------
if "health_logs" not in st.session_state:
    st.session_state.health_logs = []

# -------------------------------
# ANALYSIS
# -------------------------------
def analyze(data):
    risk = 0
    for d in data:
        if d["sleep"] < 5:
            risk += 30
        if d["mood"] <= 2:
            risk += 20
    return risk

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("💜 MediScan")
page = st.sidebar.radio("Menu", ["Input", "Dashboard"])

# -------------------------------
# INPUT PAGE
# -------------------------------
if page == "Input":

    st.title("Daily Check")

    sleep = st.slider("Sleep", 0, 12, 6)
    mood = st.slider("Mood", 1, 5, 3)

    if st.button("Submit"):
        st.session_state.health_logs.append({
            "sleep": sleep,
            "mood": mood
        })
        st.success("Saved!")

# -------------------------------
# DASHBOARD
# -------------------------------
else:

    st.markdown("<div class='header'>Hello User 👋</div>", unsafe_allow_html=True)

    data = st.session_state.health_logs

    if not data:
        st.warning("No data yet")
    else:
        df = pd.DataFrame(data)
        risk = analyze(data)

        # MAIN LAYOUT
        left, middle, right = st.columns([2,2,1])

        # LEFT COLUMN
        with left:
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown("### 📊 Health Summary")

            st.markdown("<div class='inner'>", unsafe_allow_html=True)
            st.metric("Risk Score", risk)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # GRAPH
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown("### 📈 Sleep Trend")

            plt.figure()
            plt.plot(df["sleep"])
            st.pyplot(plt)

            st.markdown("</div>", unsafe_allow_html=True)

        # MIDDLE COLUMN
        with middle:
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown("### 🧠 Insights")

            if risk > 70:
                st.error("High Risk")
            elif risk > 40:
                st.warning("Moderate Risk")
            else:
                st.success("Low Risk")

            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT COLUMN (LIKE IMAGE)
        with right:
            st.markdown("<div class='stat-card'>Attendance<br><h2>60%</h2></div>", unsafe_allow_html=True)
            st.markdown("<div class='stat-card'>Homework<br><h2>90%</h2></div>", unsafe_allow_html=True)
            st.markdown("<div class='stat-card'>Rating<br><h2>75%</h2></div>", unsafe_allow_html=True)
