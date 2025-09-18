import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

BASE_DIR = os.path.dirname(__file__)

def icon_path(name):
    return os.path.join(BASE_DIR, "icons", name)

st.title("📋 Générateur de fiche tournage (PNG)")

# Formulaire
nom = st.text_input("Nom du tournage")
prod = st.text_input("Production")
client = st.text_input("Client")
description = st.text_area("Description")
poste = st.text_input("Poste")
remu = st.text_input("Rémunération")
date = st.text_input("Dates de tournage")
lieu = st.text_input("Lieu")
horaires = st.text_input("Horaires estimés")

if st.button("Générer fiche"):
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

    # Création image blanche
    img = Image.new("RGB", (1000, 1200), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font = ImageFont.load_default()

    y = 120
    for icon_file, texte in lignes:
        icon = Image.open(icon_path(icon_file)).resize((36, 36))
        img.paste(icon, (80, y), mask=icon)  # coller emoji
        draw.text((140, y), texte, font=font, fill="black")
        y += 80

    # Sauvegarde
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    st.image(img, caption="Aperçu fiche")
    st.download_button(
        "📥 Télécharger la fiche en PNG",
        buffer,
        file_name="fiche_tournage.png",
        mime="image/png"
    )
