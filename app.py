from flask import Flask, jsonify, request
from model.functions import validate_user_input, create_user_profile, get_embeddings, calculate_similarity, compare_industries
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)

companies_db = [
    {
        "id": 1,
        "type": "company",
        "industry": "AI",
        "budget": "1M-10M",
        "location": "Warszawa",
        "notes": "Szukam współpracy z akademikami specjalizującymi się w AI."
    },
    {
        "id": 2,
        "type": "company",
        "industry": "AI",
        "budget": "10M-50M",
        "location": "Kraków",
        "notes": "Poszukuję innowacyjnych rozwiązań w AI."
    },
    {
        "id": 3,
        "type": "company",
        "industry": "AI",
        "budget": "500K-1M",
        "location": "Warszawa",
        "notes": "Szukam partnerów do rozwoju projektów AI."
    }
]


academics_db = [
    {
        "id": 1,
        "type": "academic",
        "industry": "AI",
        "budget": "1M-10M",
        "location": "Warszawa",
        "notes": "Specjalizuję się w badaniach nad sztuczną inteligencją."
    },
    {
        "id": 2,
        "type": "academic",
        "industry": "AI",
        "budget": "500K-1M",
        "location": "Kraków",
        "notes": "Poszukuję partnerów do badań w dziedzinie AI."
    }
    # Dodaj innych akademików...
]


investors_db = [
    {
        "id": 1,
        "type": "investor",
        "industry": "AI",
        "budget": "10M-50M",
        "location": "Warszawa",
        "notes": "Inwestuję w start-upy AI."
    },
    {
        "id": 2,
        "type": "investor",
        "industry": "AI",
        "budget": "50M+",
        "location": "Kraków",
        "notes": "Szukam inwestycji w projekty AI o dużym potencjale."
    }
    # Dodaj innych inwestorów...
]

@app.route('/')
def index():
    return "API działa!"

@app.route('/user/profile', methods=['POST'])
def create_profile():
    """
    Endpoint do tworzenia profilu użytkownika na podstawie danych JSON.
    """
    try:
        user_data = request.json 
        # Walidacja danych
        validate_user_input(user_data)

        # Tworzenie profilu
        profile = create_user_profile(user_data)
        
        return jsonify({"profile": profile})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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

@app.route('/user/<user_id>', methods=['GET'])
def get_user_profile_by_id(user_id):
    """
    Endpoint do pobrania profilu użytkownika na podstawie ID.
    Zamiast bazy danych, zwróćmy przykładowe dane. - zmiana na baze danych później
    """
    try:
        example_user_data = {
            "id": user_id,
            "type": "company",
            "industry": "AI",
            "budget": "1M-10M",
            "location": "Warszawa",
            "notes": "Szukam współpracy z akademikami specjalizującymi się w AI."
        }
        
        return jsonify(example_user_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/user/target-similarity', methods=['POST'])
def find_similar_targets():
    """
    Endpoint do obliczania podobieństwa pomiędzy użytkownikiem a wybranym targetem (company, academic, investor).
    Zwraca 5 najbliższych wyników.
    """
    try:
        # Dane użytkownika (np. firma szukająca współpracy)
        user_data = request.json
        target_type = user_data.get("target_type", "company")  # domyślnie 'company' jeśli brak target_type
        
        # Walidacja danych użytkownika
        validate_user_input(user_data)
        
        # Tworzymy profil użytkownika
        user_profile = create_user_profile(user_data)
        
        # Generowanie embeddingu profilu użytkownika
        user_embedding = get_embeddings(user_profile)
        
        similarities = []
        
        # Zależnie od typu targetu, przechodzimy po odpowiednich bazach (company, academic, investor)
        if target_type == 'company':
            target_db = companies_db  # Używamy bazy firm
        elif target_type == 'academic':
            target_db = academics_db  # Baza akademików
        elif target_type == 'investor':
            target_db = investors_db  # Baza inwestorów
        else:
            return jsonify({"error": "Nieprawidłowy typ targetu"}), 400
        
        # Przeszukiwanie bazy targetów (company, academic, investor)
        for target in target_db:
            # Tworzymy profil targetu
            target_profile = create_user_profile(target)
            
            # Generowanie embeddingu dla targetu
            target_embedding = get_embeddings(target_profile)
            
            # Obliczanie podobieństwa kosinusowego
            similarity_score = calculate_similarity(user_embedding, target_embedding)
            
            # Porównanie branż
            industry_similarity = compare_industries(user_data['industry'], target['industry'])
            
            # Finalne podobieństwo uwzględniające zarówno embeddingi, jak i branże
            final_similarity = (similarity_score + industry_similarity) / 2  # Możesz dostosować wagę
            
            # Dodajemy wynik (id targetu i podobieństwo)
            similarities.append({
                "target_id": target['id'],
                "similarity_score": final_similarity
            })
        
        # Sortowanie wyników według podobieństwa malejąco
        similarities = sorted(similarities, key=lambda x: x['similarity_score'], reverse=True)
        
        # Wybieramy 5 najbardziej podobnych targetów
        top_5_similar = similarities[:5]
        
        # Zwracamy 5 targetów z najbliższym podobieństwem
        return jsonify({"top_5_similar_targets": top_5_similar})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)