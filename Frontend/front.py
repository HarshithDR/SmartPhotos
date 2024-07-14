import streamlit as st
from pymongo import MongoClient
import bcrypt
from PIL import Image
import io

# Connect to MongoDB
url = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster0.gzsu9lm.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.ImageDB

# Streamlit page configuration
st.set_page_config(page_title="Smart Photos", page_icon="📸", layout="centered")

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

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# User ID and Password input fields
if not st.session_state.authenticated:
    # logo
    st.image('logosmart.png')

    # User ID and Password input fields
    user_id = st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
    password = st.text_input("Password", key="password", placeholder="Enter your Password", type="password")

    st.columns(1)
    _, button2, button3, _ = st.columns(4)
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
                st.success("Sign-in successful!")
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Login failed. Check your username and/or password.")
                st.error("Sign-in failed!")

    # Sign-up button
    with button2:
        st.markdown(button_style, unsafe_allow_html=True)
        if st.button("Sign Up", key="sign_up"):
            if create_user(user_id, password):
                st.success("You have successfully created an account! You can login now.")
            else:
                st.error("Username already exists. Try a different username.")
else:
    # Sidebar with upload and search buttons
    st.sidebar.title("Options")
    uploaded_file = st.sidebar.file_uploader("Choose an image")
    if uploaded_file is not None:
        tags = st.text_input("Enter tags for the image")
        if st.button("Upload Image"):
            upload_image(st.session_state['logged_in'], uploaded_file.read(), tags)
            st.success("Image uploaded with tags!")
    user_images = get_user_images(st.session_state['logged_in'])
    search_query = st.sidebar.text_input("Search with AI")

    # Main content area
    st.title("Photo Gallery")

    # Display images in a grid
    def display_images_grid(images):
        cols = st.columns(3)  # Create 3 columns for the photos
        for idx, image_data in enumerate(images):
            col = cols[idx % 3]  # Cycle through the columns
            image = Image.open(io.BytesIO(image_data['image']))
            col.image(image, use_column_width=True, caption=image_data['tags'])

    if user_images:
        st.write("### Uploaded Photos")
        display_images_grid(user_images)

    if search_query:
        st.write(f"### Search Results for: {search_query}")
        # Here you would implement the AI search functionality
        # For now, let's just display a placeholder
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 1")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 2")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 3")

    if not uploaded_file and not search_query:
        st.write("Upload photos or use the AI search to display images here.")
