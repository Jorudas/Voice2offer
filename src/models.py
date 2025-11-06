
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    decor = Column(String)
    area = Column(Float)
    price_per_m2 = Column(Float)
    total_sum = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    file_path = Column(String)

# ✅ Automatiškai sukuria DB ir lentelę, jei jos nėra
engine = create_engine("sqlite:///voice2offer.db")
Base.metadata.create_all(engine)