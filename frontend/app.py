import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# ================= CONFIG =================
st.set_page_config(
    page_title="Wellness Dashboard",
    page_icon="🧘",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

# ================= SESSION =================
if "token" not in st.session_state:
    st.session_state.token = None


# ================= SAFE HELPERS =================
def safe_fetch(endpoint, headers):
    """Fetch API data safely"""
    try:
        res = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


def to_dataframe(data):
    """Convert API response to DataFrame safely"""
    if isinstance(data, dict):
        return pd.DataFrame([data])   # scalar-safe
    if isinstance(data, list):
        return pd.DataFrame(data)
    return pd.DataFrame()


def safe_datetime(df):
    """Convert created_at if exists"""
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df


def apply_filter(df, period):
    """Apply Weekly / Monthly filter safely"""
    if df.empty or "created_at" not in df.columns:
        return df

    now = datetime.now()

    if period == "Weekly":
        return df[df["created_at"] >= now - timedelta(days=7)]
    if period == "Monthly":
        return df[df["created_at"] >= now - timedelta(days=30)]

    return df


# ================= LOGIN =================
def login():
    st.title("🧘 Wellness Manager")
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/auth/login",
                data={"username": email, "password": password}
            )

            if res.status_code == 200:
                st.session_state.token = res.json().get("access_token")
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
        except Exception as e:
            st.error("Backend not reachable")


# ================= LOGOUT =================
def logout():
    st.session_state.token = None
    st.rerun()


# ================= DASHBOARD =================
def dashboard():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # -------- SIDEBAR --------
    with st.sidebar:
        st.title("🧘 Wellness")
        st.markdown("---")

        period = st.radio("📅 Filter", ["All", "Weekly", "Monthly"])

        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()

    st.title("📊 Wellness Overview")

    

    # -------- FETCH DATA --------
    sleep_data = safe_fetch("/sleep/", headers)
    exercise_data = safe_fetch("/exercise/", headers)
    mood_data = safe_fetch("/mood/", headers)

    df_sleep = safe_datetime(to_dataframe(sleep_data))
    df_ex = safe_datetime(to_dataframe(exercise_data))
    df_mood = safe_datetime(to_dataframe(mood_data))

    df_sleep = apply_filter(df_sleep, period)
    df_ex = apply_filter(df_ex, period)
    df_mood = apply_filter(df_mood, period)
    
    
    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_sleep = (
            df_sleep["duration_hours"].mean()
            if "duration_hours" in df_sleep.columns and not df_sleep.empty
            else 0
        )
        st.metric("😴 Avg Sleep (hrs)", round(avg_sleep, 1))

    with col2:
        total_ex = (
            df_ex["duration_minutes"].sum()
            if "duration_minutes" in df_ex.columns and not df_ex.empty
            else 0
        )
        st.metric("🏃 Total Exercise (min)", int(total_ex))

    with col3:
        avg_mood = (
            df_mood["mood_score"].mean()
            if "mood_score" in df_mood.columns and not df_mood.empty
            else 0
        )
        st.metric("🙂 Avg Mood", round(avg_mood, 1))

    st.markdown("---")

    # -------- GRAPHS --------
    colA, colB = st.columns(2)

    with colA:
        st.subheader("😴 Sleep Duration Trend")
        if {"created_at", "duration_hours"}.issubset(df_sleep.columns):
            st.line_chart(df_sleep.set_index("created_at")["duration_hours"])
        else:
            st.info("No sleep trend data available")

    with colB:
        st.subheader("🏃 Exercise Trend")
        if {"created_at", "duration_minutes"}.issubset(df_ex.columns):
            st.bar_chart(df_ex.set_index("created_at")["duration_minutes"])
        else:
            st.info("No exercise data available")

    st.markdown("---")

    # -------- MOOD GRAPH --------
    st.subheader("🙂 Mood Trend")
    if {"created_at", "mood_score"}.issubset(df_mood.columns):
        st.line_chart(df_mood.set_index("created_at")["mood_score"])
    else:
        st.info("No mood data available")

    # -------- AI INSIGHTS --------
    st.markdown("---")
    st.subheader("🤖 AI Wellness Insights")

    insights = []

    if avg_sleep and avg_sleep < 7:
        insights.append("😴 Try to get at least 7–8 hours of sleep.")

    if total_ex and total_ex < 150:
        insights.append("🏃 Aim for 150 minutes of exercise per week.")

    if avg_mood and avg_mood < 3:
        insights.append("🙂 Mood seems low. Consider relaxation or talking to someone.")

    if insights:
        for msg in insights:
            st.success(msg)
    else:
        st.success("🌟 You are maintaining a healthy lifestyle!")


# ================= MAIN =================
if st.session_state.token is None:
    login()
else:
    dashboard()