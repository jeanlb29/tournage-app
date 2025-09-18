import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- Fonts ---
FONT_PATH_REGULAR = "fonts/Montserrat-Regular.ttf"
FONT_PATH_BOLD = "fonts/Montserrat-Bold.ttf"

# --- Icons ---
def icon_path(name):
    return os.path.join("icons", name)

# --- Génération de la fiche en PNG ---
def generate_card(data):
    width, height = 1240, 1754  # A4 vertical
    bg_color = (255, 255, 255)  # fond blanc pur
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype(FONT_PATH_BOLD, 90)
    label_font = ImageFont.truetype(FONT_PATH_BOLD, 50)
    font = ImageFont.truetype(FONT_PATH_REGULAR, 50)

    # --- Marges globales ---
    margin = 120
    content_width = width - 2 * margin

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    tw, th = draw.textbbox((0, 0), title_text, font=title_font)[2:]
    draw.text(((width - tw) / 2, margin), title_text, font=title_font, fill="black")

    # Ligne fine sous le titre
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

    y = line_y + 100  # départ après la ligne

    for icon_file, label, valeur in lignes:
        # Icône
        path = icon_path(icon_file)
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((50, 50))
                img.paste(icon, (margin, y), mask=icon)
            except Exception as e:
                st.write(f"⚠️ Erreur icône {icon_file} : {e}")

        # Label (gris foncé, bold)
        draw.text((margin + 70, y), f"{label} :", font=label_font, fill="#333333")

        # Position valeur
        lw = draw.textlength(f"{label} :", font=label_font)
        text_x = margin + 70 + lw + 25
        text_y = y

        # Largeur max plus grande
        max_width = width - margin - text_x

        # Multi-lignes
        if valeur:
            words = valeur.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if draw.textlength(test_line, font=font) <= max_width:
                    line = test_line
                else:
                    draw.text((text_x, text_y), line, font=font, fill="black")
                    text_y += 65
                    line = word + " "
            draw.text((text_x, text_y), line, font=font, fill="black")
            y = text_y + 90
        else:
            y += 90

    # Sauvegarde
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


# --- App Streamlit ---
st.title("🎬 Générateur de Fiche Tournage")

with st.form("fiche_form"):
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
    image_bytes = generate_card(data)

    st.image(image_bytes, caption="Aperçu de la fiche", use_container_width=True)
    st.download_button(
        label="📥 Télécharger la fiche (PNG)",
        data=image_bytes,
        file_name="fiche_tournage.png",
        mime="image/png",
    )
