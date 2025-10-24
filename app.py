from PIL import Image
import streamlit as st
import os

# List of accepted vector file extensions
vector_extensions = ['.ai', '.svg', '.eps']

st.title("LPS - Check printing file")

# 📁 File upload
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["svg", "ai", "eps", "png", "jpg", "jpeg", "tiff"]
)

if uploaded_file:
    file_name = uploaded_file.name
    _, extension = os.path.splitext(file_name)

    # Check if the file is a vector format
    if extension.lower() in vector_extensions:
        st.success(f"✅ The file '{file_name}' is in vector format ({extension}).")
    else:
        try:
            # Check resolution if it's a raster image
            image = Image.open(uploaded_file)
            width, height = image.size

            if width >= 3500 and height >= 3500:
                st.success(f"✅ The image '{file_name}' has sufficient resolution ({width} x {height} pixels).")
            else:
                st.error(f"❌ Insufficient resolution ({width} x {height} pixels). Minimum required: 3500 x 3500.")
        except Exception as e:
            st.error(f"Error while analyzing the image: {e}")
