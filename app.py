from flask import Flask, jsonify, request
from model.functions import validate_user_input, map_target_data, create_user_profile, get_embeddings, calculate_similarity, compare_industries, calculate_weighted_similarity
from transformers import AutoTokenizer, AutoModel
#from database.data_base import pobierz_obiekty_po_typie
from database.data_base import DatabaseManager
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

db = DatabaseManager('moja_baza.db')

@app.route('/')
def index():
    return "API działa!"

@app.route('/user/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    try:
        # Debugowanie: sprawdź, co zwraca baza danych
        user_data_json = db.pobierz_uzytkownika_po_id(user_id)  
        print(f"Debug: Otrzymane dane: {user_data_json}")
        
        if user_data_json:
            user_data = json.loads(user_data_json)
            return jsonify(user_data["data"])
        else:
            return jsonify({"error": "Użytkownik nie znaleziony"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/user/register', methods=['POST'])
def register_user():
    """
    Rejestruje nowego użytkownika w bazie danych.
    """
    try:
        user_data = request.json
        required_fields = ["nazwa", "email", "haslo"]
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Brak pola: {field}"}), 400

        # Dodajemy użytkownika do bazy
        token = "TOKEN_" + user_data["email"]  # Generujemy prosty token, można zastąpić JWT
        user_data_json = json.dumps({
            "typ": "",
            "nazwa": user_data["nazwa"],
            "email": user_data["email"],
            "haslo": user_data["haslo"],
            "branze": [],
            "budzet": "",
            "lokalizacja": "",
            "uwagi": "",
        })
        response = db.dodaj_uzytkownika(user_data_json, token)
        response_data = json.loads(response)

        if response_data["status"] == "success":
            # Pobierz ID nowo dodanego użytkownika
            added_user = db.pobierz_uzytkownika_po_nazwie(user_data["nazwa"])
            user_id = json.loads(added_user)["data"]["id"]
            return jsonify({"id": user_id, "message": "Użytkownik został zarejestrowany pomyślnie."})
        else:
            return jsonify({"error": response_data["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/user/login', methods=['POST'])
def login_user():
    """
    Loguje użytkownika na podstawie emaila i hasła.
    """
    try:
        user_data = request.json
        required_fields = ["email", "haslo"]
        
        # Sprawdzamy, czy wszystkie wymagane pola są obecne
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Brak pola: {field}"}), 400
        
        # Logowanie dla debugowania - co otrzymujemy w żądaniu
        print(f"Debug: Otrzymane dane logowania: {user_data}")

        # Zmieniamy podejście do wywołania sprawdz_uzytkownika()
        email = user_data.get('email').strip().lower()  # Usuwamy zbędne białe znaki i zmieniamy na małe litery
        haslo = user_data.get('haslo').strip()

        # Sprawdzamy dane logowania - wywołanie funkcji sprawdz_uzytkownika z dwoma argumentami
        is_valid_user = db.sprawdz_uzytkownika(email, haslo)  # Wywołanie z dwoma argumentami: email i haslo
        if is_valid_user:
            print(f"Debug: Dane logowania prawidłowe dla użytkownika: {email}")
            
            # Pobieramy dane użytkownika z bazy na podstawie emaila
            user_record = db.pobierz_uzytkownika_po_emailu(email)  # Funkcja zwraca dane użytkownika na podstawie emaila
            print(f"Debug: Otrzymany rekord użytkownika: {user_record}")
            
            # Sprawdzamy, czy odpowiedź zawiera status success i dane użytkownika
            user_record_json = json.loads(user_record)
            if user_record_json.get("status") == "error":
                return jsonify({"error": "Nie znaleziono użytkownika w bazie."}), 404
            
            # Parsowanie JSON odpowiedzi z bazy danych
            if "data" not in user_record_json:
                return jsonify({"error": "Błąd w odpowiedzi bazy danych."}), 500

            user_data_json = user_record_json["data"]
            user_id = user_data_json["id"]  # Wyciągamy id użytkownika

            # Zwracamy sukces i dane użytkownika (w tym id)
            return jsonify({"id": user_id, "message": "Zalogowano pomyślnie."})
        
        else:
            print("Debug: Nieprawidłowe dane logowania")
            return jsonify({"error": "Nieprawidłowe dane logowania."}), 401

    except Exception as e:
        # Logowanie błędu
        print(f"Error during login: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/user/update/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    """
    Aktualizuje dane profilu użytkownika.
    """
    try:
        user_data = request.json
        required_fields = ["type", "industry", "budget", "location", "notes"]
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Brak pola: {field}"}), 400

        # Aktualizujemy dane użytkownika
        user_data_json = json.dumps({
            "typ": user_data["type"],
            "branze": [user_data["industry"]],
            "budzet": user_data["budget"],
            "lokalizacja": user_data["location"],
            "uwagi": user_data["notes"],
        })
        response = db.aktualizuj_uzytkownika(str(user_id), user_data_json)
        response_data = json.loads(response)

        if response_data["status"] == "success":
            return jsonify({"message": response_data["message"]})
        else:
            return jsonify({"error": response_data["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/user/similarity', methods=['POST'])
def calculate_user_similarity():
    """
    Endpoint do obliczania podobieństwa między dwoma użytkownikami.
    """
    try:
        user_data_1 = request.json.get('user_1')
        user_data_2 = request.json.get('user_2')
        
        # Generowanie embeddingów
        embedding_1 = get_embeddings(create_user_profile(user_data_1))
        embedding_2 = get_embeddings(create_user_profile(user_data_2))

        # Obliczanie podobieństwa
        similarity_score = calculate_similarity(embedding_1, embedding_2)

        return jsonify({"similarity_score": similarity_score})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_profile_by_id(user_id):
    """
    Endpoint do pobrania profilu użytkownika na podstawie ID z bazy danych.
    """
    try:
        # Pobranie danych użytkownika z bazy danych
        user_data_json = db.pobierz_uzytkownika_po_id(user_id)
        user_data = json.loads(user_data_json)

        # Sprawdzenie, czy użytkownik został znaleziony
        if user_data.get("status") == "success":
            return jsonify(user_data["data"])  # Zwracamy dane użytkownika w formacie JSON
        else:
            return jsonify({"error": user_data.get("message", "Nieznany błąd")}), 404

    except Exception as e:
        # Obsługa błędów i logowanie
        print(f"Error in get_user_profile_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/user/target-similarity', methods=['POST'])
def find_similar_targets():
    try:
        # Pobranie ID użytkownika z żądania JSON
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({"error": "Brak ID użytkownika"}), 400
        
        # Pobranie tylko wymaganych danych użytkownika z bazy na podstawie ID
        user_data_json = db.pobierz_uzytkownika_po_id(user_id)
        user_data = json.loads(user_data_json)
        
        # Sprawdzenie, czy użytkownik został znaleziony
        if user_data.get("status") != "success":
            return jsonify({"error": "Nie znaleziono użytkownika"}), 404
        
        # Pobranie rzeczywistych danych użytkownika
        user_data = user_data["data"]

        # Mapowanie danych z polskich nazw na angielskie
        mapped_user_data = {
            "type": user_data.get("typ", ""),
            "industry": user_data.get("branże", []),
            "budget": user_data.get("budżet", "N/A"),
            "location": user_data.get("lokalizacja", ""),
            "target_types": user_data.get("target_types", ["company", "academic", "investor"])  # Domyślne wartości
        }

        # Walidacja, czy pola są obecne
        required_fields = ['type', 'industry', 'budget', 'location', 'target_types']
        for field in required_fields:
            if field not in mapped_user_data:
                return jsonify({"error": f"Brak wymaganego pola: {field}"}), 400

        # Tworzenie profilu użytkownika i embeddingu
        user_profile = create_user_profile(mapped_user_data)
        user_embedding = get_embeddings(user_profile)

        # Ustawienie domyślnych typów celów
        target_types = mapped_user_data["target_types"]

        result = {}
        for target_type in target_types:
            # Pobranie i mapowanie danych celów
            target_data = db.pobierz_obiekty_po_typie(target_type)
            try:
                target_users = json.loads(target_data)
            except json.JSONDecodeError:
                raise ValueError(f"Niepoprawne dane JSON dla {target_type}: {target_data}")

            similarities = []
            for target in target_users:
                # Mapowanie danych celu
                mapped_target = map_target_data(target)

                # Tworzenie profilu celu i embeddingu
                target_profile = create_user_profile(mapped_target)
                target_embedding = get_embeddings(target_profile)

                # Obliczanie podobieństwa z uwzględnieniem wag
                weighted_similarity = calculate_weighted_similarity(
                    user_embedding, target_embedding, mapped_user_data, mapped_target
                )

                similarities.append({
                    "id": target.get('id'),
                    "similarity": weighted_similarity
                })

            # Sortowanie wyników i zwrócenie najlepszych
            top_5_similar = sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:5]
            result[target_type] = top_5_similar

        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500








if __name__ == '__main__':
    app.run(debug=True)