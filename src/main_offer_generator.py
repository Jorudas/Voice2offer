
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

# Registruojame šriftą
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))

def generate_offer(data):
    # Sukuriame laiko žymą su data ir valandomis/minutėmis
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Sukuriame absoliutų kelią iki PDF šakniniame kataloge
    base_dir = os.path.dirname(os.path.dirname(__file__))  # išeiname iš src/
    file_name = os.path.join(base_dir, f"komercinis_pasiulymas_{timestamp}.pdf")

    print(f"📁 PDF bus sukurtas čia: {file_name}")

    # Jei toks failas jau yra – pašaliname seną
    if os.path.exists(file_name):
        os.remove(file_name)
        print("🧹 Senas failas pašalintas.")

    # Sukuriame PDF
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # --- Logotipas (dešinėje virš projekto informacijos) ---
    logo_path = os.path.join(os.path.dirname(__file__), "data", "logo.png")

    if os.path.exists(logo_path):
        print(f"Logotipas įkeltas iš: {logo_path}")
        # Paveikslo vieta – apie puslapio viršutinį trečdalį, dešinėje pusėje
        c.drawImage(
            logo_path,
            width - 8*cm,   # horizontalus atstumas nuo kairio krašto
            height - 7*cm, # vertikalus atstumas nuo viršaus
            width=6*cm,     # logotipo plotis
            height=4*cm,    # logotipo aukštis
            preserveAspectRatio=True
        )
    else:
        print(f"Logotipas nerastas šiame kelyje: {logo_path}")

    # --- Viršutinė linija ---
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(2*cm, height - 2.2*cm, width - 2*cm, height - 2.2*cm)

    # --- Antraštė ---
    c.setFont("Arial", 12)
    c.drawString(2*cm, height - 3*cm, "KOMERCINIS PASIŪLYMAS")

    # --- Apskaičiuojame kainas (tik kintamieji, be išvedimo) ---
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
    m2 = data.get('plotas_m2', 0)
    suma = base_price * m2
    mokestis = round(suma * 0.21, 2)
    bendra = round(suma + mokestis, 2)

    # --- Projekto informacija ---
    c.setFont("Arial", 12)
    y = height - 4.8*cm
    c.drawString(2*cm, y, f"Darbo tipas: {data.get('dekoras', '')}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Dekoruojama vieta: {data.get('vieta', '')}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Bendras plotas: {data.get('plotas_m2', '')} m²")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Kaina už 1 m²: {base_price:.2f} €")
    y -= 0.7*cm


    # --- Lentele su kainomis ---
    y -= 1.3*cm
    c.setFont("Arial", 12)
    c.drawString(2*cm, y, "Kainų skaičiavimas:")

    c.setFont("Arial", 12)
    y -= 1*cm
    c.drawString(2*cm, y, f"Suma EUR: {suma:.2f} €")
    y -= 0.6*cm
    c.drawString(2*cm, y, f"Mokesčiai (ne PVM) – 21 %: {mokestis:.2f} €")
    y -= 0.6*cm
    c.drawString(2*cm, y, f"Bendra suma EUR: {bendra:.2f} €")

    # --- Pastabos ---
    y -= 1.2*cm
    c.setFont("Arial", 12)
    c.drawString(2*cm, y, "Pastabos:")

    # Paruošiame stilių su automatinio laužymo parama
    style = ParagraphStyle(
        name="Normal",
        fontName="Arial",
        fontSize=11,
        leading=14,  # tarp eilučių
        alignment=TA_LEFT
    )

    notes = [
        "• Už atliktus darbus išrašoma ne PVM sąskaita faktūra.",
        "• Kiekiai gali keistis po faktinių plokštumų išmatavimų ir jei darbų eigoje bus nuspręsta dekoruoti papildomus, iš anksto nenumatytus plotus.",
        "• Nors veikla vykdoma pagal individualią veiklą ir PVM nėra skaičiuojamas atskirai, prie kainos papildomai pridedamas 21 % mokestis. "
        "Ši suma reikalinga padengti valstybės nustatytus mokesčius, taikomus individualiai veiklai."
    ]

    y -= 0.3*cm
    for note in notes:
        paragraph = Paragraph(note, style)
        w, h = paragraph.wrap(16*cm, 2*cm)  # gauk realų teksto aukštį
        paragraph.drawOn(c, 2*cm, y - h)
        y -= h + 0.2*cm  # 0.4 cm buvo tarpas tarp pastabų, dabar 0.2 cm

    # --- Kontaktinė informacija ---
    y -= 2*cm
    c.setFont("Arial", 11)
    c.drawString(2*cm, y, "Kontaktai:")
    y -= 0.6*cm
    c.setFont("Arial", 11)
    c.drawString(2.5*cm, y, "Kęstutis Jorudas")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "Tel.: +37060065375")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "El. paštas: labas@marmurotinkas.lt")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, "Tinklalapis: marmurotinkas.lt")

    # --- Data ---
    today = datetime.date.today().strftime("%Y-%m-%d")
    c.setFont("Arial", 10)
    c.drawString(2*cm, 2*cm, f"Parengta: {today}")

    c.save()
    print(f"✅ PDF pasiūlymas sėkmingai išsaugotas: {file_name}")


# Testavimo blokas (vykdomas tik jei paleidi šį failą tiesiogiai)
if __name__ == "__main__":
    test_data = {
        "plotas_m2": 35,
        "dekoras": "Uolienos imitacija",
        "vieta": "Siena"
    }

    generate_offer(test_data)