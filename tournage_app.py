import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- Police Montserrat ---
FONT_PATH_REGULAR = "fonts/Montserrat-Regular.ttf"
FONT_PATH_BOLD = "fonts/Montserrat-Bold.ttf"

# --- Dossier icônes ---
ICON_DIR = "icons"

def icon_path(filename):
    return os.path.join(ICON_DIR, filename)

def generate_card(data):
    # A4 horizontal
    width, height = 1754, 1240  
    bg_color = (255, 255, 255)  
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype(FONT_PATH_BOLD, 90)
    label_font = ImageFont.truetype(FONT_PATH_BOLD, 50)
    font = ImageFont.truetype(FONT_PATH_REGULAR, 50)

    margin = 120
    content_width = width - 2 * margin

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    tw, th = draw.textbbox((0, 0), title_text, font=title_font)[2:]
    draw.text(((width - tw) / 2, margin), title_text, font=title_font, fill="black")

    # Ligne fine
    line_y = margin + 120
    draw.line([(margin, line_y), (width - margin, line_y)], fill=(220, 220, 220), width=3)

    # --- Contenu ---
    lignes = [
        ("clapper.png", "Nom du tournage", data.get("nom", "")),
        ("building.png", "Prod", data.get("prod", "")),
        ("person.png", "Client", data.get("client", "")),
        ("page.png", "Description", data.get("description", "")),
        ("camera.png", "Poste", data.get("poste", "")),
        ("money.png", "Rémunération", data.get("remuneration", "")),
        ("calendar.png", "Dates de tournage", data.get("dates", "")),
        ("pin.png", "Lieu", data.get("lieu", "")),
        ("clock.png", "Horaires estimés", data.get("horaires", "")),
    ]

    y = line_y + 100

    for icon_file, label, valeur in lignes:
        # Icône
        path = icon_path(icon_file)
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((50, 50))
                img.paste(icon, (margin, y), mask=icon)
            except Exception as e:
                st.write(f"⚠️ Erreur icône {icon_file} : {e}")

        # Label
        draw.text((margin + 70, y), f"{label} :", font=label_font, fill="#333333")

        # Valeur (jamais coupée car largeur énorme)
        lw = draw.textlength(f"{label} :", font=label_font)
        text_x = margin + 70 + lw + 25
        draw.text((text_x, y), valeur, font=font, fill="black")

        y += 100  # espacement

    # Sauvegarde
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.title("🎬 Générateur de Fiche Tournage")

with st.form("tournage_form"):
    nom = st.text_input("Nom du tournage")
    prod = st.text_input("Prod")
    client = st.text_input("Client")
    description = st.text_area("Description")
    poste = st.text_input("Poste")
    remuneration = st.text_input("Rémunération")
    dates = st.text_input("Dates de tournage")
    lieu = st.text_input("Lieu")
    horaires = st.text_input("Horaires estimés")
    submitted = st.form_submit_button("Générer fiche")

if submitted:
    data = {
        "nom": nom,
        "prod": prod,
        "client": client,
        "description": description,
        "poste": poste,
        "remuneration": remuneration,
        "dates": dates,
        "lieu": lieu,
        "horaires": horaires,
    }
    buffer = generate_card(data)
    st.image(buffer, caption="Aperçu de la fiche", use_container_width=True)
    st.download_button(
        label="📥 Télécharger la fiche",
        data=buffer,
        file_name="fiche_tournage.png",
        mime="image/png"
    )
