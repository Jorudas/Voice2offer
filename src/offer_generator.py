
# src/offer_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Offer

try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
except Exception:
    pass


def generate_offer(data, db_path="voice2offer.db"):

    # Sukuriame /pdf aplanką
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_dir = os.path.join(base_dir, "pdf")
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # Laikinas failas kol nežinome ID
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    temp_name = f"komercinis_pasiulymas_{timestamp}.pdf"
    temp_path = os.path.join(pdf_dir, temp_name)

    # ---- PDF GENERAVIMAS ---
    c = canvas.Canvas(temp_path, pagesize=A4)
    width, height = A4

    logo_path = os.path.join(os.path.dirname(__file__), "data", "logo.png")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width - 8*cm, height - 7*cm, width=6*cm, height=4*cm, preserveAspectRatio=True)

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(2*cm, height - 2.2*cm, width - 2*cm, height - 2.2*cm)

    c.setFont("Arial", 12)
    c.drawString(2*cm, height - 3*cm, "KOMERCINIS PASIŪLYMAS")

    price_list = {
        "Uolienos imitacija": 450,
        "Marmuro tinkas": 40,
        "Kalkinis tinkas": 35,
        "Lygus dekoras": 45,
        "Betono imitacija": 90,
        "Struktūrinis dekoras": 42,
        "Tradicinis tinkas": 25
    }

    dekoras = data.get('dekoras', '')
    base_price = price_list.get(dekoras, 45)
    m2 = float(data.get('plotas_m2', 0) or 0)
    suma = base_price * m2
    mokestis = round(suma * 0.21, 2)
    bendra = round(suma + mokestis, 2)

    y = height - 4.8*cm
    c.setFont("Arial", 12)
    c.drawString(2*cm, y, f"Darbo tipas: {dekoras}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Dekoruojama vieta: {data.get('vieta', '')}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Bendras plotas: {m2} m²")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Kaina už 1 m²: {base_price:.2f} €")

    y -= 1.3*cm
    c.drawString(2*cm, y, "Kainų skaičiavimas:")
    y -= 1*cm
    c.drawString(2*cm, y, f"Suma EUR: {suma:.2f} €")
    y -= 0.6*cm
    c.drawString(2*cm, y, f"Mokesčiai (21%): {mokestis:.2f} €")
    y -= 0.6*cm
    c.drawString(2*cm, y, f"Bendra suma EUR: {bendra:.2f} €")

    y -= 1.2*cm
    c.setFont("Arial", 12)
    c.drawString(2*cm, y, "Pastabos:")

    style = ParagraphStyle(name="Normal", fontName="Arial", fontSize=11, leading=14, alignment=TA_LEFT)
    notes = [
        "• Už atliktus darbus išrašoma ne PVM sąskaita faktūra.",
        "• Kiekiai gali keistis po faktinių išmatavimų.",
        "• Papildomas 21% mokestis taikomas veiklos mokesčiams."
    ]

    y -= 0.3*cm
    for note in notes:
        paragraph = Paragraph(note, style)
        w, h = paragraph.wrap(16*cm, 2*cm)
        paragraph.drawOn(c, 2*cm, y - h)
        y -= h + 0.2*cm

    y -= 2*cm
    c.setFont("Arial", 11)
    c.drawString(2*cm, y, "Kontaktai:")
    y -= 0.6*cm
    c.drawString(2.5*cm, y, "Kęstutis Jorudas")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "Tel.: +37060065375")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "El. paštas: labas@marmurotinkas.lt")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "Tinklalapis: marmurotinkas.lt")

    today = datetime.date.today().strftime("%Y-%m-%d")
    c.setFont("Arial", 10)
    c.drawString(2*cm, 2*cm, f"Parengta: {today}")

    c.save()

    # ✅ Įrašas į DB
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        offer = Offer(
            decor=dekoras,
            area=m2,
            price_per_m2=base_price,
            total_sum=bendra,
            file_path=""
        )
        session.add(offer)
        session.commit()

        # ✅ Čia jau turime offer.id – dabar galutinis failo pavadinimas su data ir ID
        final_name = f"pasiulymas_ID{offer.id}_{timestamp}.pdf"
        final_path = os.path.join(pdf_dir, final_name)

        os.rename(temp_path, final_path)

        offer.file_path = final_name
        session.commit()

    finally:
        session.close()

    return {"pdf_path": final_path, "total_sum": bendra}