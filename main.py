import random
import json

# Lista branż, potrzeb i lokalizacji
branże = [
    "AI", "biotechnologia", "zielone technologie",
    "robotyka", "edukacja", "energetyka", "medycyna",
    "gaming", "ochrona środowiska", "kosmos"
]
# Lista lokalizacji
# Lista lokalizacji: Województwa, Polska, Europa, Świat, Kraje Europejskie
lokalizacje = [
    # Województwa w Polsce
    "Dolnośląskie", "Kujawsko-Pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-Mazurskie", "Wielkopolskie", "Zachodniopomorskie",
    # Szerokie lokalizacje
    "Polska", "Europa", "Świat",
    # Kraje europejskie
    "Albania", "Andora", "Austria", "Belgia", "Białoruś", "Bośnia i Hercegowina",
    "Bułgaria", "Chorwacja", "Czarnogóra", "Czechy", "Dania", "Estonia",
    "Finlandia", "Francja", "Grecja", "Hiszpania", "Holandia", "Irlandia",
    "Islandia", "Kosowo", "Liechtenstein", "Litwa", "Luksemburg", "Łotwa",
    "Macedonia Północna", "Malta", "Mołdawia", "Monako", "Niemcy", "Norwegia",
    "Polska", "Portugalia", "Rosja", "Rumunia", "San Marino", "Serbia",
    "Słowacja", "Słowenia", "Szwajcaria", "Szwecja", "Turcja", "Ukraina",
    "Watykan", "Węgry", "Wielka Brytania", "Włochy"
]


# Potrzeby zależne od typu
potrzeby_typ = {
    "Biznes": [
        "finansowanie", "partnerstwo", "mentoring biznesowy",
        "wzrost efektywności", "eksport", "restrukturyzacja",
        "innowacje produktowe", "rozwój zasobów ludzkich",
        "transformacja cyfrowa", "automatyzacja procesów"
    ],
    "Akademia": [
        "granty", "partnerstwo badawcze", "mentoring naukowy",
        "publikacje naukowe", "konferencje", "wymiana doświadczeń",
        "rozwój technologii", "nowe kierunki badań",
        "projekty interdyscyplinarne", "współpraca z przemysłem"
    ],
    "Inwestor": [
        "projekty do inwestycji", "zyski długoterminowe", "ekspansja międzynarodowa",
        "inwestycje w startupy", "projekty technologiczne", "projekty ekologiczne",
        "dywersyfikacja portfela", "analiza rynkowa",
        "projekty w energię odnawialną", "partnerstwa strategiczne"
    ]
}

# Funkcja generująca budżet (co 500)
def generuj_budżet(min_budżet, max_budżet, krok):
    return random.randint(min_budżet // krok, max_budżet // krok) * krok

# Funkcja generująca użytkownika
def generuj_użytkownika(id, typ):
    return {
        "id": id,
        "typ": typ.lower(),
        "branże": random.sample(branże, random.randint(1, 2)),
        "potrzeby": random.choice(potrzeby_typ[typ]),
        "budżet": generuj_budżet(10_000, 1_000_000, 1000),
        "lokalizacja": random.choice(lokalizacje)
    }

# Generowanie danych
dane = [generuj_użytkownika(i, random.choice(["Biznes", "Akademia", "Inwestor"])) for i in range(100)]

# Zapis danych do pliku JSON
with open("użytkownicy.json", "w", encoding="utf-8") as f:
    json.dump(dane, f, ensure_ascii=False, indent=4)

print("Plik użytkownicy.json został zapisany!")
