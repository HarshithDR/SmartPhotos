import streamlit as st
from pymongo import MongoClient
import bcrypt

uri = "mongodb+srv://amithdeeplearningworkshop:mucgz8JjD5ynz40A@cluster0.gzsu9lm.mongodb.net/ImageDB?retryWrites=true&w=majority&appName=Cluster0"
# Connect to MongoDB
client = MongoClient(uri)
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

# Streamlit interface
st.title('Image Uploader with Tags')

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Signup":
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if create_user(new_username, new_password):
            st.success("You have successfully created an account! You can login now.")
        else:
            st.error("Username already exists. Try a different username.")

if choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = check_user(username, password)
        if user_id:
            st.session_state['logged_in'] = user_id
            st.success("Logged in successfully!")
        else:
            st.error("Login failed. Check your username and/or password.")

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    # Image upload
    uploaded_file = st.file_uploader("Choose an image")
    if uploaded_file is not None:
        tags = st.text_input("Enter tags for the image")
        if st.button("Upload Image"):
            upload_image(st.session_state['logged_in'], uploaded_file.read(), tags)
            st.success("Image uploaded with tags!")

    # Display images
    user_images = get_user_images(st.session_state['logged_in'])
    for image_data in user_images:
        st.image(image_data['image'], caption=image_data['tags'])