import re

STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "a", "for", "on", "with"
}

def tokenize_text(text: str) -> list[str]:
    """
    Tokenize a text by space, remove punctuation and stopwords.
    """
    if not text:
        return []

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()

    return [token for token in tokens if token not in STOPWORDS]
