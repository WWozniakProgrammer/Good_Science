# Prezentacja projektu znajduje się w filmie poniżej:
  [![Zobacz prezentację na YouTube](https://img.youtube.com/vi/Su2A1SZtQxU/0.jpg)](https://www.youtube.com/watch?v=Su2A1SZtQxU)


## Opis działania stworzonej aplikacji oraz jej funkcjonalności:
# Good Science — projekt hackathonu **IDEAHACK 2024**

Platforma, która **łączy naukowców, firmy i inwestorów**, umożliwiając szybkie wyszukiwanie partnerów o określonych kompetencjach oraz umawianie spotkań bezpośrednio z poziomu aplikacji.

IDEAHACK 2024 postawił przed zespołami zadanie stworzenia systemu do kojarzenia środowisk akademickich z biznesem i kapitałem inwestycyjnym :contentReference[oaicite:0]{index=0}. Good Science spełnia te wymagania, oferując:

* **REST API** (Flask) do rejestracji, logowania, aktualizacji profilu i wyszukiwania partnerów :contentReference[oaicite:2]{index=2}  
* **Moduł ML** wykorzystujący polski BERT do tworzenia embeddingów i obliczania podobieństwa z dodatkowymi wagami dla branży, lokalizacji i budżetu :contentReference[oaicite:4]{index=4}  
* **Bazę SQLite** z prostym wrapperem (CRUD)  
* **Integrację z Gmail i Kalendarzem Google** – wysyłanie zaproszeń mailowych i tworzenie wydarzeń :contentReference[oaicite:6]{index=6}  
* **Generator danych demo** do szybkiego prototypowania :contentReference[oaicite:8]{index=8}  
* **Zestaw testów PyTest** pokrywających kluczowe funkcje ML :contentReference[oaicite:10]{index=10}  

---

## Spis treści
1. [Wymagania](#wymagania)  
2. [Instalacja](#instalacja)  
3. [Uruchamianie API](#uruchamianie-api)  
4. [Przykłady wywołań](#przykłady-wywołań)  
5. [Struktura repozytorium](#struktura-repozytorium)  
6. [Testy](#testy)  
7. [Integracja Google](#integracja-google)  
8. [Roadmapa](#roadmapa)  
9. [Zespół](#zespół)  
10. [Licencja](#licencja)  

---

## Wymagania

* Python ≥ 3.9  
* zależności z `requirements.txt` :contentReference[oaicite:12]{index=12}  
* konto Google Cloud + plik `credentials.json` (dla Gmail / Calendar)  

---

## Instalacja

```bash
git clone https://github.com/WWozniakProgrammer/IDEAHACK_2024_Good_Science.git
cd IDEAHACK_2024_Good_Science

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # instalacja pakietów

# jednorazowe pobranie polskiego BERT‑a (~400 MB)
python model/download_model.py         # :contentReference[oaicite:14]{index=14}
