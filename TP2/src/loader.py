import json

def load_jsonl_file(file_path: str) -> list:
    """
    Load a JSONL file and return a list of documents.
    """
    documents = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                documents.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return documents
