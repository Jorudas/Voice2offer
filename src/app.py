
# src/app.py
import whisper
import os
import soundfile as sf
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer
from offer_generator import generate_offer
from plots import generate_model_plots

DB_PATH = "voice2offer.db"

st.set_page_config(page_title="Voice2Offer - Mini UI", layout="centered")

# ✅ Sukuriame 3 puslapius
tab1, tab2, tab3 = st.tabs(["💼 Pasiūlymų generatorius", "📊 Modelių analizė", "🎧 Garso įkėlimas"])

# =========================================================
# ✅ TAB 1 – Pasiūlymų generatorius (TAVO ESAMAS KODAS)
# =========================================================
with tab1:
    st.title("Voice2Offer - komercinių pasiūlymų generatorius")

    st.subheader("Sukurti naują pasiūlymą (PDF + įrašas į DB)")

    with st.form("new_offer"):
        dekoras = st.selectbox(
            "Dekoras",
            ["Uolienos imitacija", "Marmuro tinkas", "Kalkinis tinkas", "Lygus dekoras", "Betono imitacija", "Struktūrinis dekoras", "Tradicinis tinkas"],
            index=1
        )
        plotas_m2 = st.number_input("Plotas, m²", min_value=0.0, step=1.0, value=20.0)
        vieta = st.text_input("Vieta (pvz., siena, koridorius)", value="Siena")
        submitted = st.form_submit_button("Generuoti PDF ir įrašyti")

    if submitted:
        data = {"dekoras": dekoras, "plotas_m2": plotas_m2, "vieta": vieta}
        result = generate_offer(data, db_path=DB_PATH)

        st.success("✅ Pasiūlymas sukurtas ir įrašytas į DB.")
        st.write(f"**PDF failas:** {result['pdf_path']}")
        st.write(f"**Bendra suma:** {result['total_sum']:.2f} €")

        # ✅ PDF ATSISIUNTIMO MYGTUKAS
        try:
            with open(result["pdf_path"], "rb") as f:
                st.download_button(
                    label="📥 Atsisiųsti PDF",
                    data=f,
                    file_name=result["pdf_path"].split("\\")[-1],
                    mime="application/pdf"
                )
        except:
            st.warning("⚠️ Nepavyko įkelti PDF atsisiuntimui (gal failas ne tame kataloge?)")

    # ✅ Lentelė iš DB
    st.divider()
    st.subheader("Esami pasiūlymai (iš DB)")

    engine = create_engine(f"sqlite:///{DB_PATH}")
    with Session(engine) as session:
        rows = session.query(Offer).order_by(Offer.id.desc()).all()

    data = []
    for r in rows:
        data.append({
            "ID": r.id,
            "DEKORAVIMO TIPAS": r.decor,
            "KIEKIS_m2": r.area,
            "KAINA_EUR_be_PVM": r.price_per_m2,
            "SUMA_EUR_su_PVM": r.total_sum,
            "Sukurta": getattr(r, "created_at", None)
        })

    df = pd.DataFrame(data)

    # ✅ Pridedame mygtukus: Peržiūrėti PDF ir Atsisiųsti
    def file_buttons(row):
        # Sukuriame failo pavadinimą
        pdf_name = f"Pasiūlymas #{row['ID']} ({str(row['Sukurta']).split()[0]}).pdf" if row["Sukurta"] else f"Pasiūlymas #{row['ID']}.pdf"

        # Pilnas kelias iki failo
        full_path = os.path.join(os.getcwd(), "pdf", pdf_name)

        # Jei failas egzistuoja
        if os.path.exists(full_path):
            # Peržiūrėjimo nuoroda
            view_link = f'<a target="_blank" href="file:///{full_path}">👁️ Peržiūrėti</a>'

            # Atsisiuntimo mygtukas
            with open(full_path, "rb") as f:
                download_button = st.download_button(
                    label="💾 Atsisiųsti",
                    data=f,
                    file_name=pdf_name,
                    mime="application/pdf",
                    key=f"dl_{row['ID']}"
                )

            return view_link + " | " + download_button

        return "❌ Failas nerastas"

    # ✅ Sukuriame stulpelį 'Veiksmai'
    df["Veiksmai"] = df.apply(file_buttons, axis=1)

    st.write(df)
    


# =========================================================
# ✅ TAB 2 – ML/NN grafikai
# =========================================================
with tab2:
    st.title("📊 ML ir neuroninių tinklų analizė")
    st.write("Čia bus atvaizduojami modelio tikslumo ir mokymo grafikai.")

    if st.button("Generuoti ir atvaizduoti grafikus"):
        result = generate_model_plots(DB_PATH)

        if result is None:
            st.warning("⚠️ Per mažai duomenų modeliui mokyti (reikia bent 5 pasiūlymų).")
        else:
            fig1, fig2, fig3 = result

            st.subheader("📈 Mokymo kreivės (Accuracy/Loss)")
            st.pyplot(fig1)

            st.subheader("✅ Klaidų matrica")
            st.pyplot(fig2)

            st.subheader("📊 Sumų pasiskirstymo histograma")
            st.pyplot(fig3)


# =========================================================
# ✅ TAB 3 – Garso įrašymas ir PDF automatinis generavimas
# =========================================================
from audiorecorder import audiorecorder
import os
from voice_pipeline import transcribe_audio, create_offer_from_text

DB_PATH = "voice2offer.db"

with tab3:
    st.title("🎧 Garso įrašymas arba įkėlimas")
    st.write("Įrašykite arba įkelkite balso įrašą – automatiškai transkribuosime, išanalizuosime ir sukursime PDF + įrašą į DB.")

    # --------- 1) Įrašas naršyklėje ----------
    st.subheader("🎤 Įrašyti balsą")
    audio = audiorecorder("🎙 Pradėti įrašymą", "⏹ Sustabdyti")

    if audio and len(audio) > 0:
        st.audio(audio.raw_data, format="audio/wav")
        record_path = "temp_record.wav"
        audio.export(record_path, format="wav")
        st.success("✅ Įrašas sėkmingai padarytas!")

        with st.spinner("⏳ Transkribuojame ir generuojame pasiūlymą..."):
            text = transcribe_audio(record_path, lang="lt")
            st.write("### 📝 Išgautas tekstas:")
            st.write(text)

            result = create_offer_from_text(text, db_path=DB_PATH)

        st.success("✅ Pasiūlymas automatiškai sukurtas!")
        st.write(f"**PDF:** {result['pdf_path']}")
        st.write(f"**Suma:** {result['total_sum']:.2f} €")

        try:
            with open(result["pdf_path"], "rb") as f:
                st.download_button("📥 Atsisiųsti PDF", data=f, file_name=os.path.basename(result["pdf_path"]), mime="application/pdf")
        except:
            st.warning("⚠ Nepavyko pateikti PDF atsisiuntimui.")

        try:
            os.remove(record_path)
        except:
            pass

    st.divider()

    # --------- 2) Įkelti garso failą ----------
    st.subheader("📂 Įkelti garso failą")
    uploaded_file = st.file_uploader("Pasirinkite WAV/MP3/FLAC", type=["wav", "mp3", "flac"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")

        temp_path = "temp_uploaded_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("⏳ Transkribuojame ir generuojame pasiūlymą..."):
            text = transcribe_audio(temp_path, lang="lt")
            st.write("### 📝 Išgautas tekstas:")
            st.write(text)

            result = create_offer_from_text(text, db_path=DB_PATH)

        st.success("✅ Pasiūlymas automatiškai sukurtas!")
        st.write(f"**PDF:** {result['pdf_path']}")
        st.write(f"**Suma:** {result['total_sum']:.2f} €")

        try:
            with open(result["pdf_path"], "rb") as f:
                st.download_button("📥 Atsisiųsti PDF", data=f, file_name=os.path.basename(result["pdf_path"]), mime="application/pdf")
        except:
            st.warning("⚠ Nepavyko pateikti PDF atsisiuntimui.")

        try:
            os.remove(temp_path)
        except:
            pass