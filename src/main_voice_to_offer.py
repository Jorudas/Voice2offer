import whisper
import re
import json

# --- 1. Funkcija analizei (iš main_ml_prepare.py) ---
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


# --- 2. Whisper modelis ---
model = whisper.load_model("large-v3")
audio_path = r"C:\1 JORUDAS\DOC Jorudas\AI\PROJEKTAI\Voice2offer\src\data\audio2.wav"

# --- 3. Transkribuojame balsą ---
result = model.transcribe(audio_path, language="lt", fp16=False)
recognized_text = result["text"]

print("\nAtpažintas tekstas:")
print(recognized_text)

# --- 4. Analizuojame užklausą ---
offer_data = extract_offer_data(recognized_text)

print("\nIšgauta informacija iš užklausos:")
print(json.dumps(offer_data, indent=4, ensure_ascii=False))
