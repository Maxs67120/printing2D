import streamlit as st
from PIL import Image
import os

# Liste des extensions vectorielles acceptées
vector_extensions = ['.ai', '.svg', '.eps']

st.title("LPS - Check printing file")

# 📁 Upload du fichier
uploaded_file = st.file_uploader("Choisissez un fichier", type=["svg", "ai", "eps", "png", "jpg", "jpeg"])

if uploaded_file:
    file_name = uploaded_file.name
    _, extension = os.path.splitext(file_name)

    # Vérification du format vectoriel
    if extension.lower() in vector_extensions:
        st.success(f"✅ Le fichier '{file_name}' est au format vectoriel ({extension}).")
    else:
        try:
            # Vérification de la résolution si c'est une image raster
            image = Image.open(uploaded_file)
            width, height = image.size

            if width >= 3500 and height >= 3500:
                st.success(f"✅ L'image '{file_name}' a une résolution suffisante ({width} x {height} pixels).")
            else:
                st.error(f"❌ Résolution insuffisante ({width} x {height} pixels). Minimum requis : 3500 x 3500.")
        except Exception as e:
            st.error(f"Erreur lors de l'analyse de l'image : {e}")
