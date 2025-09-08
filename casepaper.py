import streamlit as st
from datetime import datetime

# Dummy user database
users = {
    "drsmith": "password123",
    "drjones": "secure456"
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "on_lunch" not in st.session_state:
    st.session_state.on_lunch = False

# Function to handle login
def login():
    st.title("Doctor Login - CLOE System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()  # 👈 This refreshes the page and shows dashboard
        else:
            st.error("Invalid username or password.")

# Function to handle dashboard
def dashboard():
    st.subheader(f"👨‍⚕️ Doctor Dashboard - Dr. {st.session_state.username.capitalize()}")

    # Lunch break section
    st.markdown("### 🥪 Lunch Break")
    if st.session_state.on_lunch:
        if st.button("End Lunch Break"):
            st.session_state.on_lunch = False
            st.success("Lunch break ended at " + datetime.now().strftime("%I:%M %p"))
    else:
        if st.button("Start Lunch Break"):
            st.session_state.on_lunch = True
            st.info("You're now on lunch break as of " + datetime.now().strftime("%I:%M %p"))

    # Appointments (demo)
    st.markdown("### 📅 Today's Appointments")
    appointments = [
        {"time": "09:00 AM", "patient": "Alice Johnson"},
        {"time": "10:30 AM", "patient": "Bob Smith"},
        {"time": "01:00 PM", "patient": "Charlie Lee"},
    ]
    for appt in appointments:
        st.write(f"🕒 {appt['time']} - 👤 {appt['patient']}")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.on_lunch = False
        st.success("You have been logged out.")
        st.experimental_rerun()

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    dashboard()


