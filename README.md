Popis
Projekt implementuje REST API pro evidenci pojistek a pojistných událostí.  
API umožňuje správu klientů, pojistných smluv, událostí a připojených dokumentů.  
Součástí je Swagger dokumentace dostupná na endpointu `/api`.

API je navrženo dle specifikace OpenAPI 3.0 a používá framework Flask (Python).

Požadavky (requirements)

Software
- Python 3.10 nebo novější  
- pip (součást instalace Pythonu)  
- Textový editor nebo IDE (např. Visual Studio Code nebo Visual Studio)

Python knihovny
Instalace požadovaných balíčků:
pip install flask flask-cors



Postup spuštění:

1.Stáhni projekt
Buď naklonuj repozitář:
git clone https://github.com/KubaDavidek/API---Pojisteni.git
Nebo si stáhni ZIP z GitHubu a rozbal ho do libovolné složky.

2. Otevři složku projektu
Např. v příkazové řádce nebo Visual Studiu Code:
cd API---Pojisteni

3.Nainstaluj požadované knihovny
pip install flask flask-cors

4.Spusť aplikaci
do terminálu napiš: python app.py

5.Otevři webový prohlížeč a přejdi na adresu
http://localhost:8080/api


Zobrazí se Swagger UI s dokumentací a interaktivním rozhraním, kde si můžeš API vyzkoušet pomocí tlačítka Try it out.
