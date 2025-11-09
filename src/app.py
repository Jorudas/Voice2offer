
# src/app.py
import whisper
import os
import soundfile as sf
import streamlit as st
import pandas as pd
import base64
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
# ✅ TAB 1 – Pasiūlymų generatorius
# =========================================================
with tab1:
    st.title("Voice2Offer - komercinių pasiūlymų generatorius")

    st.subheader("Sukurti naują pasiūlymą (PDF + įrašas į DB)")

    with st.form("new_offer"):
        dekoras = st.selectbox(
            "Dekoras",
            ["Uolienos imitacija", "Marmuro tinkas", "Kalkinis tinkas",
             "Lygus dekoras", "Betono imitacija", "Struktūrinis dekoras", "Tradicinis tinkas"],
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

        with open(result["pdf_path"], "rb") as f:
            st.download_button(
                label="📥 Atsisiųsti PDF",
                data=f,
                file_name=os.path.basename(result["pdf_path"]),
                mime="application/pdf"
            )

    # ✅ Lentelė iš DB su atsisiuntimu
    st.divider()
    st.subheader("Esami pasiūlymai duomenų bazėje")

    engine = create_engine(f"sqlite:///{DB_PATH}")
    with Session(engine) as session:
        rows = session.query(Offer).order_by(Offer.id.desc()).all()

    table_data = []
    for r in rows:
        # Reali PDF vieta
        pdf_folder = os.path.join(os.path.dirname(__file__), "..", "pdf")
        full_path = os.path.join(pdf_folder, r.file_path)

        # ✅ vietoje neveikiančio HTML – grąžiname mygtuko placeholderį
        if os.path.exists(full_path):
            download_html = f"__BTN__{r.id}"
        else:
            download_html = "❌ Failas nerastas"

        table_data.append({
            "ID": r.id,
            "DEKORAVIMO TIPAS": r.decor,
            "KIEKIS m²": r.area,
            "KAINA EUR be PVM": r.price_per_m2,
            "SUMA EUR su PVM": r.total_sum,
            "Sukurta": getattr(r, "created_at", None),
            "Atsisiųsti": download_html
        })

    df = pd.DataFrame(table_data)

    st.write("")
    

    # ✅ Stulpelių pavadinimai
    header1, header2, header3, header4, header5, header6, header7 = st.columns([1, 3, 2, 2, 2, 3, 3])
    header1.write("ID")
    header2.write("DEKORAVIMO TIPAS")
    header3.write("KIEKIS m²")
    header4.write("KAINA EUR be PVM")
    header5.write("SUMA EUR su PVM")
    header6.write("Sukurta")
    header7.write("Atsisiųsti")
    st.markdown("---")  

    # ✅ Realiai atvaizduojame lentelę su mygtukais
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 2, 2, 3, 3])

        col1.write(row["ID"])
        col2.write(row["DEKORAVIMO TIPAS"])
        col3.write(row["KIEKIS m²"])
        col4.write(row["KAINA EUR be PVM"])
        col5.write(row["SUMA EUR su PVM"])
        col6.write(row["Sukurta"])

        pdf_folder = os.path.join(os.path.dirname(__file__), "..", "pdf")
        full_path = os.path.join(pdf_folder, rows[i].file_path)

        if os.path.exists(full_path):
            with col7:
                with open(full_path, "rb") as f:
                    st.download_button(
                        label="💾",
                        data=f,
                        file_name=rows[i].file_path,
                        mime="application/pdf",
                        key=f"dl_{i}"
                    )
        else:
            col7.write("❌")

        st.markdown("---")

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