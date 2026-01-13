from collections import defaultdict
from tokenizer import tokenize_text

def build_positional_index(documents: list, field_name: str) -> dict:
    """
    Build a positional inverted index.
    """
    index = defaultdict(lambda: defaultdict(list))

    for doc in documents:
        url = doc.get("url")
        tokens = tokenize_text(doc.get(field_name, ""))

        for position, token in enumerate(tokens):
            index[token][url].append(position)

    return index
