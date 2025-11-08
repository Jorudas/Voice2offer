
import os
import re
import json
from typing import Optional, Dict
from dotenv import load_dotenv   
load_dotenv()
print("DEBUG ENV KEY ===", os.getenv("OPENAI_API_KEY"))
from openai import OpenAI
import soundfile as sf

from offer_generator import generate_offer


# ✅ 1. API client (saugiai per ENV arba tiesiogiai)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# ✅ 2. Transkripcija
def transcribe_audio(audio_path: str, lang: str = "lt") -> str:
    with open(audio_path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f,
            response_format="text",
            language=lang
        )
    return str(resp).strip()


# ✅ 3. GPT JSON ištraukimui
def gpt_extract_offer_data(recognized_text: str) -> Dict:
    prompt = f"""
Tu esi ekspertas, kuris analizuoja lietuvišką klientų balso tekstą.
Tikslas – išgauti duomenis komerciniam pasiūlymui.

Grąžink TIK JSON:
{{
  "plotas_m2": <skaicius arba null>,
  "dekoras": "<string arba null>",
  "vieta": "<string arba null>"
}}

- leistinas šveplavimas, šnekta ("olienos", "uolenos", "istrintas", "senovinis")
- jei nerandi reikšmės → null
- NEGALIMA rašyti nieko be JSON (jokių sakinių ar komentarų)

Apdorojamas tekstas:
\"\"\"{recognized_text}\"\"\""""

    # ✅ GPT kvietimas
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu esi griežtas JSON ekstraktorius. Atsakyk TIK JSON formatu."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0
    )

    if not resp or not resp.choices or not resp.choices[0].message or not resp.choices[0].message.content:
        raise RuntimeError(f"ChatCompletions grąžino tuščią atsakymą. Debug: {resp}")

    raw_text = resp.choices[0].message.content.strip()
    print("DEBUG raw_text >>>", repr(raw_text))

    # ✅ 1 bandymas: tiesioginis JSON
    try:
        return json.loads(raw_text)
    except:
        pass

    # ✅ 2 bandymas: ištraukti JSON iš teksto
    m = re.search(r"\{.*\}", raw_text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            pass

    # ✅ 3 bandymas: paprašyti GPT išgryninti JSON
    fix_prompt = f"""
Pateik TIK JSON, be jokio teksto:

{{
  "plotas_m2": skaicius arba null,
  "dekoras": tekstas arba null,
  "vieta": tekstas arba null
}}

Išvalyk ir grąžink:
\"\"\"{raw_text}\"\"\""""

    fix_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Atsakyk TIK JSON formatu."},
            {"role": "user", "content": fix_prompt}
        ],
        max_tokens=100,
        temperature=0
    )

    clean = fix_resp.choices[0].message.content.strip()

    m = re.search(r"\{.*\}", clean, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            pass

    raise RuntimeError("GPT negrąžino JSON. Gauta:\n" + raw_text)

# ✅ 4. Fuzzy korekcija
def normalize_offer_fields(data: Dict) -> Dict:
    t_decor = (data.get("dekoras") or "").lower().strip()
    t_vieta = (data.get("vieta") or "").lower().strip()

    uolien_syn = ["uolien", "olien", "uolen", "akmens imit"]
    beton_syn = ["beton", "betonk", "betono efekt"]
    marmur_syn = ["marmur"]
    lygus_syn = ["lyg", "glotn", "glanc", "istrint"]
    sendin_syn = ["send", "senovin", "rustic", "seniuot"]

    if any(x in t_decor for x in uolien_syn):
        dekoras = "Uolienos imitacija"
    elif any(x in t_decor for x in beton_syn):
        dekoras = "Betono imitacija"
    elif any(x in t_decor for x in marmur_syn):
        dekoras = "Marmuro tinkas"
    elif any(x in t_decor for x in lygus_syn):
        dekoras = "Lygus dekoras"
    elif any(x in t_decor for x in sendin_syn):
        dekoras = "Sendinimas"
    else:
        dekoras = data.get("dekoras") or "Nenurodytas"

    if "sien" in t_vieta:
        vieta = "Siena"
    elif "lub" in t_vieta:
        vieta = "Lubos"
    elif "grind" in t_vieta:
        vieta = "Grindys"
    else:
        vieta = "Neaišku"

    plotas = data.get("plotas_m2")
    try:
        plotas = int(plotas) if plotas is not None else 0
    except:
        plotas = 0

    return {
        "dekoras": dekoras,
        "plotas_m2": plotas,
        "vieta": vieta
    }


# ✅ 5. VISAS PROCESAS (tekstas → JSON → PDF + DB)
def create_offer_from_text(recognized_text: str, db_path="voice2offer.db") -> Dict:
    raw = gpt_extract_offer_data(recognized_text)
    cleaned = normalize_offer_fields(raw)
    return generate_offer(cleaned, db_path=db_path)