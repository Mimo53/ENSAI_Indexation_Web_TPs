import os
from loader import load_json
from ranking import compute_bm25
from search_engine import filter_any_token, process_query

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data")
INDEXES_PATH = os.path.join(DATA_PATH, "indexes")

# --- Load indexes ---
indexes = {
    "title": load_json(os.path.join(INDEXES_PATH, "title_index.json")),
    "description": load_json(os.path.join(INDEXES_PATH, "description_index.json")),
    "brand": load_json(os.path.join(INDEXES_PATH, "brand_index.json")),
    "origin": load_json(os.path.join(INDEXES_PATH, "origin_index.json")),
    "reviews": load_json(os.path.join(INDEXES_PATH, "reviews_index.json"))
}

# --- Load synonyms ---
synonyms = load_json(os.path.join(DATA_PATH, "origin_synonyms.json"))

# --- Example queries for testing ---
test_queries = [
    "chocolate from switzerland",
    "dark chocolate usa",
    "chocodelight cherry",
    "milk chocolate orange"
]

# --- Weight ranges (0.1 à 3.0 par exemple) ---
title_weights = [i / 10 for i in range(5, 31)]        # 0.5 → 3.0
desc_weights = [i / 10 for i in range(1, 21)]         # 0.1 → 2.0
mean_mark_weights = [i / 10 for i in range(0, 21)]    # 0 → 2.0
total_reviews_weights = [i / 10 for i in range(0, 11)]# 0 → 1.0

best_score_sum = -1
best_weights = None
total_combinations = len(title_weights) * len(desc_weights) * len(mean_mark_weights) * len(total_reviews_weights)
current_combination = 0

# --- Brute force search with realistic scores ---
for tw in title_weights:
    for dw in desc_weights:
        for mw in mean_mark_weights:
            for rw in total_reviews_weights:
                current_combination += 1

                # Affichage de l'avancement
                if current_combination % 50 == 0:
                    print(f"Testing combination {current_combination}/{total_combinations}...")

                # Fonction de ranking interne avec poids actuels
                def rank_documents_weighted(docs, tokens, title_index, description_index, reviews_index):
                    from collections import defaultdict
                    scores = defaultdict(float)
                    avgdl = 50
                    for doc in docs:
                        doc_len = 50
                        for token in tokens:
                            scores[doc] += tw * compute_bm25(token, doc, title_index, avgdl, doc_len)
                            scores[doc] += dw * compute_bm25(token, doc, description_index, avgdl, doc_len)
                        reviews = reviews_index.get(doc, {})
                        scores[doc] += reviews.get("mean_mark", 0) * mw
                        scores[doc] += reviews.get("total_reviews", 0) * rw
                    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

                # Calcul du score total pour ce set de poids
                score_sum = 0
                for q in test_queries:
                    tokens = process_query(q, synonyms)
                    text_docs = filter_any_token(tokens, [indexes["title"], indexes["description"]])
                    feature_docs = filter_any_token(tokens, [indexes["brand"], indexes["origin"]])
                    filtered_docs = text_docs & feature_docs if feature_docs else text_docs

                    ranked_docs = rank_documents_weighted(filtered_docs, tokens, indexes["title"], indexes["description"], indexes["reviews"])
                    # On somme les 10 premiers résultats pour ce test (top-k)
                    score_sum += sum([score for _, score in ranked_docs[:10]])

                # Mise à jour du meilleur score
                if score_sum > best_score_sum:
                    best_score_sum = score_sum
                    best_weights = (tw, dw, mw, rw)

# --- Résultats finaux ---
print("\n=== Best weights found ===")
print(f"Title weight: {best_weights[0]}")
print(f"Description weight: {best_weights[1]}")
print(f"Mean mark weight: {best_weights[2]}")
print(f"Total reviews weight: {best_weights[3]}")
print(f"Total top-10 score sum across queries: {best_score_sum}")
