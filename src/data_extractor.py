
import re

def extract_data(text):
    data = {}

    # Plotui (pvz.: 20 m² arba 35 m2)
    match_pl = re.search(r"(\d+)\s?(m²|m2)", text)
    if match_pl:
        data["plotas"] = float(match_pl.group(1))

    # Darbų tipui
    if "marmuro" in text.lower():
        data["tipas"] = "marmuro_tinkas"
    elif "uolienos" in text.lower():
        data["tipas"] = "uolienos_imitacija"
    else:
        data["tipas"] = "nežinoma"

    # Terminui
    if "dien" in text.lower():
        data["terminas"] = "kelios dienos"
    elif "savait" in text.lower():
        data["terminas"] = "1 savaitė"
    else:
        data["terminas"] = "nenustatytas"

    return data