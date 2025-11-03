
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Offer

# Prisijungiame prie DB
engine = create_engine("sqlite:///test_offer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Sukuriame testinį įrašą
offer = Offer(
    decor="Marmuro tinkas",
    area=25.0,
    price_per_m2=40.0,
    total_sum=1000.0,
    file_path="komercinis_pasiulymas_test.pdf"
)

session.add(offer)
session.commit()
print("✅ Testinis įrašas sėkmingai pridėtas į lentelę 'offers'.")