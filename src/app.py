
# src/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer
from offer_generator import generate_offer
from plots import generate_model_plots   # <-- vietoje show_model_plots

DB_PATH = "voice2offer.db"

st.set_page_config(page_title="Voice2Offer - Mini UI", layout="centered")

# ✅ Sukuriame du puslapius
tab1, tab2 = st.tabs(["💼 Pasiūlymų generatorius", "📊 Modelių analizė"])

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
            "Dekoras": r.decor,
            "Plotas_m2": r.area,
            "Kaina_m2": r.price_per_m2,
            "Suma": r.total_sum,
            "Failas": r.file_path,
            "Sukurta": getattr(r, "created_at", None)
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)


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