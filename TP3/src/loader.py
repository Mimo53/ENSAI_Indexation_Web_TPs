import json

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_jsonl(path: str) -> list:
    documents = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            documents.append(json.loads(line))
    return documents
