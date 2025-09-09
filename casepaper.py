import streamlit as st
from datetime import datetime
import mysql.connector
def dashboard():
    st.subheader(f"👨‍⚕️ Doctor Dashboard - Dr. {st.session_state.username.capitalize()}")

    # --- Tabs
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
