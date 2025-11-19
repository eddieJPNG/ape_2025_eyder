
import os
import json

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_PATH, exist_ok=True)


def save_json(filename, data):
    """Salva 'data' (objeto Python) em JSON dentro de DATA_PATH."""
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json(filename):
    """Lê um JSON dentro de DATA_PATH. Retorna None se não existir."""
    file_path = os.path.join(DATA_PATH, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_text(filename, text):
    file_path = os.path.join(DATA_PATH, filename)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
