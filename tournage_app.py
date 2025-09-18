import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

# Base directory pour localiser les icônes
BASE_DIR = os.path.dirname(__file__)

def icon_path(name):
    return os.path.join(BASE_DIR, "icons", name)

st.title("📋 Générateur de fiche tournage")

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
    # Affichage Streamlit
    st.markdown("""
    🎬 **Nom du tournage** : {}  
    🏢 **Prod** : {}  
    👤 **Client** : {}  
    📝 **Description** : {}  
    🎥 **Poste** : {}  
    💶 **Rémunération** : {}  
    📅 **Dates de tournage** : {}  
    📍 **Lieu** : {}  
    ⏱ **Horaires estimés** : {}  
    """.format(nom, prod, client, description, poste, remu, date, lieu, horaires))

    # Création PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    lignes = [
        (icon_path("clapper.png"), f"Nom du tournage : {nom}"),
        (icon_path("building.png"), f"Prod : {prod}"),
        (icon_path("person.png"), f"Client : {client}"),
        (icon_path("page.png"), f"Description : {description}"),
        (icon_path("camera.png"), f"Poste : {poste}"),
        (icon_path("money.png"), f"Rémunération : {remu}"),
        (icon_path("calendar.png"), f"Dates de tournage : {date}"),
        (icon_path("pin.png"), f"Lieu : {lieu}"),
        (icon_path("clock.png"), f"Horaires estimés : {horaires}")
    ]

    y = 800
    for icon, texte in lignes:
        if os.path.exists(icon):  # évite de planter si une icône n'existe pas
            c.drawImage(icon, 40, y-8, width=14, height=14)
        c.drawString(65, y, texte)
        y -= 25

    c.save()
    buffer.seek(0)

    st.download_button(
        "📥 Télécharger la fiche en PDF",
        buffer,
        file_name="fiche_tournage.pdf",
        mime="application/pdf"
    )
