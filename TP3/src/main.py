import sys
import os
import json
from loader import load_json
from search_engine import search

# Base directory = dossier src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dossier data/
DATA_PATH = os.path.join(BASE_DIR, "..", "data")
INDEXES_PATH = os.path.join(DATA_PATH, "indexes")
WEIGHTS_PATH = os.path.join(DATA_PATH, "optimized_weights.json")


def display_results(results, top_n=50):
    """Affiche les résultats de manière lisible"""
    print(f"\nQuery: {results['query']}")
    print(f"Total documents: {results['total_documents']}")
    print(f"Filtered documents: {results['filtered_documents']}")
    print("Top results:")
    for r in results["results"][:top_n]:
        print(f"- {r['url']} (score: {r['score']})")


def load_weights():
    """Charge les poids optimisés depuis le JSON si disponible"""
    default_weights = {
        "title": 3.0,
        "description": 2.0,
        "mean_mark": 2.0,
        "total_reviews": 1.0
    }
    if os.path.exists(WEIGHTS_PATH):
        with open(WEIGHTS_PATH, "r") as f:
            try:
                weights = json.load(f)
                # Merge avec les valeurs par défaut si certains champs manquent
                default_weights.update(weights)
                print(f"Loaded optimized weights: {default_weights}")
            except Exception as e:
                print(f"Error loading optimized weights: {e}")
                print("Using default weights.")
    else:
        print("No optimized weights found, using default weights.")
    return default_weights


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'search query'")
        sys.exit(1)

    query = sys.argv[1]

    # --- Load optimized weights ---
    weights = load_weights()
    # Les poids sont maintenant utilisés automatiquement dans ranking.py

    # --- Load required indexes ---
    indexes = {
        "title": load_json(os.path.join(INDEXES_PATH, "title_index.json")),
        "description": load_json(os.path.join(INDEXES_PATH, "description_index.json")),
        "brand": load_json(os.path.join(INDEXES_PATH, "brand_index.json")),
        "origin": load_json(os.path.join(INDEXES_PATH, "origin_index.json")),
        "reviews": load_json(os.path.join(INDEXES_PATH, "reviews_index.json"))
    }

    # --- Load synonyms ---
    synonyms = load_json(os.path.join(DATA_PATH, "origin_synonyms.json"))

    # --- Load optional positional indexes ---
    positional_indexes = {}
    title_pos_path = os.path.join(INDEXES_PATH, "title_positional_index.json")
    desc_pos_path = os.path.join(INDEXES_PATH, "description_positional_index.json")

    if os.path.exists(title_pos_path) and os.path.exists(desc_pos_path):
        positional_indexes["title_positional"] = load_json(title_pos_path)
        positional_indexes["description_positional"] = load_json(desc_pos_path)
    else:
        positional_indexes = None
        print(
            "Note: positional indexes not found. "
            "You can add them later to improve ranking."
        )

    # --- Run search for the input query ---
    results = search(query, indexes, synonyms, positional_indexes)
    print("=== Single Query Results ===")
    display_results(results)

    # --- Example batch of queries for testing & optimization ---
    # Commented out for now
    # example_queries = [
    #     "chocolate from switzerland",
    #     "dark chocolate usa",
    #     "chocodelight cherry",
    #     "milk chocolate orange",
    #     "chocolate cherry switzerland",
    #     "milk chocolate usa",
    #     "dark chocolate cherry",
    #     "chocolate orange cherry",
    #     "white chocolate"
    # ]
    #
    # print("\n=== Batch Queries ===")
    # for q in example_queries:
    #     res = search(q, indexes, synonyms, positional_indexes)
    #     display_results(res)


if __name__ == "__main__":
    main()
