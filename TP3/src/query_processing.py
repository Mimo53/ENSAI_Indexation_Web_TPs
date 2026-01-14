from tokenizer import tokenize
from synonyms import expand_with_synonyms

def process_query(query: str, synonyms: dict) -> list[str]:
    tokens = tokenize(query)
    tokens = expand_with_synonyms(tokens, synonyms)
    return tokens
