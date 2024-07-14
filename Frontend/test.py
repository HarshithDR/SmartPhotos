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

def upload_image(user_id, image):
    db.Images.insert_one({"user_id": user_id, "image": image})

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
        .uploaded-images .uploaded-image-name {
            display: flex;
            align-items: center;
        }
        .uploaded-images .remove-button {
            margin-left: 10px;
            cursor: pointer;
            color: red;
            font-size: 20px;
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
        upload_button = st.sidebar.button("Upload Image")
        if upload_button:
            upload_image(st.session_state['logged_in'], uploaded_file.read())
            st.sidebar.empty()  # Clear the file uploader
            st.success("Image uploaded!")

    user_images = get_user_images(st.session_state['logged_in'])
    if user_images:
        st.sidebar.title("Uploaded Images")
        for image_data in user_images:
            img = Image.open(io.BytesIO(image_data['image']))
            st.sidebar.image(img, use_column_width=True)
            st.sidebar.markdown("---")

    search_query = st.sidebar.text_input("Search with AI")

    # Main content area
    st.title("Photo Gallery")

    def display_images(files):
        cols = st.columns(3)  # Create 3 columns for the photos
        for idx, file in enumerate(files):
            try:
                image = Image.open(io.BytesIO(file['image']))
                image = image.convert('RGB')  # Convert to RGB mode
                image = image.resize((300, 300))  # Resize image to 300x300 pixels
                col = cols[idx % 3]  # Cycle through the columns
                col.image(image, use_column_width=True, caption=f"Photo {idx + 1}")
            except (IOError, OSError) as e:
                st.error(f"Error loading image: {e}")

    if search_query:
        st.write(f"### Search Results for: {search_query}")
        # Here you would implement the AI search functionality
        # For now, let's just display a placeholder
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 1")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 2")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 3")

    user_images = list(get_user_images(st.session_state['logged_in']))
    if user_images:
        st.write("### Your Photos")
        display_images(user_images)

    if not uploaded_file and not search_query and not user_images:
        st.write("Upload photos or use the AI search to display images here.")
