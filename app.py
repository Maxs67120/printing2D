import streamlit as st
from PIL import Image
import os

# Titre de l'application
st.title("Vérification du format vectoriel ou du DPI d'une image")

# Extensions vectorielles acceptées
vector_formats = ['.ai', '.svg', '.eps']
# Extensions raster acceptées
raster_formats = ['.jpg', '.jpeg', '.png', '.tiff']

# Téléversement du fichier
uploaded_file = st.file_uploader("Téléversez un fichier", type=vector_formats + raster_formats)

if uploaded_file:
    # Extraire l'extension du fichier
    file_name = uploaded_file.name
    _, extension = os.path.splitext(file_name)
    extension = extension.lower()

    st.write(f"**Fichier téléversé :** {file_name}")
    st.write(f"**Extension détectée :** {extension}")

    if extension in vector_formats:
        st.success(f"✅ Le fichier est au format vectoriel ({extension})")
    elif extension in raster_formats:
        try:
            img = Image.open(uploaded_file)
            dpi_info = img.info.get("dpi", None)

            st.image(img, caption="Aperçu de l'image", use_column_width=True)
            st.write(f"**Dimensions :** {img.size[0]} x {img.size[1]} pixels")
            st.write(f"**DPI détecté :** {dpi_info if dpi_info else 'Non spécifié'}")

            if dpi_info and dpi_info[0] >= 150:
                st.success("✅ Le DPI est suffisant (≥ 150)")
            else:
                st.warning("⚠️ Le DPI est insuffisant ou non spécifié (< 150)")
        except Exception as e:
            st.error(f"Erreur lors de l'ouverture de l'image : {e}")
    else:
        st.error("❌ Format de fichier non pris en charge")
