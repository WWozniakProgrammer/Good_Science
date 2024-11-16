from transformers import AutoTokenizer, AutoModel

# Ścieżka, w której zapiszesz model i tokenizer
local_model_dir = './models/bert-base-polish-cased-v1'

# Pobierz model i tokenizer i zapisz je lokalnie (robimy to tylko raz)
tokenizer = AutoTokenizer.from_pretrained("dkleczek/bert-base-polish-cased-v1")
model = AutoModel.from_pretrained("dkleczek/bert-base-polish-cased-v1")

tokenizer.save_pretrained(local_model_dir)
model.save_pretrained(local_model_dir)