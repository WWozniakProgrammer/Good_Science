from flask import Flask, jsonify, request
from model.functions import validate_user_input, create_user_profile, get_embeddings, calculate_similarity
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)