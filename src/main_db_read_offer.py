
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Offer

# Prisijungiame prie tos pačios duomenų bazės
engine = create_engine("sqlite:///test_offer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Nuskaitome visus įrašus iš lentelės 'offers'
offers = session.query(Offer).all()

print("📋 Lentelės 'offers' įrašai:")
for offer in offers:
    print(f"ID: {offer.id}, Decor: {offer.decor}, Plotas: {offer.area}, Kaina/m²: {offer.price_per_m2}, Suma: {offer.total_sum}, Failas: {offer.file_path}")

session.close()