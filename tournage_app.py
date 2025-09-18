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
        ("clapper.png", f"Nom du tournage : {nom}"),
        ("building.png", f"Prod : {prod}"),
        ("person.png", f"Client : {client}"),
        ("page.png", f"Description : {description}"),
        ("camera.png", f"Poste : {poste}"),
        ("money.png", f"Rémunération : {remu}"),
        ("calendar.png", f"Dates de tournage : {date}"),
        ("pin.png", f"Lieu : {lieu}"),
        ("clock.png", f"Horaires estimés : {horaires}")
    ]

    # --- Dimensions image ---
    width, height = 1080, 1350
    img = Image.new("RGB", (width, height), "#f5f5f5")  # fond gris clair
    draw = ImageDraw.Draw(img)

    # --- Carte blanche ---
    margin = 60
    card_x0, card_y0 = margin, margin
    card_x1, card_y1 = width - margin, height - margin
    card = Image.new("RGB", (card_x1 - card_x0, card_y1 - card_y0), "white")

    # Police Montserrat
    try:
        font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Regular.ttf"), 36)
        title_font = ImageFont.truetype(os.path.join(BASE_DIR, "fonts", "Montserrat-Bold.ttf"), 56)
    except:
        font = ImageFont.load_default()
        title_font = font

    # Dessin sur la carte
    card_draw = ImageDraw.Draw(card)

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    bbox = card_draw.textbbox((0, 0), title_text, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    card_draw.text(((card.width - tw) // 2, 40), title_text, font=title_font, fill="black")

    # Ligne de séparation
    card_draw.line((80, 120, card.width - 80, 120), fill="#cccccc", width=3)

    # --- Contenu ---
    y = 160
    for icon_file, texte in lignes:
        path = icon_path(icon_file)
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((48, 48))
                card.paste(icon, (80, y), mask=icon)
            except Exception as e:
                st.write(f"❌ Erreur icône {icon_file} : {e}")
        card_draw.text((150, y + 8), texte, font=font, fill="black")
        y += 90

    # --- Coller la carte sur le fond ---
    img.paste(card, (card_x0, card_y0))

    # --- Export ---
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Affichage et téléchargement
    st.image(img, caption="Aperçu fiche")
    st.download_button(
        "📥 Télécharger la fiche en PNG",
        buffer,
        file_name="fiche_tournage.png",
        mime="image/png"
    )
