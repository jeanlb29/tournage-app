import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- Configuration police ---
FONT_PATH_REGULAR = "fonts/Montserrat-Regular.ttf"
FONT_PATH_BOLD = "fonts/Montserrat-Bold.ttf"

# --- Configuration icons ---
def icon_path(name):
    return os.path.join("icons", name)

# --- Génération de la fiche en PNG ---
def generate_card(data):
    width, height = 1240, 1754  # format A4 vertical
    bg_color = (245, 245, 245)  # gris clair style Apple
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype(FONT_PATH_BOLD, 90)
    label_font = ImageFont.truetype(FONT_PATH_BOLD, 55)
    font = ImageFont.truetype(FONT_PATH_REGULAR, 55)

    # --- Titre ---
    title_text = "FICHE TOURNAGE"
    tw, th = draw.textbbox((0, 0), title_text, font=title_font)[2:]
    draw.text(((width - tw) / 2, 100), title_text, font=title_font, fill="black")

    # Ligne sous le titre
    draw.line([(150, 220), (width - 150, 220)], fill=(200, 200, 200), width=4)

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

    y = 320
    max_width = width - 300  # zone max pour texte

    for icon_file, label, valeur in lignes:
        path = icon_path(icon_file)

        # Icône
        if os.path.exists(path):
            try:
                icon = Image.open(path).convert("RGBA").resize((60, 60))
                img.paste(icon, (150, y), mask=icon)
            except Exception as e:
                st.write(f"❌ Erreur icône {icon_file} : {e}")

        # Label en gras
        draw.text((240, y), f"{label} :", font=label_font, fill="black")

        # Position texte valeur
        lw = draw.textlength(f"{label} :", font=label_font)
        text_x = 240 + lw + 20
        text_y = y

        # Découpe multi-lignes si nécessaire
        line_height = 0
        if valeur:
            words = valeur.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if draw.textlength(test_line, font=font) < (max_width - text_x):
                    line = test_line
                else:
                    draw.text((text_x, text_y), line, font=font, fill="black")
                    text_y += 65  # espace entre lignes
                    line = word + " "
            draw.text((text_x, text_y), line, font=font, fill="black")
            line_height = text_y - y + 80
        else:
            line_height = 100

        # Décalage dynamique
        y += line_height

    # Sauvegarde en mémoire
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

    st.image(image_bytes, caption="Aperçu de la fiche", use_column_width=True)
    st.download_button(
        label="📥 Télécharger la fiche (PNG)",
        data=image_bytes,
        file_name="fiche_tournage.png",
        mime="image/png",
    )
