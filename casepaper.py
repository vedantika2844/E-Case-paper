import streamlit as st
import sqlite3
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
    DB Utility Functions ---
def get_connection():
    return sqlite3.connect('patients.db')

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM patients")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def get_patient_info(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT age, condition, last_visit FROM patients WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"Age": row[0], "Condition": row[1], "Last Visit": row[2]}
    return None

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
    tab1, tab2 = st.tabs(["📝 All Patients", "📋 Patient Information"])

    # --- Tab 1: All Patients ---
    with tab1:
        st.markdown("### 🧑‍🤝‍🧑 Patient List")
        appointments = [
            {"time": "09:00 AM", "patient": "Dev"},
            {"time": "10:30 AM", "patient": "Bob Smith"},
            {"time": "01:00 PM", "patient": "Charlie Lee"},
        ]
        for appt in appointments:
            st.write(f"👤 {appt['patient']}")

    # --- Tab 2: Patient Info ---
    with tab2:
        st.markdown("### 🧾 Patient Information")
        patient_name = st.selectbox(
            "Select a patient to view information:",
            ["Dev", "Bob Smith", "Charlie Lee"]
        )

        # Dummy patient data
        patient_info = {
            "Dev": {"Age": 30, "Condition": "Flu", "Last Visit": "2025-09-01"},
            "Riya": {"Age": 45, "Condition": "Diabetes", "Last Visit": "2025-08-25"},
            "Anu": {"Age": 50, "Condition": "Hypertension", "Last Visit": "2025-08-30"},
        }

        if patient_name:
            info = patient_info[patient_name]
            st.write(f"**Name:** {patient_name}")
            st.write(f"**Age:** {info['Age']}")
            st.write(f"**Condition:** {info['Condition']}")
            st.write(f"**Last Visit:** {info['Last Visit']}")

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
        {"time": "09:00 AM", "patient": "dev"},
        {"time": "10:30 AM", "patient": "Riya"},
        {"time": "01:00 PM", "patient": "Anu"},
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
