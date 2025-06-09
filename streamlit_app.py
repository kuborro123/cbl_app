
import streamlit as st

# Title of the app
st.title("Simple Streamlit App")

# Text input
name = st.text_input("Enter your name:")

# Button
if st.button("Say Hello"):
    if name:
        st.success(f"Hello, {name}!")
    else:
        st.warning("Please enter your name first.")
