import streamlit as st
from pymongo import MongoClient
import bcrypt

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["smart_photos"]
users_collection = db["users"]

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

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'signup' not in st.session_state:
    st.session_state.signup = False

# User ID and Password input fields
if not st.session_state.authenticated and not st.session_state.signup:
    user_id = st.text_input("User ID", key="user_id", placeholder="Enter your User ID", type="default")
    password = st.text_input("Password", key="password", placeholder="Enter your Password", type="password")

    # Button click handler
    if st.button("Sign In"):
        if authenticate(user_id, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid User ID or Password")

    # Sign-up button
    if st.button("Sign Up"):
        st.session_state.signup = True
        st.experimental_rerun()

elif st.session_state.signup:
    st.write("## Sign Up")

    new_user_id = st.text_input("New User ID", key="new_user_id", placeholder="Enter your new User ID", type="default")
    new_password = st.text_input("New Password", key="new_password", placeholder="Enter your new Password", type="password")
    confirm_password = st.text_input("Confirm Password", key="confirm_password", placeholder="Confirm your Password", type="password")

    if st.button("Submit"):
        if new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            try:
                users_collection.insert_one({"user_id": new_user_id, "password": hashed_password})
                st.success("Sign-up successful! Please sign in.")
                st.session_state.signup = False
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error signing up: {e}")
        else:
            st.error("Passwords do not match.")

    if st.button("Cancel"):
        st.session_state.signup = False
        st.experimental_rerun()

else:
    # Sidebar with upload and search buttons
    st.sidebar.title("Options")
    uploaded_files = st.sidebar.file_uploader("Upload Photos", accept_multiple_files=True)
    search_query = st.sidebar.text_input("Search with AI")

    # Main content area
    st.title("Photo Gallery")

    def display_images(files):
        cols = st.columns(3)  # Create 3 columns for the photos
        for idx, file in enumerate(files):
            try:
                image = Image.open(file)
                image = image.resize((300, 300))  # Resize image to 300x300 pixels
                col = cols[idx % 3]  # Cycle through the columns
                col.image(image, use_column_width=True, caption=f"Photo {len(files) - idx}")
            except (IOError, OSError) as e:
                st.error(f"Error loading image {file.name}: {e}")

    if uploaded_files:
        st.write("### Uploaded Photos")
        display_images(uploaded_files[::-1])  # Display images with the latest uploaded first

    if search_query:
        st.write(f"### Search Results for: {search_query}")
        # Here you would implement the AI search functionality
        # For now, let's just display a placeholder
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 1")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 2")
        st.image("https://via.placeholder.com/300", caption="Sample Search Result 3")

    if not uploaded_files and not search_query:
        st.write("Upload photos or use the AI search to display images here.")
