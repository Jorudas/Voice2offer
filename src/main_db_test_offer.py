
from sqlalchemy import create_engine, inspect

# Prisijungiame prie tos pačios DB
engine = create_engine("sqlite:///test_offer.db")

# Naudojame inspektorių, kad pažiūrėtume lenteles
inspector = inspect(engine)
tables = inspector.get_table_names()

print("Esančios lentelės duomenų bazėje:")
for table in tables:
    print(" -", table)