
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# --- Nuskaitom duomenis iš DB ---
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

# --- Paruošiam duomenis ---
X = df[["area", "price_per_m2"]]
y = (df["sum"] > df["sum"].median()).astype(int)  # binarinis tikslas

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)

# --- Sukuriam neuroninį tinklą ---
model = Sequential([
    Dense(8, input_dim=X_train.shape[1], activation="relu"),
    Dense(4, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer=Adam(learning_rate=0.01),
              loss="binary_crossentropy",
              metrics=["accuracy"])

# --- Mokymas ---
print("\nMokome neuroninį tinklą...")
history = model.fit(X_train, y_train, epochs=50, batch_size=4, verbose=0)

# --- Vertinimas ---
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nNeuroninio tinklo tikslumas (accuracy): {accuracy:.2f}")

# --- Mokymo eiga (pirmos kelios epochos) ---
acc_values = history.history['accuracy'][:5]
print("Pirmos 5 epochos tikslumai:", [round(a, 3) for a in acc_values])