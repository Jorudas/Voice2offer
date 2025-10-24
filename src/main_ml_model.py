
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. Įkeliame išvalytus duomenis
df = pd.read_csv("data/voice_data_clean.csv")

print("✅ Duomenys įkelti sėkmingai!\n")
print(df.head())

# 2. Patikriname stulpelius
print("\nStulpeliai:")
print(df.columns.tolist())

# 3. Patikriname, kiek turime įrašų
print(f"\nIš viso įrašų: {len(df)}")

# 4. Pasiruošiame duomenis modeliui
X = df["transcription"]      # tekstas (įvestis)
y = df["tipas"]              # darbų tipas (etiketė)

# 5. Sukuriame modelį (TF-IDF + Naive Bayes)
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# 6. Apmokome modelį (testinis režimas)
model.fit(X, y)

print("\n✅ Modelis sėkmingai apmokytas (testinis režimas)!")

import joblib

# 7. Išsaugome apmokytą modelį
model_path = "data/model.pkl"
joblib.dump(model, model_path)
print(f"\n💾 Modelis išsaugotas į: {model_path}")

# 8. Sukuriame testinį pavyzdį
naujas_tekstas = ["Reikia marmuro tinko 20 m² sienai per savaitę"]
prognoze = model.predict(naujas_tekstas)[0]

print(f"\n🤖 Prognozė naujam tekstui: {prognoze}")
