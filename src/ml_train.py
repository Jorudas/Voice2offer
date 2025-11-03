
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer

# --- Nuskaitom duomenis iš voice2offer.db ---
engine = create_engine("sqlite:///voice2offer.db")
with Session(engine) as session:
    offers = session.query(Offer).all()

data = []
for o in offers:
    data.append({
        "area": o.area,
        "price_per_m2": o.price_per_m2,
        "sum": o.total_sum
    })

df = pd.DataFrame(data)
print("Duomenys iš DB:")
print(df.head())

# --- Paruošiam požymius ir taikinį ---
X = df[["area", "price_per_m2"]]  # požymiai
y = (df["sum"] > df["sum"].median()).astype(int)  # 1 jei didesnė už medianą

# --- Padalinam į mokymo ir testavimo rinkinius ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Sukuriam modelį ---
model = LogisticRegression()
model.fit(X_train, y_train)

# --- Prognozė ir tikslumas ---
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModelio tikslumas (accuracy):", accuracy)
print("Prognozės pavyzdžiai:", y_pred)