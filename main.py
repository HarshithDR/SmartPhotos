import streamlit as st
from pymongo import MongoClient
import bcrypt

# Connect to MongoDB
url = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster0.gzsu9lm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url)
db = client.ImageDB

def create_user(username, password):
    # Check if user already exists
    if db.Users.find_one({"username": username}):
        return None
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = db.Users.insert_one({"username": username, "password": hashed}).inserted_id
    return user_id

def check_user(username, password):
    user = db.Users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user['_id']
    return None

def upload_image(user_id, image, tags):
    db.Images.insert_one({"user_id": user_id, "image": image, "tags": tags})

def get_user_images(user_id):
    return db.Images.find({"user_id": user_id})

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
            color: #FFB22C;
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


# st.logo('assets/a.png', link="https://github.com/HarshithDR/SmartPhotos", icon_image=None)

# st.markdown('<div class="header">', unsafe_allow_html=True)
# st.markdown('<div class="title">Smart Photos</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

#logo
st.image('assets/logo2.png')

# User ID and Password input fields
user_id = st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
password = st.text_input("Password", key="password", placeholder="Enter your Password", type="password")


st.columns(1)
_ , button2, button3, _ = st.columns(4)
button_style = '''
    <style>
        .stButton button {
            color: white !important;
            background-color: #0F67B1 !important;
            width: 100px;
            height: 45px;
            border: none;
            border-radius: 15px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #27AE60 !important;
        }
    </style>
'''

# Sign-in button
with button3:
    st.markdown(button_style, unsafe_allow_html=True)
    if st.button('Sign-in', key="sign_in"):
        user_id = check_user(user_id, password)
        if user_id:
            st.session_state['logged_in'] = user_id
            st.success("Logged in successfully!")
        else:
            st.error("Login failed. Check your username and/or password.")
        st.success("Sign-in successful!")
        
# Sign-up button
with button2:
    st.markdown(button_style, unsafe_allow_html=True)
    if st.button("Sign Up", key="sign_up"):
        if create_user(user_id, password):
            st.success("You have successfully created an account! You can login now.")
        else:
            st.error("Username already exists. Try a different username.")

