import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io
import os

# Titre de l'application
st.title("Vérification du format d'image pour l'impression 2D")

# Extensions acceptées
vector_formats = ['.ai', '.svg', '.eps']
raster_formats = ['.jpg', '.jpeg', '.png', '.tiff']
pdf_format = ['.pdf']

# Téléversement du fichier
uploaded_file = st.file_uploader("Téléversez un fichier", type=vector_formats + raster_formats + pdf_format)

if uploaded_file:
    file_name = uploaded_file.name
    _, extension = os.path.splitext(file_name)
    extension = extension.lower()

    st.write(f"**Fichier téléversé :** {file_name}")
    st.write(f"**Extension détectée :** {extension}")

    if extension in vector_formats:
        st.success(f"✅ Le fichier est au format vectoriel ({extension})")
        st.info("🖨️ Ce fichier vectoriel est adapté pour l'impression.")

    elif extension in raster_formats:
        try:
            img = Image.open(uploaded_file)
            dpi_info = img.info.get("dpi", None)

            st.image(img, caption="Aperçu de l'image", use_column_width=True)
            st.write(f"**Dimensions :** {img.size[0]} x {img.size[1]} pixels")
            st.write(f"**DPI détecté :** {dpi_info if dpi_info else 'Non spécifié'}")

            if dpi_info and dpi_info[0] >= 150:
                st.success("✅ Le DPI est suffisant (≥ 150)")
                st.info("🖨️ Ce fichier peut être utilisé pour l'impression.")
            else:
                st.warning("⚠️ Le DPI est insuffisant ou non spécifié (< 150)")
        except Exception as e:
            st.error(f"Erreur lors de l'ouverture de l'image : {e}")

    elif extension in pdf_format:
        try:
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            page = doc.load_page(0)
            text = page.get_text()
            vector_objects = page.get_drawings()

            st.write(f"**Nombre de pages :** {len(doc)}")
            st.write(f"**Texte détecté :** {'Oui' if text else 'Non'}")
            st.write(f"**Objets vectoriels détectés :** {'Oui' if vector_objects else 'Non'}")

            if vector_objects or text:
                st.success("✅ Le PDF contient des éléments vectoriels")
                st.info("🖨️ Ce fichier PDF est adapté pour l'impression.")
            else:
                st.warning("⚠️ Le PDF semble ne contenir que des images raster")

            # Extraction des images raster et lecture des DPI
            image_count = 0
            for page_index in range(len(doc)):
                page = doc.load_page(page_index)
                images = page.get_images(full=True)

                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    image = Image.open(io.BytesIO(image_bytes))
                    dpi_info = image.info.get("dpi", None)

                    image_count += 1
                    st.image(image, caption=f"Image extraite page {page_index + 1}, image {img_index + 1}", use_column_width=True)
                    st.write(f"**Format :** {image_ext}")
                    st.write(f"**Dimensions :** {image.size[0]} x {image.size[1]} pixels")
                    st.write(f"**DPI détecté :** {dpi_info if dpi_info else 'Non spécifié'}")

                    if dpi_info and dpi_info[0] >= 150:
                        st.success("✅ Le DPI est suffisant (≥ 150)")
                        st.info("🖨️ Cette image peut être utilisée pour l'impression.")
                    else:
                        st.warning("⚠️ Le DPI est insuffisant ou non spécifié (< 150)")

            if image_count == 0:
                st.info("ℹ️ Aucun objet image raster trouvé dans ce fichier PDF.")

        except Exception as e:
            st.error(f"Erreur lors de l'analyse du PDF : {e}")

    else:
        st.error("❌ Format de fichier non pris en charge")
