
import sqlite3
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline

# 1. Prisijungiame prie duomenų bazės
conn = sqlite3.connect("voice2offer.db")

# 2. Nuskaitome lentelę su transkripcijomis
df = pd.read_sql_query("SELECT * FROM voice_messages", conn)
print("✅ Duomenys iš DB sėkmingai nuskaityti:")
print(df.head())

# 3. Įkeliame anksčiau apmokytą modelį
model = joblib.load("data/model.pkl")
print("\n💾 Modelis įkeltas iš 'data/model.pkl'")

# 4. Tikriname, ar yra tekstas prognozei
if "transcription" not in df.columns:
    print("❌ Klaida: lentelėje nėra stulpelio 'transcription'")
else:
    # 5. Kuriame prognozes
    df["predicted_type"] = model.predict(df["transcription"])
    print("\n🤖 Prognozės sukurtos sėkmingai!")
    print(df[["id", "transcription", "predicted_type"]])

    # 6. Išsaugome prognozes atgal į duomenų bazę
    df.to_sql("voice_messages", conn, if_exists="replace", index=False)
    print("\n💾 Lentelė 'voice_messages' atnaujinta su prognozėmis!")

conn.close()