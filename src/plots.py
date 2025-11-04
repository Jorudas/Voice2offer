
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import numpy as np


def generate_model_plots(db_path="voice2offer.db"):
    # 1. Nuskaitome duomenis
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        offers = session.query(Offer).all()

    if len(offers) < 5:
        return None  # jei duomenų per mažai

    df = pd.DataFrame([{
        "area": o.area,
        "price_per_m2": o.price_per_m2,
        "sum": o.total_sum
    } for o in offers])

    # 2. Paruošiame duomenis
    X = df[["area", "price_per_m2"]]
    y = (df["sum"] > df["sum"].median()).astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # 3. Modelis
    model = Sequential([
        Dense(8, activation="relu", input_shape=(X_train.shape[1],)),
        Dense(4, activation="relu"),
        Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer=Adam(0.01), loss="binary_crossentropy", metrics=["accuracy"])
    history = model.fit(X_train, y_train, epochs=30, batch_size=4, verbose=0)

    # 4. Accuracy/Loss grafikas
    fig1 = plt.figure(figsize=(5,3))
    plt.plot(history.history["accuracy"], label="Tikslumas")
    plt.plot(history.history["loss"], label="Nuostolis")
    plt.legend()
    plt.title("Mokymo kreivės")

    # 5. Klaidų matrica
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    cm = confusion_matrix(y_test, y_pred)
    fig2 = plt.figure(figsize=(4,4))
    plt.imshow(cm, cmap="Greens")
    plt.title("Klaidų matrica")

    # 6. Histograma
    fig3 = plt.figure(figsize=(5,3))
    df['sum'].plot(kind="hist", bins=6, color="skyblue")
    plt.title("Pasiūlymų sumos pasiskirstymas")

    return fig1, fig2, fig3