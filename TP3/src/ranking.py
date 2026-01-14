import math
import json
from collections import defaultdict
import os

# --- Default weights ---
TITLE_WEIGHT = 6.0
DESCRIPTION_WEIGHT = 2.0
MEAN_MARK_WEIGHT = 2.0
TOTAL_REVIEWS_WEIGHT = 1.0

# --- Try to load optimized weights if they exist ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data")
WEIGHTS_PATH = os.path.join(DATA_PATH, "optimized_weights.json")

if os.path.exists(WEIGHTS_PATH):
    with open(WEIGHTS_PATH, "r") as f:
        weights = json.load(f)
        TITLE_WEIGHT = weights.get("title", TITLE_WEIGHT)
        DESCRIPTION_WEIGHT = weights.get("description", DESCRIPTION_WEIGHT)
        MEAN_MARK_WEIGHT = weights.get("mean_mark", MEAN_MARK_WEIGHT)
        TOTAL_REVIEWS_WEIGHT = weights.get("total_reviews", TOTAL_REVIEWS_WEIGHT)

def compute_bm25(token, doc, index, avgdl, doc_len, k1=1.5, b=0.75):
    df = len(index.get(token, {}))
    if df == 0:
        return 0
    idf = math.log(1 + (1 / df))
    tf = len(index[token].get(doc, []))
    denom = tf + k1*(1-b+b*(doc_len/avgdl))
    return idf*((tf*(k1+1))/denom)

def rank_documents(docs, tokens, title_index, description_index, reviews_index):
    scores = defaultdict(float)
    avgdl = 50
    for doc in docs:
        doc_len = 50
        for token in tokens:
            scores[doc] += TITLE_WEIGHT * compute_bm25(token, doc, title_index, avgdl, doc_len)
            scores[doc] += DESCRIPTION_WEIGHT * compute_bm25(token, doc, description_index, avgdl, doc_len)
        reviews = reviews_index.get(doc,{})
        scores[doc] += reviews.get("mean_mark",0)*MEAN_MARK_WEIGHT
        scores[doc] += reviews.get("total_reviews",0)*TOTAL_REVIEWS_WEIGHT
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
