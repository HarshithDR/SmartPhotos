import streamlit as st

# Streamlit page configuration
st.set_page_config(page_title="Horizontal Division Example", layout="wide")

# Divide the page into two rows horizontally
top_row, bottom_row = st.columns(2)

# Components for the top row
with top_row:
    st.header("Top Row")
    st.text("This is the top row.")

    # Example input field
    user_input_top = st.text_input("Enter something for top row")

# Components for the bottom row
with bottom_row:
    st.header("Bottom Row")
    st.text("This is the bottom row.")

    # Example input field
    user_input_bottom = st.text_input("Enter something for bottom row")

# Additional components beside the rows (full-width)
st.header("Beside the Rows")
st.text("This section spans the full width beside the rows.")