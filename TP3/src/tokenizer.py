import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

def tokenize(text: str) -> list[str]:
    if not text:
        return []

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()

    return [t for t in tokens if t not in STOPWORDS]
