import streamlit as st
from PIL import Image
import io

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
