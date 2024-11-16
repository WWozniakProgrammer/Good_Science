from transformers import AutoTokenizer, AutoModel

def download_and_save_model():
    """
    Pobiera model i tokenizer, a następnie zapisuje je lokalnie.
    Funkcja powinna być wywoływana raz, np. przy uruchamianiu aplikacji.
    """
    local_model_dir = './models/bert-base-polish-cased-v1'

    # Pobierz model i tokenizer
    tokenizer = AutoTokenizer.from_pretrained("dkleczek/bert-base-polish-cased-v1")
    model = AutoModel.from_pretrained("dkleczek/bert-base-polish-cased-v1")

    # Zapisz model i tokenizer lokalnie, jeśli nie zostały zapisane
    tokenizer.save_pretrained(local_model_dir)
    model.save_pretrained(local_model_dir)

    print("Model i tokenizer zostały pobrane i zapisane lokalnie.")

download_and_save_model()