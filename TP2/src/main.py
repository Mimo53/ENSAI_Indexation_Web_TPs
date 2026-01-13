import os

from loader import load_jsonl_file
from inverted_index import build_inverted_index
from positional_index import build_positional_index
from feature_index import build_feature_index  # index brand et origin
from reviews_index import build_reviews_index
from storage import save_index_to_json

DATA_PATH = "../data/products.jsonl"
OUTPUT_DIR = "indexes"


def main():
    # Crée le dossier output s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Charge les documents JSONL
    documents = load_jsonl_file(DATA_PATH)

    # --- Index positionnels ---
    title_pos_index = build_positional_index(documents, "title")
    description_pos_index = build_positional_index(documents, "description")

    # --- Index inversés (texte) ---
    title_index = build_inverted_index(documents, "title")
    description_index = build_inverted_index(documents, "description")

    # --- Index features (brand et origin) ---
    feature_index = build_feature_index(documents)

    # --- Index reviews ---
    reviews_index = build_reviews_index(documents)

    # --- Sauvegarde dans JSON ---
    save_index_to_json(title_pos_index, f"{OUTPUT_DIR}/title_positional_index.json")
    save_index_to_json(description_pos_index, f"{OUTPUT_DIR}/description_positional_index.json")
    save_index_to_json(title_index, f"{OUTPUT_DIR}/title_index.json")
    save_index_to_json(description_index, f"{OUTPUT_DIR}/description_index.json")
    
    # --- Index features (séparés) ---

    save_index_to_json(feature_index["brand"], f"{OUTPUT_DIR}/brand_index.json")
    save_index_to_json(feature_index["origin"], f"{OUTPUT_DIR}/origin_index.json")
    save_index_to_json(feature_index["material"], f"{OUTPUT_DIR}/material_index.json")
    save_index_to_json(feature_index["date"], f"{OUTPUT_DIR}/date_index.json")

    # Sauvegarde feature_index complet si besoin
    save_index_to_json(feature_index, f"{OUTPUT_DIR}/feature_index.json")
    
    # Sauvegarde reviews
    save_index_to_json(reviews_index, f"{OUTPUT_DIR}/reviews_index.json")

    print("Indexation terminée. Fichiers sauvegardés dans", OUTPUT_DIR)


if __name__ == "__main__":
    main()
