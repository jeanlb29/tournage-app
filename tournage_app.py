import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

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
    # Texte à afficher
    lignes = [
        f"🎬 Nom du tournage : {nom}",
        f"🏢 Prod : {prod}",
        f"👤 Client : {client}",
        f"📝 Description : {description}",
        f"🎥 Poste : {poste}",
        f"💶 Rémunération : {remu}",
        f"📅 Dates de tournage : {date}",
        f"📍 Lieu : {lieu}",
        f"⏱ Horaires estimés : {horaires}"
    ]

    # Création image blanche
    img = Image.new("RGB", (800, 1000), "white")
    draw = ImageDraw.Draw(img)

    # Police (Arial ou DejaVu si dispo sur ton Streamlit Cloud)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        font = ImageFont.load_default()

    y = 100
    for ligne in lignes:
        draw.text((80, y), ligne, font=font, fill="black")
        y += 60

    # Sauvegarde en mémoire
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
