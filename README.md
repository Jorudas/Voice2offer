Voice2Offer

Voice2Offer – dirbtinio intelekto sistema, skirta automatiškai generuoti PDF komercinius pasiūlymus iš balso įrašų.
Sistema apdoroja naudotojo balsą, atpažįsta esminę informaciją, išsaugo ją duomenų bazėje ir automatiškai sukuria profesionalų PDF pasiūlymą.



Pagrindinė idėja

Projektas sukurtas kaip realaus verslo automatizavimo sprendimas dekoratyvinio tinkavimo rinkai.
Sistema sumažina rankinio darbo kiekį, pagreitina pasiūlymų rengimą ir palengvina komunikaciją tarp kliento ir tiekėjo.
Naudotojui užtenka įrašyti balso žinutę – visa kita padaroma automatiškai.



Naudojamos technologijos

Paskirtis	Technologija
Balso atpažinimas	OpenAI Whisper (speech-to-text)
Teksto analizė ir duomenų išgavimas	GPT-5
DB valdymas	SQLAlchemy ORM + SQLite
PDF generavimas	ReportLab
Vartotojo sąsaja	Streamlit
Programavimo kalba	Python 3.12



Sistemos veikimo principas

Naudotojas įkelia garso įrašą arba įrašo balsu.
Whisper modelis transkribuoja kalbą į tekstą.
GPT-5 iš teksto išgauna reikiamus duomenis (plotas, dekoras, vieta).
Duomenys automatiškai įrašomi į SQLite DB.
Sugeneruojamas PDF komercinis pasiūlymas.
Vartotojas gali atsisiųsti PDF arba peržiūrėti istoriją sistemoje.
Visa logika vyksta vienu paspaudimu.




Projekto struktūra

src/
 ├─ app.py                 # Streamlit vartotojo sąsaja
 ├─ voice_pipeline.py      # Whisper → GPT-5 → JSON → DB procesas
 ├─ offer_generator.py     # PDF pasiūlymo generavimas (ReportLab)
 ├─ db.py                  # DB inicijavimas, ryšys, Session
 ├─ models.py              # SQLAlchemy ORM lentelės
 ├─ data_extractor.py      # Teksto analizė per GPT-5
 ├─ plots.py               # ML grafikų generavimas
 ├─ ml_model.py            # Paprastas ML modelis
 ├─ nn_train.py            # Neuroninio tinklo treniravimas
 └─ whisper_test.py        # Whisper testai



Pagrindinės funkcijos

✔ Transkribuoja balso žinutę į tekstą
✔ Automatiškai išgauna plotą, dekorą, lokaciją
✔ Įrašo duomenis į SQLite DB
✔ Sugeneruoja profesionalų PDF (logotipas, lentelės, kaina)
✔ Leidžia atsisiųsti pasiūlymą
✔ Parodo visų pasiūlymų istoriją Streamlit lange




Lokalus testavimas

python main_db_init.py       # sukuria DB
python main_db_insert_offer.py
python main_db_read_offer.py
python main_offer_generator.py



Autorius
Kęstutis Jorudas
