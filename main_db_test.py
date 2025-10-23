
from src.db import SessionLocal
from src.models import VoiceMessage
from src.data_extractor import extract_data
import json

# Sukuriam sesiją
session = SessionLocal()

# Nuskaitom visus įrašus iš DB
messages = session.query(VoiceMessage).all()

for msg in messages:
    extracted = extract_data(msg.transcription)
    msg.extracted_data = json.dumps(extracted, ensure_ascii=False)
    print(f"Atnaujinta: ID={msg.id}, Duomenys={extracted}")

# Išsaugom pakeitimus
session.commit()
session.close()

print("✅ Visi įrašai atnaujinti su išgautais duomenimis.")