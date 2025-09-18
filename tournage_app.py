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

    # Création PDF avec ReportLab
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)

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

    y = 800
    for ligne in lignes:
        c.drawString(50, y, ligne)
        y -= 20

    c.save()
    buffer.seek(0)

    st.download_button(
        "📥 Télécharger la fiche en PDF",
        buffer,
        file_name="fiche_tournage.pdf",
        mime="application/pdf"
    )
