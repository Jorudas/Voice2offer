
import sqlite3
import pandas as pd
import joblib
import time
import argparse
import datetime
from sklearn.pipeline import Pipeline

MODEL_PATH = "data/model.pkl"
DB_PATH = "voice2offer.db"

def log(msg):
    """Gražus log su laiku"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

def check_new_messages():
    """Tikrina duomenų bazę ir pritaiko prognozes naujiems įrašams"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM voice_messages", conn)
    except Exception as e:
        log(f"⚠️ Klaida nuskaitant duomenis iš DB: {e}")
        return

    # Jei nėra 'predicted_type' stulpelio – sukuriame tuščią
    if "predicted_type" not in df.columns:
        df["predicted_type"] = None

    # Randame įrašus be prognozės
    new_rows = df[df["predicted_type"].isnull()]

    if new_rows.empty:
        log("⏳ Naujų įrašų kol kas nėra...")
        conn.close()
        return

    log(f"🔍 Rasta {len(new_rows)} naujų įrašų be prognozės.")

    # Įkeliame modelį
    try:
        model = joblib.load(MODEL_PATH)
        log("💾 Modelis įkeltas.")
    except Exception as e:
        log(f"❌ Nepavyko įkelti modelio: {e}")
        conn.close()
        return

    # Sukuriame prognozes
    try:
        new_rows = new_rows.copy()
        new_rows["predicted_type"] = model.predict(new_rows["transcription"])
    except Exception as e:
        log(f"❌ Klaida generuojant prognozes: {e}")
        conn.close()
        return

    # Atnaujiname pagrindinę lentelę
    try:
        df.update(new_rows)
        df.to_sql("voice_messages", conn, if_exists="replace", index=False)
        conn.close()
        log(f"🤖 Atnaujinta {len(new_rows)} įrašų su prognozėmis!\n")
    except Exception as e:
        log(f"⚠️ Klaida atnaujinant duomenų bazę: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Vystymo režimas (kas 30s)")
    args = parser.parse_args()

    interval = 30 if args.dev else 86400  # 30s testavimui, 24h realiam režimui
    mode = "Vystymo (kas 30s)" if args.dev else "Produkcijos (kas 24h)"

    print(f"\n🚀 Paleista realaus laiko analizės sistema (Voice2offer AI) – {mode}")
    print(f"Sistema tikrins duomenų bazę kas {interval} sekundžių.\nNutraukti – Ctrl + C\n")

    while True:
        try:
            check_new_messages()
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Sistema sustabdyta rankiniu būdu.")
            break
        except Exception as e:
            log(f"❌ Klaida cikle: {e}")
            time.sleep(interval)