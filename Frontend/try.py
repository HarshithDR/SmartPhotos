import streamlit as st
from pymongo import MongoClient
import bcrypt
from PIL import Image
import io
import requests
import time
# Connect to MongoDB
url = "mongodb+srv://sohanmahadev:Sohan%40123@cluster0.gachc3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url, tlsAllowInvalidCertificates=True)
db = client.ImageDB


if 'data' not in st.session_state:
    st.session_state.data = {}

# Streamlit page configuration
st.set_page_config(page_title="Smart Photos", page_icon="📸", layout="centered")

if 'new_id' not in st.session_state:
    st.session_state.new_id = {}


def create_user(username, password):
    try:
        # Check if user already exists
        if db.Users.find_one({"username": username}):
            return None
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = db.Users.insert_one({"username": username, "password": hashed}).inserted_id



        return user_id
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None

def check_user(username, password):
    try:
        user = db.Users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user['_id']
        return None
    except Exception as e:
        st.error(f"Error checking user: {e}")
        return None

def upload_image(user_id, image):
    try:
        db.Images.insert_one({"user_id": user_id, "image": image,'tags':''})
    except Exception as e:
        st.error(f"Error uploading image: {e}")

def get_user_images(user_id):
    try:
        return db.Images.find({"user_id": user_id})
    except Exception as e:
        st.error(f"Error fetching images: {e}")
        return []

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
    c1,c2,c3 = st.columns(3)
    with c2:
        st.image('l.png',width=300)

    # User ID and Password input fields
    user_id = st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
    password = st.text_input("Password", key="password", placeholder="Enter your Password", type="password")


    st.session_state.data = {
        "user_id": user_id,
        "password": password
    }

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
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Login failed. Check your username and/or password.")

    # Sign-up button
    with button2:
        st.markdown(button_style, unsafe_allow_html=True)
        if st.button("Sign Up", key="sign_up"):
            if create_user(user_id, password):
                st.success("You have successfully created an account! You can login now.")
                st.session_state.new_id = {
                    "user_id": user_id
                }

            else:
                st.error("Username already exists. Try a different username.")
else:
    # Sidebar with upload button
    st.sidebar.title("Options")
    uploaded_file = st.sidebar.file_uploader("Choose an image")

    if uploaded_file is not None:
        if st.sidebar.button("Upload Image"):
            url_backend = 'http://127.0.0.1:5000/process_images'




            upload_image(st.session_state['logged_in'], uploaded_file.read())
            st.sidebar.empty()  # Clear the file uploader
            st.success("Image uploaded!")
            # Make the POST request
            requests.post(url_backend, json=st.session_state.data)
            print(st.session_state.data)
            st.experimental_rerun()  # Rerun the app to update the image gallery

    search_query = st.sidebar.text_input("Search with AI")
    if search_query:
        url_backend_chat = 'http://127.0.0.1:5000/chat_query'
        # time.sleep(5)
        # st.sidebar.text('Here is the car image you are searching for')

        # Initialize a new session state variable by copying the existing data
        if 'data_sent' not in st.session_state:
            st.session_state.data_sent = dict(st.session_state.data)  # Create a copy of the data

        # Append the query to the new session state variable
        st.session_state.data_sent['query'] = search_query
        

        # Send the updated data dictionary via POST request
        response = requests.post(url_backend_chat, json=st.session_state.data_sent)
        print(response.text)
        data = response.json()
        st.sidebar.text(data['ai_response'])

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
        # st.image("https://via.placeholder.com/300", caption="Sample Search Result 1")
        # st.image("https://via.placeholder.com/300", caption="Sample Search Result 2")
        # st.image("https://via.placeholder.com/300", caption="Sample Search Result 3")

    user_images = list(get_user_images(st.session_state['logged_in']))
    if user_images:
        st.write("### Your Photos")
        display_images(user_images)

    if not uploaded_file and not search_query and not user_images:
        st.write("Upload photos or use the AI search to display images here.")