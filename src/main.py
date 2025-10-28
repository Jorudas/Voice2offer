
import whisper
import re
import json

# --- 1. Analizės funkcija ---
def extract_offer_data(text):
    data = {}
    t = text.lower()

    # Ploto paieška
    area_match = re.search(r"(\d+)\s*(?:m2|m²|kvadratin|kvadratiniu)", t, re.IGNORECASE)
    data["plotas_m2"] = int(area_match.group(1)) if area_match else None

    # Dekoro paieška
    if "uolien" in t or "olien" in t:
        data["dekoras"] = "Uolienos imitacija"
    elif "marmur" in t:
        data["dekoras"] = "Marmuro tinkas"
    elif "kalk" in t:
        data["dekoras"] = "Kalkinis tinkas"
    elif "lygus" in t:
        data["dekoras"] = "Lygus dekoras"
    elif "beton" in t:
        data["dekoras"] = "Betono imitacija"
    elif "strukt" in t:
        data["dekoras"] = "Struktūrinis dekoras"
    elif "tradic" in t:
        data["dekoras"] = "Tradicinis tinkas"
    else:
        data["dekoras"] = "Nenurodytas"

    # Vietos paieška
    if "sien" in t:
        data["vieta"] = "Siena"
    elif "lub" in t:
        data["vieta"] = "Lubos"
    elif "grind" in t:
        data["vieta"] = "Grindys"
    else:
        data["vieta"] = "Neaišku"

    return data


# --- 2. Pasiūlymo generavimo funkcija ---
def generate_offer(data):
    price_list = {
        "Uolienos imitacija": 45,
        "Marmuro tinkas": 40,
        "Kalkinis tinkas": 35,
        "Lygus dekoras": 30,
        "Betono imitacija": 38,
        "Struktūrinis dekoras": 42,
        "Tradicinis tinkas": 25
    }

    dekoras = data.get("dekoras", "Nenurodytas")
    plotas = data.get("plotas_m2", 0)
    vieta = data.get("vieta", "Neaišku")

    kaina_m2 = price_list.get(dekoras, 0)
    suma = kaina_m2 * plotas if plotas else 0

    offer_text = f"""
KOMERCINIS PASIŪLYMAS

Darbo tipas: {dekoras}
Dekoruojama vieta: {vieta}
Bendras plotas: {plotas} m²

Vieneto kaina: {kaina_m2} €/m²
Bendra suma: {suma} €

Pastabos:
• Kaina nurodyta be PVM.
• Galutinė suma gali kisti pagal faktinį darbų kiekį ir sudėtingumą.
"""
    return offer_text.strip()


# --- 3. Balso atpažinimas su Whisper ---
model = whisper.load_model("large-v3")
audio_path = r"C:\1 JORUDAS\DOC Jorudas\AI\PROJEKTAI\Voice2offer\src\data\audio2.wav"

result = model.transcribe(audio_path, language="lt", fp16=False)
recognized_text = result["text"]

print("\nAtpažintas tekstas:")
print(recognized_text)

# --- 4. Teksto analizė ---
offer_data = extract_offer_data(recognized_text)

print("\nIšgauta informacija iš užklausos:")
print(json.dumps(offer_data, indent=4, ensure_ascii=False))

# --- 5. Pasiūlymo generavimas ---
offer_text = generate_offer(offer_data)

print("\nSugeneruotas pasiūlymas:")
print(offer_text)

# --- 6. Išsaugome faile ---
with open("komercinis_pasiulymas.txt", "w", encoding="utf-8") as f:
    f.write(offer_text)