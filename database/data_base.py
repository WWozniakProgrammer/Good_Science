import sqlite3
import json
from typing import Optional, Union

class DatabaseManager:
    """Klasa do obsługi bazy danych SQLite."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Tworzy tabelę użytkowników w bazie danych."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS uzytkownicy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    typ TEXT NOT NULL,
                    nazwa TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    haslo TEXT NOT NULL,
                    branże TEXT NOT NULL,
                    budżet TEXT NOT NULL,
                    lokalizacja TEXT NOT NULL,
                    uwagi TEXT NOT NULL,
                    token TEXT NOT NULL
                )
            ''')
            conn.commit()

    def dodaj_uzytkownika(self, dane_json: str, token: str) -> str:
        """Dodaje użytkownika do bazy danych."""
        dane = json.loads(dane_json)
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO uzytkownicy (typ, nazwa, email, haslo, branże, budżet, lokalizacja, uwagi, token) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', (
                    dane.get('typ'),
                    dane.get('nazwa'),
                    dane.get('email'),
                    dane.get('haslo'),
                    json.dumps(dane.get('branze', []), ensure_ascii=False),
                    dane.get('budzet'),
                    dane.get('lokalizacja'),
                    dane.get('uwagi'),
                    token
                ))
                conn.commit()
            return json.dumps({"status": "success", "message": f"Użytkownik {dane.get('nazwa')} został dodany."}, ensure_ascii=False)
        except sqlite3.IntegrityError as e:
            return json.dumps({"status": "error", "message": f"Błąd dodawania użytkownika: {str(e)}"}, ensure_ascii=False)


    def pobierz_uzytkownika_po_id(self, user_id: int) -> str:
        """Pobiera użytkownika na podstawie ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM uzytkownicy WHERE id = ?', (user_id,))
            wiersz = cursor.fetchone()

        if wiersz:
            uzytkownik = {
                'id': wiersz[0],
                'typ': wiersz[1],
                'nazwa': wiersz[2],
                'email': wiersz[3],
                'haslo': wiersz[4],
                'branże': json.loads(wiersz[5]),
                'budżet': wiersz[6],
                'lokalizacja': wiersz[7],
                'uwagi': wiersz[8],
                'token': wiersz[9]
            }
            return json.dumps({"status": "success", "data": uzytkownik}, ensure_ascii=False, indent=4)
    
        return json.dumps({"status": "error", "message": "Użytkownik nie znaleziony"}, ensure_ascii=False)
    
    def pobierz_uzytkownika_po_nazwie(self, nazwa: str) -> str:
        """Pobiera użytkownika na podstawie nazwy."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM uzytkownicy WHERE nazwa = ?', (nazwa,))
            wiersz = cursor.fetchone()
        
        if wiersz:
            uzytkownik = {
                'id': wiersz[0],
                'typ': wiersz[1],
                'nazwa': wiersz[2],
                'email': wiersz[3],
                'haslo': wiersz[4],
                'branże': json.loads(wiersz[5]),
                'budżet': wiersz[6],
                'lokalizacja': wiersz[7],
                'uwagi': wiersz[8],
                'token': wiersz[9]
            }
            return json.dumps({"status": "success", "data": uzytkownik}, ensure_ascii=False, indent=4)
        return json.dumps({"status": "error", "message": "Użytkownik nie znaleziony"}, ensure_ascii=False)

    def pobierz_obiekty_po_typie(self, typ: str) -> str:
        """Zwraca wszystkie obiekty o danym typie."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, typ, branże, budżet, lokalizacja, uwagi FROM uzytkownicy WHERE typ = ?', (typ,))
            wyniki = cursor.fetchall()

        if not wyniki:
            return json.dumps({"status": "error", "message": f"Brak obiektów o typie: {typ}"}, ensure_ascii=False)

        obiekty = [
            {
                "id": wiersz[0],
                "typ": wiersz[1],
                "industry": ", ".join(json.loads(wiersz[2])),
                "budget": wiersz[3],
                "location": wiersz[4],
                "notes": wiersz[5]
            }
            for wiersz in wyniki
        ]
        return json.dumps({"status": "success", "data": obiekty}, ensure_ascii=False, indent=4)

    
    def sprawdz_uzytkownika(self, email: str, haslo: str):
        """Sprawdza, czy użytkownik istnieje w bazie na podstawie emaila i hasła."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM uzytkownicy WHERE email = ? AND haslo = ?
                ''', (email, haslo))
                user = cursor.fetchone()
                if user:
                    return True  # Użytkownik istnieje
                else:
                    return False  # Użytkownik nie istnieje
        except sqlite3.Error as e:
            return False  # Obsługuje ewentualne błędy

    def aktualizuj_uzytkownika(self, user_id: int, dane_json: str) -> str:
        """Aktualizuje dane użytkownika na podstawie ID użytkownika."""
        dane = json.loads(dane_json)

        # Pobieramy obecne dane użytkownika
        current_user_data = self.pobierz_uzytkownika_po_id(user_id)
        current_user_data = json.loads(current_user_data)
        
        if current_user_data.get("status") == "error":
            return json.dumps({"status": "error", "message": "Użytkownik nie znaleziony"}, ensure_ascii=False)

        # Sprawdzenie, czy wszystkie wymagane pola są obecne w danych
        typ = dane.get('typ', current_user_data['data']['typ'])  # Zachowaj obecny typ, jeśli nie zmieniono
        email = dane.get('email', current_user_data['data']['email'])  # Nie zmieniaj emailu, jeśli nie dostarczono
        haslo = dane.get('haslo', current_user_data['data']['haslo'])  # Jeśli nie zmieniono, zachowaj poprzednie hasło
        branże = dane.get('branze', current_user_data['data']['branże'])
        budżet = dane.get('budzet', current_user_data['data']['budżet'])
        lokalizacja = dane.get('lokalizacja', current_user_data['data']['lokalizacja'])
        uwagi = dane.get('uwagi', current_user_data['data']['uwagi'])

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Przygotowanie zapytania SQL do aktualizacji (nie zmieniamy emailu i hasła, jeśli nie są dostarczone)
                cursor.execute(''' 
                    UPDATE uzytkownicy
                    SET typ = ?, email = ?, haslo = ?, branże = ?, budżet = ?, lokalizacja = ?, uwagi = ?
                    WHERE id = ?
                ''', (
                    typ,
                    email,  # email nie jest zmieniany w tym przypadku
                    haslo,  # hasło nie jest zmieniane, jeśli nie dostarczono
                    json.dumps(branże, ensure_ascii=False),  # Branże muszą być zapisane jako JSON
                    budżet,
                    lokalizacja,
                    uwagi,
                    user_id  # Używamy ID użytkownika do aktualizacji
                ))
                conn.commit()

            # Sprawdzamy, czy aktualizacja się powiodła
            if cursor.rowcount > 0:
                return json.dumps({"status": "success", "message": f"Użytkownik o ID {user_id} został zaktualizowany."}, ensure_ascii=False)
            else:
                return json.dumps({"status": "error", "message": "Nie znaleziono użytkownika o podanym ID."}, ensure_ascii=False)

        except sqlite3.IntegrityError as e:
            return json.dumps({"status": "error", "message": f"Błąd aktualizacji użytkownika: {str(e)}"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Nieoczekiwany błąd: {str(e)}"}, ensure_ascii=False)

    def pobierz_uzytkownika_po_emailu(self, email: str) -> str:
        """Pobiera użytkownika na podstawie adresu email."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM uzytkownicy WHERE email = ?', (email,))
            wiersz = cursor.fetchone()

        if wiersz:
            uzytkownik = {
                'id': wiersz[0],
                'typ': wiersz[1],
                'nazwa': wiersz[2],
                'email': wiersz[3],
                'haslo': wiersz[4],
                'branże': json.loads(wiersz[5]),
                'budżet': wiersz[6],
                'lokalizacja': wiersz[7],
                'uwagi': wiersz[8],
                'token': wiersz[9]
            }
            return json.dumps({"status": "success", "data": uzytkownik}, ensure_ascii=False, indent=4)
        
        return json.dumps({"status": "error", "message": "Użytkownik nie znaleziony"}, ensure_ascii=False)

    def zamknij_polaczenie(self):
        """Zamyka połączenie z bazą danych."""
        # Dzięki wykorzystaniu `with` w każdej funkcji połączenie zamyka się automatycznie, więc ta metoda jest opcjonalna.
        pass
