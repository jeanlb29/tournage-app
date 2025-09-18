import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

BASE_DIR = os.path.dirname(__file__)

def icon_path(name):
    return os.path.join(BASE_DIR, "icons", name)

st.title("📋 Générateur de fiche tournage (PNG)")

# --- Formulaire ---
nom = st.text_input("Nom du tournage")
prod = st.text_input("Production")
client = st.text_input("Client")
description = st.text_area("Description")
poste = st.text_input("Poste")
remu = st.text_input("Rémunération")
date = st.text_input("Dates de tournage")
lieu = st.text_input("Lieu")
horaires = st.text_input("Horaires estimés")

if st.button("✨ Générer fiche"):
    lignes = [
        ("clapper.png", "Nom du tournage", nom),
        ("building.png", "Prod", prod),
        ("person.png", "Client", client),
        ("page.png", "Description", description),
        ("camera.png", "Poste", poste),
        ("money.png", "Rémunération", remu),
        ("calendar.png", "Dates de tournage", date),
        ("pin.png", "Lieu", lieu),
        ("clock.png", "Horaires estimés", horaires)
    ]

    # --- Dimensions image ---
    width, height = 1240, 1754  # format A4 vertical
    img = Image.new("RGB", (width, height), "#f5f5f7")  # fond gris clair
    draw = ImageDraw.Draw(img)

    # Police Montserrat
    try:
        font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Regular.ttf"), 42)
        label_font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Bold.ttf"), 42)
        title_font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Bold.ttf"), 78)
    except:
        font = ImageFont.load_default()
        label_font = font
        title_font = font

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) // 2, 120), title_text, font=title_font, fill="black")

    # Ligne fine
    draw.line((150, 240, width - 150, 240), fill="#d1d1d6", width=3)

    # --- Contenu ---
    y = 320
    max_width = width - 300  # largeur max pour le texte

    for icon_file, label, valeur in lignes:
        path = icon_path(icon_file)

        # Icône
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((60, 60))
                img.paste(icon, (150, y), mask=icon)
            except Exception as e:
                st.write(f"❌ Erreur icône {icon_file} : {e}")

        # Label en gras
        draw.text((240, y), f"{label} :", font=label_font, fill="black")

        # Valeur → texte multiline si trop long
        if valeur:
            lw = draw.textlength(f"{label} :", font=label_font)
            text_x = 240 + lw + 20
            text_y = y

            # découpe auto en lignes
            words = valeur.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if draw.textlength(test_line, font=font) < (max_width - text_x):
                    line = test_line
                else:
                    draw.text((text_x, text_y), line, font=font, fill="black")
                    text_y += 60
                    line = word + " "
            draw.text((text_x, text_y), line, font=font, fill="black")

        y += 120  # espace plus grand entre les blocs

    # --- Export ---
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Affichage et téléchargement
    st.image(img, caption="Aperçu fiche (style Apple)")
    st.download_button(
        "📥 Télécharger la fiche en PNG",
        buffer,
        file_name="fiche_tournage.png",
        mime="image/png"
    )
