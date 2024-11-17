import pytest
from model.functions import validate_user_input, create_user_profile, get_embeddings, calculate_similarity, get_user_profile

# Przykładowe dane
user_data = {
    'type': 'company',
    'industry': 'AI',
    'budget': '1M-10M',
    'location': 'Warszawa',
    'notes': 'Szukam współpracy z akademikami specjalizującymi się w AI.'
}

user_data_1 = {
    'type': 'company',
    'industry': 'AI',
    'budget': '1M-10M',
    'location': 'Warszawa',
    'notes': 'Szukam współpracy z akademikami specjalizującymi się w AI.'
}

user_data_2 = {
    'type': 'company',
    'industry': 'AI',
    'budget': '10M-50M',
    'location': 'Kraków',
    'notes': 'Poszukuję nowych inwestycji w AI.'
}

def test_validate_user_input():
    """Testowanie walidacji danych użytkownika."""
    # Test poprawnych danych
    assert validate_user_input(user_data) is True

    # Test błędnych danych
    invalid_user_data = user_data.copy()
    invalid_user_data['type'] = 'unknown'  # Niepoprawny typ
    with pytest.raises(ValueError):
        validate_user_input(invalid_user_data)

def test_create_user_profile():
    """Testowanie tworzenia profilu użytkownika."""
    profile = create_user_profile(user_data)
    assert "Typ użytkownika: Firma" in profile
    assert "Branża: AI" in profile
    assert "Budżet: 1M-10M" in profile

def test_calculate_similarity():
    """Testowanie obliczania podobieństwa."""
    embedding_1 = get_embeddings(create_user_profile(user_data_1))
    embedding_2 = get_embeddings(create_user_profile(user_data_2))
    similarity_score = calculate_similarity(embedding_1, embedding_2)
    assert 0 <= similarity_score <= 1  # Wynik podobieństwa w granicach 0 i 1

def test_get_user_profile():
    """Testowanie funkcji get_user_profile."""
    user_profile_json = get_user_profile(user_data)
    assert 'profile_text' in user_profile_json
    assert 'user_data' in user_profile_json
    assert user_profile_json['profile_text'] == 'Typ użytkownika: Firma. Branża: AI. Budżet: 1M-10M. Lokalizacja: Warszawa. Uwagi: Szukam współpracy z akademikami specjalizującymi się w AI..'
