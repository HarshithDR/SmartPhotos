import streamlit as st

# Streamlit page configuration
st.set_page_config(page_title="Smart Photos", page_icon="📸", layout="centered")

# CSS styles for the page
st.markdown("""
    <style>
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin-top: 50px;
        }
        .input-field {
            width: 300px;
            margin: 0 auto;
        }
        .button {
            background-color: #2E86C1;
            color: white;
            width: 100px;
            height: 40px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #1B4F72;
        }
        .sign-up {
            text-align: center;
            margin-top: 10px;
            color: #2E86C1;
            cursor: pointer;
        }
        .sign-up:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="title">Smart Photos</div>', unsafe_allow_html=True)

# User ID and Password input fields
st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
st.text_input("Password", key="password", placeholder="Enter your Password", type="password")

# Sign-in button
if st.button("Sign In", key="sign_in"):
    st.success("Sign-in successful!")

# Sign-up text
if st.button("Sign Up", key="sign_up"):
    st.info("Sign-up feature coming soon!")


