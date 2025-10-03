import streamlit as st
from PIL import Image
import os

st.title("Vérification du format vectoriel, raster ou PDF d'une image")

vector_formats = ['.ai', '.svg', '.eps']
raster_formats = ['.jpg', '.jpeg', '.png', '.tiff']
pdf_format = ['.pdf']

uploaded_file = st.file_uploader("Téléversez un fichier", type=vector_formats + raster_formats + pdf_format)

if uploaded_file:
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

    elif extension in pdf_format:
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            page = doc.load_page(0)
            text = page.get_text()
            vector_objects = page.get_drawings()

            st.write(f"**Nombre de pages :** {len(doc)}")
            st.write(f"**Texte détecté :** {'Oui' if text else 'Non'}")
            st.write(f"**Objets vectoriels détectés :** {'Oui' if vector_objects else 'Non'}")

            if vector_objects or text:
                st.success("✅ Le PDF contient des éléments vectoriels")
            else:
                st.warning("⚠️ Le PDF semble ne contenir que des images raster")

        except Exception as e:
            st.error(f"Erreur lors de l'analyse du PDF : {e}")

  
