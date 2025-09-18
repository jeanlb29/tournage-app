import streamlit as st
from fpdf import FPDF

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
    
    # Export PDF (facultatif)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Nom du tournage : {nom}")
    pdf.multi_cell(0, 10, f"Prod : {prod}")
    pdf.multi_cell(0, 10, f"Client : {client}")
    pdf.multi_cell(0, 10, f"Description : {description}")
    pdf.multi_cell(0, 10, f"Poste : {poste}")
    pdf.multi_cell(0, 10, f"Rémunération : {remu}")
    pdf.multi_cell(0, 10, f"Dates de tournage : {date}")
    pdf.multi_cell(0, 10, f"Lieu : {lieu}")
    pdf.multi_cell(0, 10, f"Horaires estimés : {horaires}")
    pdf_output = "fiche_tournage.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button("📥 Télécharger la fiche en PDF", f, file_name=pdf_output)
