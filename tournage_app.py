import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

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
    st.markdown(f"""
    🎬 **Nom du tournage** : {nom}  
    🏢 **Prod** : {prod}  
    👤 **Client** : {client}  
    📝 **Description** : {description}  
    🎥 **Poste** : {poste}  
    💶 **Rémunération** : {remu}  
    📅 **Dates de tournage** : {date}  
    📍 **Lieu** : {lieu}  
    ⏱ **Horair**
