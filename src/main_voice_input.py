
import speech_recognition as sr
import sqlite3
from datetime import datetime
import os

DB_PATH = "voice2offer.db"
AUDIO_FILE = "data/audio2.mp3"  # Galima pakeisti į kitą failą

def recognize_speech(file_path):
    """Atpažįsta lietuvišką kalbą iš garso failo"""
    if not os.path.exists(file_path):
        print(f"Klaida: failas '{file_path}' nerastas.")
        return None

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="lt-LT")
            return text
    except sr.UnknownValueError:
        print("Nepavyko atpažinti kalbos – galbūt per tylus arba triukšmingas garsas.")
        return None
    except sr.RequestError as e:
        print(f"Klaida jungiantis prie Google API: {e}")
        return None
    except Exception as e:
        print(f"Nenumatyta klaida: {e}")
        return None

def save_to_db(file_path, text):
    """Įrašo atpažintą tekstą į voice_messages lentelę"""
    if text is None or text.strip() == "":
        print("Nėra teksto įrašymui į DB – praleidžiama.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO voice_messages (file_path, transcription, terminas, extracted_data, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (file_path, text, "1 savaitė", "{}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()
        print("Nauja balso žinutė įrašyta į DB sėkmingai.")
    except sqlite3.Error as e:
        print(f"Klaida įrašant į duomenų bazę: {e}")

if __name__ == "__main__":
    print("Pradedamas balso failo apdorojimas...")
    text = recognize_speech(AUDIO_FILE)
    if text:
        print(f"Atpažintas tekstas:\n{text}")
        save_to_db(AUDIO_FILE, text)
    else:
        print("Nepavyko apdoroti balso žinutės.")