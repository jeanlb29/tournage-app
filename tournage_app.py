import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

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
    # Affichage Streamlit (avec vrais emojis)
    st.markdown(f"""
    🎬 **Nom du tournage** : {nom}  
    🏢 **Prod** : {prod}  
    👤 **Client** : {client}  
    📝 **Description** : {description}  
    🎥 **Poste** : {poste}  
    💶 **Rémunération** : {remu}  
    📅 **Dates de tournage** : {date}  
    📍 **Lieu** : {lieu}  
    ⏱ **Horaires estimés** : {horaires}  
    """)

    # Création PDF avec emojis en PNG
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    lignes = [
        ("icons/clapper.png", f"Nom du tournage : {nom}"),
        ("icons/building.png", f"Prod : {prod}"),
        ("icons/person.png", f"Client : {client}"),
        ("icons/page.png", f"Description : {description}"),
        ("icons/camera.png", f"Poste : {poste}"),
        ("icons/money.png", f"Rémunération : {remu}"),
        ("icons/calendar.png", f"Dates de tournage : {date}"),
        ("icons/pin.png", f"Lieu : {lieu}"),
        ("icons/clock.png", f"Horaires estimés : {horaires}")
    ]

    y = 800
    for icon, texte in lignes:
        c.drawImage(icon, 40, y-8, width=12, height=12)  # emoji image
        c.drawString(60, y, texte)                       # texte
        y -= 25

    c.save()
    buffer.seek(0)

    st.download_button(
        "📥 Télécharger la fiche en PDF",
        buffer,
        file_name="fiche_tournage.pdf",
        mime="application/pdf"
    )
