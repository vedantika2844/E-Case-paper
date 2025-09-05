import streamlit as st

# Dummy user database (dictionary)
users = {
    "admin": "admin123",
    "user": "pass"
}

# Title
st.title("🔐 Simple Login Page")

# Mode selection
mode = st.radio("Select mode:", ("Login", "Signup"))

# Common fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if mode == "Signup":
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if username in users:
            st.warning("Username already exists!")
        elif password != confirm_password:
            st.warning("Passwords do not match!")
        else:
            users[username] = password
            st.success("Account created successfully! You can now log in.")

elif mode == "Login":
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}! 🎉")
            st.balloons()
        else:
            st.error("Invalid username or password.")
