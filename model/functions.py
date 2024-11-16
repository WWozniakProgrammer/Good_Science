from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity


# Ścieżka do lokalnego folderu z modelem
local_model_dir = './models/bert-base-polish-cased-v1'

# Załaduj model i tokenizer z lokalnej lokalizacji
tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
model = AutoModel.from_pretrained(local_model_dir)

# Funkcja generująca embeddingi
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Używamy średniej z ostatniej warstwy
    return embeddings


# Funkcja tworząca profil użytkownika w zależności od jego typu
def create_user_profile(user):
    """
    Tworzy tekstowy profil użytkownika na podstawie danych z ankiety.
    """
    if user['type'] == 'company':
        # Profil dla firmy
        profile_text = f"Typ użytkownika: Firma. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    
    elif user['type'] == 'academic':
        # Profil dla akademika
        profile_text = f"Typ użytkownika: Akademik. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    
    elif user['type'] == 'investor':
        # Profil dla inwestora
        profile_text = f"Typ użytkownika: Inwestor. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    
    return profile_text

def validate_user_input(user):
    """
    Sprawdza, czy w danych użytkownika znajdują się wszystkie wymagane pola.
    """
    required_fields = ['type', 'industry', 'budget', 'location']
    
    # Sprawdzanie obecności wymaganych pól
    for field in required_fields:
        if field not in user:
            raise ValueError(f"Brak wymaganego pola: {field}")
    
    # Sprawdzanie poprawności typu
    if user['type'] not in ['company', 'academic', 'investor']:
        raise ValueError("Nieprawidłowy typ użytkownika. Możliwe wartości: 'company', 'academic', 'investor'.")
    
    return True

# Funkcja obliczająca podobieństwo kosinusowe między dwoma embeddingami
def calculate_similarity(embedding1, embedding2):
    """
    Oblicza podobieństwo kosinusowe między dwoma embeddingami.
    """
    return cosine_similarity(embedding1.numpy(), embedding2.numpy())[0][0]



def create_profile_for_type(user_type, user):
    """
    Funkcja tworzy profil na podstawie typu użytkownika.
    """
    profile_text = f"Typ użytkownika: {user_type.capitalize()}. "
    profile_text += f"Branża: {user['industry']}. "
    profile_text += f"Budżet: {user['budget']}. "
    profile_text += f"Lokalizacja: {user['location']}. "
    profile_text += f"Uwagi: {user.get('notes', '')}."
    return profile_text

def create_user_profile(user):
    """
    Tworzy tekstowy profil użytkownika na podstawie danych z ankiety.
    """
    try:
        validate_user_input(user)  # Sprawdź, czy dane są poprawne
    except ValueError as e:
        return f"Błąd walidacji: {e}"  # Zwróć komunikat o błędzie walidacji
    
    # Debugowanie: Wyświetl dane wejściowe przed generowaniem profilu
    print(f"Tworzenie profilu dla: {user}")

    user_type = user['type']
    
    # Generowanie profilu w zależności od typu użytkownika
    if user_type == 'company':
        profile_text = f"Typ użytkownika: Firma. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    elif user_type == 'academic':
        profile_text = f"Typ użytkownika: Akademik. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    elif user_type == 'investor':
        profile_text = f"Typ użytkownika: Inwestor. "
        profile_text += f"Branża: {user['industry']}. "
        profile_text += f"Budżet: {user['budget']}. "
        profile_text += f"Lokalizacja: {user['location']}. "
        profile_text += f"Uwagi: {user.get('notes', '')}."
    else:
        return "Nieprawidłowy typ użytkownika."
    
    return profile_text


def get_user_profile(user):
    """
    Zwraca profil użytkownika w formacie JSON, aby frontend mógł go łatwo wykorzystać.
    """
    try:
        validate_user_input(user)
    except ValueError as e:
        return {"error": str(e)}  # Zwróć błąd walidacji w formacie JSON
    
    user_type = user['type']
    profile_text = create_profile_for_type(user_type, user)
    
    return {
        "profile_text": profile_text,
        "user_data": user  # Możesz zwrócić również pełne dane użytkownika
    }

