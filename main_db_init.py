from src.db import Base, engine
from src import models

if __name__ == "__main__":
    print("Kuriu duomenų bazės lenteles...")
    Base.metadata.create_all(bind=engine)
    print("OK. Sukurta 'voice2offer.db' ir lentelės.")