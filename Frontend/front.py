import streamlit as st
from auth import authenticate  # Import the authentication function

# Streamlit page configuration
st.set_page_config(page_title="Smart Photos", page_icon="📸", layout="centered")

# CSS styles for the page
st.markdown("""
    <style>
        .header {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding: 20px;
        }
        .logo {
            width: 100px;
            height: auto;
            margin-left: 20px;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin: 0;
        }
        .input-field {
            width: 300px;
            margin: 0 auto;
        }
        .button {
            background-color: #2E86C1;
            color: white;
            width: 130px;
            height: 40px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #1B4F72;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .button-container > div {
            margin: 0 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Page layout with title and logo
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<div class="title">Smart Photos</div>', unsafe_allow_html=True)
# st.image("logosmart.png", width=70)  # Adjust width as needed
st.markdown('</div>', unsafe_allow_html=True)

# User ID and Password input fields
user_id = st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
password = st.text_input("Password", key="password", placeholder="Enter your Password", type="password")

# Button click handler
if st.button("Sign In"):
    if authenticate(user_id, password):
        st.success("Signed in successfully!")
    else:
        st.error("Invalid User ID or Password")

# Sign-up button
if st.button("Sign Up"):
    st.info("Sign-up functionality is not implemented yet.")
