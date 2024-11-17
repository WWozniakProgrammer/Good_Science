from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
from flask import Flask, jsonify, request
from database.data_base import DatabaseManager

# Absolutna ścieżka do folderu
local_model_dir = os.path.join(os.path.dirname(__file__), 'models', 'bert-base-polish-cased-v1')

tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
model = AutoModel.from_pretrained(local_model_dir)

# Funkcja generująca embeddingi
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Używamy średniej z ostatniej warstwy
    return embeddings



def map_target_data(target):
    return {
        "type": target.get("typ", ""),  # Mapowanie `typ` na `type`
        "industry": target.get("branze", []),
        "budget": target.get("budzet", "N/A"),
        "location": target.get("lokalizacja", ""),
        "notes": target.get("uwagi", "")
    }

# Walidacja danych wejściowych
def validate_user_input(user):
    required_fields = ['type', 'industry', 'budget', 'location']
    for field in required_fields:
        if field not in user:
            raise ValueError(f"Brak wymaganego pola: {field}")
        if field == 'industry' and not isinstance(user['industry'], list):
            raise ValueError("Pole 'industry' powinno być listą.")
    
    if user['type'] not in ['company', 'academic', 'investor']:
        raise ValueError("Nieprawidłowy typ użytkownika.")
    return True

def create_user_profile(user):
    try:
        # Walidacja danych użytkownika
        validate_user_input(user)
    except ValueError as e:
        raise ValueError(f"Błąd walidacji: {e}")

    # Normalizacja 'industry' (spłaszczanie i konwersja do listy stringów)
    industry = []
    for item in user['industry']:
        if isinstance(item, list):  # Spłaszczamy listę
            industry.extend(item)
        elif isinstance(item, str):  # Jeśli to string, dodajemy bez zmian
            industry.append(item)
        else:
            raise ValueError(f"Nieobsługiwany typ danych w 'industry': {type(item)}")
    
    profile_text = (
        f"Typ użytkownika: {user['type'].capitalize()}. "
        f"Branża: {', '.join(industry)}. "
        f"Budżet: {user['budget']}. "
        f"Lokalizacja: {user['location']}. "
        f"Uwagi: {user.get('notes', '')}."
    )
    return profile_text

# Funkcja obliczająca podobieństwo kosinusowe
def calculate_similarity(embedding1, embedding2):
    similarity = cosine_similarity(embedding1.numpy(), embedding2.numpy())[0][0]
    
    return float(similarity)

# Funkcja porównująca branże
def compare_industries(industry_user, industry_target):
    # Spłaszczanie listy, jeśli zawiera listy w środku
    if isinstance(industry_user[0], list):
        industry_user = [item for sublist in industry_user for item in sublist]
    if isinstance(industry_target[0], list):
        industry_target = [item for sublist in industry_target for item in sublist]

    # Zamień wszystkie branże na małe litery, aby porównanie było niezależne od wielkości liter
    industry_user = set([industry.lower() for industry in industry_user])
    industry_target = set([industry.lower() for industry in industry_target])
    
    # Liczymy wspólne branże
    common_industries = industry_user.intersection(industry_target)
    
    # Obliczamy podobieństwo jako stosunek wspólnych branż do wszystkich branż w obu użytkownikach
    total_industries = industry_user.union(industry_target)
    
    if not total_industries:
        return 0  # Jeśli nie ma żadnych branż, podobieństwo to 0
    
    similarity = len(common_industries) / len(total_industries)
    return similarity

# Funkcja porównująca lokalizacje
def compare_location(location_user, location_target):
    location_similarity = 1.0 if location_user.lower() == location_target.lower() else 0.0
    print(f"Location similarity: {location_similarity}")
    return location_similarity

# Funkcja porównująca budżet
def compare_budget(budget_user, budget_target):
    budget_similarity = 1.0 if budget_user == budget_target else 0.0
    print(f"Budget similarity: {budget_similarity}")
    return budget_similarity

# Funkcja obliczająca podobieństwo z wagami
def calculate_weighted_similarity(user_embedding, target_embedding, user_data, target):
    similarity_score = calculate_similarity(user_embedding, target_embedding)
    
    industry_similarity = compare_industries(user_data.get('industry', []), target.get('industry', []))
    location_similarity = compare_location(user_data.get('location', ''), target.get('location', ''))
    budget_similarity = compare_budget(user_data.get('budget', ''), target.get('budget', ''))

    weighted_similarity = (0.5 * similarity_score + 0.2 * industry_similarity 
                           + 0.2 * location_similarity + 0.1 * budget_similarity)
    
    print(f"Weighted similarity: {weighted_similarity}")
    return weighted_similarity