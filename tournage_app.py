import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
from PIL import Image, ImageDraw, ImageFont

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

# --- Fonction PDF avec ReportLab ---
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    # Styles personnalisés
    title_style = ParagraphStyle(
        "title",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=1,
        textColor=colors.HexColor("#1a1a1a"),
    )

    label_style = ParagraphStyle(
        "label",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
    )

    # Titre
    elements = [Paragraph("🎬 Fiche Tournage", title_style), Spacer(1, 20)]

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

    # Tableau
    table_data = [[f"<b>{label}</b>", value if value else ""] for label, value in infos]
    table = Table(table_data, colWidths=[120, 350])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer

# --- Fonction PNG (inchangée) ---
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

# --- Affichage ---
if submitted:
    col1, col2 = st.columns(2)

    with col1:
        pdf_buffer = generate_pdf()
        st.download_button(
            "📥 Télécharger PDF",
            data=pdf_buffer,
            file_name="fiche_tournage.pdf",
            mime="application/pdf",
        )

    with col2:
        png_buffer = generate_png()
        st.download_button(
            "🖼 Télécharger PNG",
            data=png_buffer,
            file_name="fiche_tournage.png",
            mime="image/png",
        )
