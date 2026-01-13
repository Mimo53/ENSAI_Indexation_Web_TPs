from collections import defaultdict
from tokenizer import tokenize_text

def build_inverted_index(documents: list, field_name: str) -> dict:
    """
    Build an inverted index storing only document URLs.
    """
    index = defaultdict(set)

    for doc in documents:
        url = doc.get("url")
        tokens = tokenize_text(doc.get(field_name, ""))

        for token in tokens:
            index[token].add(url)

    return {token: list(urls) for token, urls in index.items()}
