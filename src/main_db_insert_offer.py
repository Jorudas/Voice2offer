
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Offer

# Prisijungiame prie DB
engine = create_engine("sqlite:///voice2offer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Sukuriame testinį įrašą
offers = [
    Offer(decor="Marmuro tinkas", area=25.0, price_per_m2=40.0, total_sum=1000.0, file_path="komercinis_pasiulymas_test.pdf"),
    Offer(decor="Uoliena", area=30.0, price_per_m2=50.0, total_sum=1500.0, file_path="test2.pdf"),
    Offer(decor="Betonas", area=20.0, price_per_m2=30.0, total_sum=600.0, file_path="test3.pdf"),
    Offer(decor="Kvarcas", area=45.0, price_per_m2=55.0, total_sum=2475.0, file_path="test4.pdf"),
    Offer(decor="Tadelakt", area=15.0, price_per_m2=80.0, total_sum=1200.0, file_path="test5.pdf"),
]

session.add_all(offers)
session.commit()
print("✅ Įkelti keli testiniai įrašai į lentelę 'offers'.")

import random

# Sugeneruojame 20 atsitiktinių įrašų
for i in range(20):
    area = round(random.uniform(10, 60), 1)
    price_per_m2 = round(random.uniform(25, 80), 1)
    total_sum = round(area * price_per_m2, 1)
    decor = random.choice(["Marmuro tinkas", "Uoliena", "Betonas", "Kvarcas", "Tadelakt"])
    file_path = f"auto_generated_{i}.pdf"

    offer = Offer(
        decor=decor,
        area=area,
        price_per_m2=price_per_m2,
        total_sum=total_sum,
        file_path=file_path
    )
    session.add(offer)

session.commit()
print("✅ Papildomai sugeneruota 20 atsitiktinių įrašų.")