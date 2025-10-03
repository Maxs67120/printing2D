
import streamlit as st
from PIL import Image
import os

# Titre de l'application
st.title("Vérification et correction du DPI d'une image")

# Téléversement de l'image
uploaded_file = st.file_uploader("Téléversez une image", type=["jpg", "jpeg", "png", "tiff"])

if uploaded_file:
    # Ouvrir l'image
    img = Image.open(uploaded_file)

    # Extraire les informations
    format_image = img.format
    width, height = img.size
    dpi_info = img.info.get("dpi", None)

    # Afficher les informations
    st.subheader("Informations de l'image")
    st.image(img, caption="Image téléversée", use_column_width=True)
    st.write(f"**Format :** {format_image}")
    st.write(f"**Dimensions :** {width} x {height} pixels")
    st.write(f"**DPI :** {dpi_info if dpi_info else 'Non spécifié'}")

    # DPI cible
    target_dpi = (300, 300)

    # Vérification et correction
    if dpi_info != target_dpi:
        st.warning("Le DPI est incorrect ou non spécifié. Il sera corrigé à 300.")
        corrected_path = "image_corrigee.jpg"
        img.save(corrected_path, dpi=target_dpi)
        st.success("Image corrigée avec succès à 300 DPI.")
        with open(corrected_path, "rb") as file:
            st.download_button("Télécharger l'image corrigée", file, file_name="image_corrigee.jpg", mime="image/jpeg")
        os.remove(corrected_path)
    else:
        st.info("Le DPI est déjà correct (300). Aucune correction nécessaire.")
