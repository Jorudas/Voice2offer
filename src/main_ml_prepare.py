
import re
import json

def extract_offer_data(text):
    data = {}

    # --- Plotas (m2) ---
    area_match = re.search(r"(\d+)\s*(?:m2|m²|kvadratin|kvadratiniu)", text, re.IGNORECASE)
    if area_match:
        data["plotas_m2"] = int(area_match.group(1))
    else:
        data["plotas_m2"] = None

    # --- Dekoro tipai ---
    t = text.lower()

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

    # --- Vieta (siena / lubos / kita) ---
    if "sien" in t:
        data["vieta"] = "Siena"
    elif "lub" in t:
        data["vieta"] = "Lubos"
    elif "grind" in t:
        data["vieta"] = "Grindys"
    else:
        data["vieta"] = "Neaišku"

    return data


# --- Testavimas ---
recognized_text = "Reikia lygus dekoras 28 kvadratinių metrų sienai"
offer_data = extract_offer_data(recognized_text)

print("Išgauta informacija iš užklausos:")
print(json.dumps(offer_data, indent=4, ensure_ascii=False))