import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Fiche Tournage", page_icon="🎬", layout="centered")

st.title("🎬 Générateur de fiche tournage")

# --- Formulaire ---
with st.form("tournage_form"):
    nom_tournage = st.text_input("Nom du tournage")
    prod = st.text_input("Production")
    client = st.text_input("Client")
    description = st.text_area("Description (très courte)")
    poste = st.text_input("Poste")
    remuneration = st.number_input("Rémunération par jour (€)", min_value=0)
    nb_jours = st.number_input("Nombre de jours", min_value=1, value=1)
    total = remuneration * nb_jours
    dates = st.text_input("Date(s) de tournage")
    versement = st.text_input("Estimation date de versement")
    lieu = st.text_input("Lieu")
    horaires = st.text_input("Horaires estimés")
    repas = st.text_input("Repas / défraiements")
    contact = st.text_input("Contact prod")

    submitted = st.form_submit_button("📄 Générer fiche")

# --- Fonction PDF ---
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Fiche tournage", ln=True, align="C")
    pdf.ln(10)

    infos = [
        ("Nom du tournage", nom_tournage),
        ("Production", prod),
        ("Client", client),
        ("Description", description),
        ("Poste", poste),
        ("Rémunération", f"{remuneration} €/jour"),
        ("Total", f"{total} €"),
        ("Dates", dates),
        ("Lieu", lieu),
        ("Horaires", horaires),
        ("Repas/défraiements", repas),
        ("Versement estimé", versement),
        ("Contact prod", contact),
    ]

    for label, value in infos:
        pdf.multi_cell(0, 10, f"{label} : {value}")

    return pdf.output(dest="S").encode("latin1")

# --- Fonction Image ---
def generate_png():
    img = Image.new("RGB", (800, 1000), "white")
    d = ImageDraw.Draw(img)
    y = 50

    font = ImageFont.load_default()

    d.text((300, 20), "🎬 Fiche tournage", fill="black", font=font)

    infos = [
        ("Nom du tournage", nom_tournage),
        ("Production", prod),
        ("Client", client),
        ("Description", description),
        ("Poste", poste),
        ("Rémunération", f"{remuneration} €/jour"),
        ("Total", f"{total} €"),
        ("Dates", dates),
        ("Lieu", lieu),
        ("Horaires", horaires),
        ("Repas/défraiements", repas),
        ("Versement estimé", versement),
        ("Contact prod", contact),
    ]

    for label, value in infos:
        d.text((50, y), f"{label} : {value}", fill="black", font=font)
        y += 40

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- Affichage des boutons ---
if submitted:
    col1, col2 = st.columns(2)

    with col1:
        pdf_bytes = generate_pdf()
        st.download_button("📥 Télécharger PDF", data=pdf_bytes, file_name="fiche_tournage.pdf", mime="application/pdf")

    with col2:
        png_bytes = generate_png()
        st.download_button("🖼 Télécharger PNG", data=png_bytes, file_name="fiche_tournage.png", mime="image/png")
