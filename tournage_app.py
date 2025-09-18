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
    width, height = 1080, 1400
    img = Image.new("RGB", (width, height), "#f5f5f7")  # fond Apple gris clair
    draw = ImageDraw.Draw(img)

    # --- Carte blanche ---
    margin = 80
    card_x0, card_y0 = margin, margin
    card_x1, card_y1 = width - margin, height - margin
    card = Image.new("RGB", (card_x1 - card_x0, card_y1 - card_y0), "white")

    # Police Montserrat
    try:
        font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Regular.ttf"), 38)
        label_font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Bold.ttf"), 38)
        title_font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Bold.ttf"), 64)
    except:
        font = ImageFont.load_default()
        label_font = font
        title_font = font

    # Dessin sur la carte
    card_draw = ImageDraw.Draw(card)

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    bbox = card_draw.textbbox((0, 0), title_text, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    card_draw.text(((card.width - tw) // 2, 60), title_text, font=title_font, fill="black")

    # Ligne fine
    card_draw.line((100, 160, card.width - 100, 160), fill="#e0e0e0", width=2)

    # --- Contenu ---
    y = 220
    for icon_file, label, valeur in lignes:
        path = icon_path(icon_file)

        # Icône
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((50, 50))
                card.paste(icon, (100, y), mask=icon)
            except Exception as e:
                st.write(f"❌ Erreur icône {icon_file} : {e}")

        # Label en gras
        card_draw.text((180, y), f"{label} :", font=label_font, fill="black")

        # Valeur en regular
        if valeur:
            lw = card_draw.textlength(f"{label} :", font=label_font)
            card_draw.text((180 + lw + 15, y), valeur, font=font, fill="black")

        y += 100  # plus d’espace entre chaque bloc

    # --- Coller la carte sur le fond ---
    img.paste(card, (card_x0, card_y0))

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
