
import sqlite3
import pandas as pd

# 1. Prisijungiame prie duomenų bazės
conn = sqlite3.connect("voice2offer.db")

# 2. Nuskaitome lentelę 'voice_messages' į DataFrame
df = pd.read_sql_query("SELECT * FROM voice_messages", conn)

# 3. Parodome pirmas eilutes
print("✅ Duomenys iš DB sėkmingai nuskaityti:")
print(df.head())

import json

# 5. Ištraukiame duomenis iš JSON lauko 'extracted_data'
def parse_extracted(row):
    try:
        return json.loads(row)
    except:
        return {}

# Pritaikome funkciją visai lentelei
def clean_json_string(x):
    if not isinstance(x, str):
        return {}
    try:
        cleaned = x.replace('\\"', '"').replace('"{', '{').replace('}"', '}')
        return json.loads(cleaned)
    except Exception as e:
        print(f"Klaida apdorojant JSON: {e}\nEilutė: {x}")
        return {}

extracted = df["extracted_data"].apply(clean_json_string)
extracted_df = pd.json_normalize(extracted)

# Sujungiame su pagrindiniais duomenimis
df = pd.concat([df, extracted_df], axis=1)

print("\n✅ Ištraukti stulpeliai iš 'extracted_data':")
print(df.head())

# 4. Uždarome prisijungimą
conn.close()

# 6. Išsaugome duomenis į CSV modeliui
output_path = "data/voice_data_clean.csv"
import os
os.makedirs("data", exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\n✅ Duomenys sėkmingai išsaugoti į: {output_path}")