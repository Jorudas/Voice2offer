
from src.db import SessionLocal
from src.models import VoiceMessage

db = SessionLocal()

irasai = db.query(VoiceMessage).all()

for irasas in irasai:
    print("---------------")
    print(f"ID: {irasas.id}")
    print(f"Failas: {irasas.file_path}")
    print(f"Tekstas: {irasas.transcription}")
    print(f"Plotas: {irasas.plotas_m2} m²")
    print(f"Darbų tipas: {irasas.darbu_tipas}")
    print(f"Terminas: {irasas.terminas}")
    print(f"Ištraukta info: {irasas.extracted_data}")
    print("---------------")

db.close()