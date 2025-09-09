import streamlit as st
import mysql.connector
from datetime import datetime

# --- DB CONNECTION ---
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students"
    )

def insert_e_case(rfid, date_time, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO E_Case (RFID_No, Date_Time, Status) VALUES (%s, %s, %s)", (rfid, date_time, status))
    conn.commit()
    conn.close()

def update_e_case(case_id, rfid, date_time, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE E_Case SET RFID_No = %s, Date_Time = %s, Status = %s WHERE id = %s", (rfid, date_time, status, case_id))
    conn.commit()
    conn.close()

def get_all_e_cases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM E_Case")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, rows

# --- DASHBOARD FUNCTION ---
def dashboard():
    st.subheader(f"👨‍⚕️ Doctor Dashboard - Dr. {st.session_state.username.capitalize()}")

    tab1, tab2, tab3 = st.tabs(["📝 All Patients", "📋 Patient Information", "📥 E_Case Records"])

    # --- Tab 1: All Patients ---
    with tab1:
        st.markdown("### 🧑‍🤝‍🧑 Patient List")
        appointments = [
            {"time": "09:00 AM", "patient": "Dev"},
            {"time": "10:30 AM", "patient": "Bob Smith"},
            {"time": "01:00 PM", "patient": "Charlie Lee"},
        ]
        for appt in appointments:
            st.write(f"🕘 {appt['time']} — 👤 {appt['patient']}")

    # --- Tab 2: Patient Info ---
    with tab2:
        st.markdown("### 🧾 Patient Information")
        patient_name = st.selectbox("Select a patient:", ["Dev", "Bob Smith", "Charlie Lee"])

        patient_info = {
            "Dev": {"Age": 30, "Condition": "Flu", "Last Visit": "2025-09-01"},
            "Bob Smith": {"Age": 45, "Condition": "Diabetes", "Last Visit": "2025-08-25"},
            "Charlie Lee": {"Age": 50, "Condition": "Hypertension", "Last Visit": "2025-08-30"},
        }

        if patient_name:
            info = patient_info[patient_name]
            st.write(f"**Name:** {patient_name}")
            st.write(f"**Age:** {info['Age']}")
            st.write(f"**Condition:** {info['Condition']}")
            st.write(f"**Last Visit:** {info['Last Visit']}")

    # --- Tab 3: E_Case Records ---
    with tab3:
        st.markdown("### 📥 Insert or Update E_Case Records")

        action = st.radio("Choose Action", ["Insert New", "Update Existing"])

        if action == "Insert New":
            rfid = st.text_input("RFID No")
            date_time = st.text_input("Date & Time (YYYY-MM-DD HH:MM:SS)")
            status = st.text_input("Status")

            if st.button("Insert Record"):
                try:
                    insert_e_case(rfid, date_time, status)
                    st.success("✅ Record inserted successfully!")
                except Exception as e:
                    st.error(f"❌ Error inserting record: {e}")

        elif action == "Update Existing":
            case_id = st.number_input("E_Case ID to Update", min_value=1, step=1)
            rfid = st.text_input("New RFID No")
            date_time = st.text_input("New Date & Time (YYYY-MM-DD HH:MM:SS)")
            status = st.text_input("New Status")

            if st.button("Update Record"):
                try:
                    update_e_case(case_id, rfid, date_time, status)
                    st.success("✅ Record updated successfully!")
                except Exception as e:
                    st.error(f"❌ Error updating record: {e}")

        st.markdown("### 📋 All E_Case Records")

        try:
            cols, rows = get_all_e_cases()
            if rows:
                df_data = [dict(zip(cols, row)) for row in rows]
                st.dataframe(df_data, use_container_width=True)
            else:
                st.info("No E_Case records found.")
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")

    # --- Lunch Break Section ---
    st.markdown("### 🥪 Lunch Break")
    if st.session_state.on_lunch:
        if st.button("End Lunch Break"):
            st.session_state.on_lunch = False
            st.success("Lunch break ended at " + datetime.now().strftime("%I:%M %p"))
    else:
        if st.button("Start Lunch Break"):
            st.session_state.on_lunch = True
            st.info("You're now on lunch break as of " + datetime.now().strftime("%I:%M %p"))

    # --- Logout Section ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.on_lunch = False
        st.success("Logged out successfully.")
        st.experimental_rerun()

# --- MAIN LOGIN PAGE ---
def login_page():
    st.title("🩺 Doctor Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "doctor" and password == "doctor123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# --- SESSION INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'on_lunch' not in st.session_state:
    st.session_state.on_lunch = False

# --- ROUTING ---
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
