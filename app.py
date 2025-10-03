import streamlit as st
from PIL import Image
import pymupdf as fitz
import os

# Titre de l'application
st.title("Vérification du format vectoriel ou du DPI d'un fichier image")

# Extensions vectorielles acceptées
vector_formats = ['.ai', '.svg', '.eps']
# Extensions raster acceptées (incluant PDF)
raster_formats = ['.jpg', '.jpeg', '.png', '.tiff', '.pdf']

# Téléversement du fichier
uploaded_file = st.file_uploader("Téléversez un fichier", type=vector_formats + raster_formats)

if uploaded_file:
    file_name = uploaded_file.name
    _, extension = uploaded_file.path.splitext(file_name)
    extension = extension.lower()

    st.write(f"**Fichier téléversé :** {file_name}")
    st.write(f"**Extension détectée :** {extension}")

    if extension in vector_formats:
        st.success(f"✅ Le fichier est au format vectoriel ({extension})")

    elif extension == '.pdf':
        try:
            pdf_bytes = uploaded_file.read()
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            page = pdf_doc[0]

            # Obtenir les dimensions en pouces
            width_in = page.rect.width / 72
            height_in = page.rect.height / 72

            # Obtenir les dimensions en pixels
            pix = page.get_pixmap(dpi=300)
            width_px = pix.width
            height_px = pix.height

            # Calcul du DPI
            dpi_x = round(width_px / width_in)
            dpi_y = round(height_px / height_in)

            st.write(f"**Dimensions de la première page :** {width_px} x {height_px} pixels")
            st.write(f"**DPI estimé :** ({dpi_x}, {dpi_y})")

            if dpi_x >= 150 and dpi_y >= 150:
                st.success("✅ Le DPI est suffisant (≥ 150)")
            else:
                st.warning("⚠️ Le DPI est insuffisant (< 150)")
        except Exception as e:
            st.error(f"Erreur lors de l'analyse du PDF : {e}")

    elif extension in raster_formats:
        try:
            image = Image.open(uploaded_file)
            dpi_info = image.info.get("dpi", None)

            st.image(image, caption="Aperçu de l'image", use_column_width=True)
            st.write(f"**Dimensions :** {image.size[0]} x {image.size[1]} pixels")
            st.write(f"**DPI détecté :** {dpi_info if dpi_info else 'Non spécifié'}")

            if dpi_info and dpi_info[0] >= 150:
                st.success("✅ Le DPI est suffisant (≥ 150)")
            else:
                st.warning("⚠️ Le DPI est insuffisant ou non spécifié (< 150)")
        except Exception as e:
            st.error(f"Erreur lors de l'ouverture de l'image : {e}")

    else:
        st.error("❌ Format de fichier non pris en charge")
