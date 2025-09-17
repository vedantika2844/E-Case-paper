import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# -------------------- DB Connection --------------------
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        password="testStudents@123",
        database="u263681140_students"
    )

# -------------------- Insert Patient --------------------
def insert_patient(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO E_casepatient 
    (Name, RFIDNO, Age, Gender, BloodGroup, DateofBirth, ContactNo, EmailID, Address, DoctorAssigned)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

# -------------------- Fetch All Patients --------------------
def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM E_casepatient ORDER BY ID DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# -------------------- Fetch Medical History --------------------
def get_medical_history_by_rfid(rfidno):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM medical__histroy WHERE RFIDNo = %s ORDER BY ID DESC",
            (rfidno,)
        )
        rows = cursor.fetchall()
        return rows if rows else []
    except Exception as e:
        st.error(f"❌ Error fetching medical history: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# -------------------- Appointment Functions --------------------
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

def get_current_appointments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM E_Case ORDER BY Date_Time DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_appointment_by_rfid(rfid):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM E_Case WHERE RFID_No = %s", (rfid,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    except Exception as e:
        st.error(f"❌ Error deleting appointment: {e}")
        return False

# -------------------- Doctor Dashboard --------------------
def dashboard():
    st.subheader(f"👨‍⚕️ Doctor Dashboard - Dr. {st.session_state.username.capitalize()}")

    tab1, tab2, tab3 = st.tabs(["📝 All Patients", "📋 Patient Information", "📥 E_Case Records"])

    # --- Tab 1: All Patients ---
    with tab1:
        st.subheader("📋 All Registered Patients")
        data = get_all_patients()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No patients registered yet.")

    # --- Tab 2: Patient Info ---
    with tab2:
        st.subheader("📖 Patient Medical History")
        appointments = get_current_appointments()
        rfid_list = [row['RFID_No'] for row in appointments if row.get('RFID_No')]

        if rfid_list:
            selected_rfid = st.selectbox("Select RFID to view history", rfid_list)
            if selected_rfid:
                history = get_medical_history_by_rfid(selected_rfid)
                if history:
                    df = pd.DataFrame(history)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No medical history found for this patient.")
        else:
            st.info("No appointments yet, so no history to show.")

    # --- Tab 3: E_Case Records ---
    with tab3:
        st.subheader("📥 Insert or Update E_Case Records")
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

        st.subheader("📋 All E_Case Records")
        try:
            cols, rows = get_all_e_cases()
            if rows:
                df_data = [dict(zip(cols, row)) for row in rows]
                st.dataframe(df_data, use_container_width=True)
            else:
                st.info("No E_Case records found.")
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")

    # --- Logout Section ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully.")
        st.experimental_rerun()

# -------------------- Login Page --------------------
def login_page():
    st.title("🩺 Doctor Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "doctor" and password == "doctor123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

# -------------------- Session Init --------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# -------------------- Routing --------------------
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
