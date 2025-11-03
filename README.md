Voice2Offer

Voice2Offer – tai dirbtinio intelekto projektas, skirtas automatiškai generuoti PDF komercinius pasiūlymus iš balso žinučių.
Sistema apdoroja naudotojo balso įrašą, atpažįsta informaciją (pvz., dekorą, plotą, kainą), išsaugo duomenis duomenų bazėje ir suformuoja profesionalų PDF pasiūlymą.

Pagrindinė idėja

Projektas kuriamas kaip praktinė dirbtinio intelekto taikymo sistema dekoratyvinio tinkavimo verslui.
Tikslas – sumažinti rankinio darbo kiekį, automatizuoti pasiūlymų rengimą ir pagerinti komunikacijos greitį tarp kliento ir tiekėjo.

Naudojamos technologijos

Balso atpažinimui naudojamas OpenAI Whisper modelis.
Duomenų valdymui – SQLAlchemy ORM, leidžiantis patogiai kurti ir valdyti SQLite duomenų bazę.
Dokumentų generavimui naudojama ReportLab biblioteka, su kuria sistema automatiškai kuria PDF pasiūlymus su logotipu, informacija ir kainų lentele.
Visa sistema sukurta naudojant Python 3.12 programavimo kalbą.

Projekto struktūra

Projekte yra atskiras src aplankas su visais pagrindiniais moduliais:

data aplankas (logotipas, garso failai)

db.py ir models.py failai (duomenų bazės struktūra ir ORM klasės)

main_offer_generator.py (PDF pasiūlymo kūrimas)

main_db_insert_offer.py (duomenų įrašymas į DB)

main_db_read_offer.py (įrašų nuskaitymas)

main_db_test_offer.py (DB testavimas)

whisper_test.py (balso atpažinimo testai)

Pagrindinės funkcijos

• Transkribuoja balso žinutę į tekstą.
• Atpažįsta plotą, dekorą, kainą ir kitus pasiūlymo duomenis.
• Įrašo duomenis į SQLite duomenų bazę.
• Automatiškai sugeneruoja PDF komercinį pasiūlymą su logotipu ir kainų lentele.
• Leidžia peržiūrėti visus įrašus duomenų bazėje.

Testavimas

Projektas testuotas lokaliai per Visual Studio Code terminalą.
Naudotos komandos:

python main_db_test_offer.py – patikrina duomenų bazės lenteles

python main_db_insert_offer.py – prideda testinį įrašą

python main_db_read_offer.py – išveda visus įrašus iš DB

python main_offer_generator.py – sugeneruoja PDF pasiūlymą

Išvestis

Sugeneruotas PDF automatiškai išsaugomas projekto šakniniame kataloge, pavyzdžiui:
komercinis_pasiulymas_2025-11-03_15-59.pdf

Autorius

Kęstutis Jorudas
AI & Interior Design Enthusiast
El. paštas: kestutis.jorudas@gmail.com 


Licencija

Projektas skirtas edukaciniams ir moksliniams tikslams (diplominis darbas).
Visos teisės saugomos © 2025 Kęstutis Jorudas.
