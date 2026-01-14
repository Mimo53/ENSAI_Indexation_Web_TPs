from query_processing import process_query
from filtering import filter_any_token
from ranking import rank_documents
from loader import load_json
import os

def search(query, indexes, synonyms, positional_indexes=None):
    """
    Main search function.
    
    positional_indexes: optional dict with title_positional / description_positional indexes.
    If missing, search will ignore them and print a warning.
    """
    # 1. Traitement de la requête (tokenization + synonymes)
    tokens = process_query(query, synonyms)

    # 2. Filtrage TEXTUEL (titre + description)
    text_docs = filter_any_token(
        tokens,
        [
            indexes["title"],
            indexes["description"]
        ]
    )

    # 3. Filtrage FEATURES (brand + origin)
    feature_docs = filter_any_token(
        tokens,
        [
            indexes["brand"],
            indexes["origin"]
        ]
    )

    # 4. Combinaison intelligente
    if feature_docs:
        filtered_docs = text_docs & feature_docs
    else:
        filtered_docs = text_docs

    # 5. Ranking
    ranked = rank_documents(
        filtered_docs,
        tokens,
        indexes["title"],
        indexes["description"],
        indexes["reviews"]
    )

    if positional_indexes is None:
        print("Note: positional indexes not found. You can add them later to improve ranking.")
    else:
        # Future implementation: use positional_indexes for phrase scoring or proximity
        pass

    return {
        "query": query,
        "total_documents": len(indexes["reviews"]),
        "filtered_documents": len(filtered_docs),
        "results": [
            {
                "url": doc,
                "score": round(score, 3)
            }
            for doc, score in ranked[:50]
        ]
    }
