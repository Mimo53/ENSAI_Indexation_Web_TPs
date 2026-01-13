import json

def save_index_to_json(index: dict, output_path: str) -> None:
    """
    Save an index to a JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(index, file, indent=2, ensure_ascii=False)
