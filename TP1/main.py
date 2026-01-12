# -*- coding: utf-8 -*-
import sys
import json
import os
from crawler.crawler import crawl


def save_to_jsonl(data, filename="crawl_results.jsonl"):
    
    # Sauvegarde les résultats du crawl dans le dossier output/
    
    output_dir = "output"

    # Crée le dossier output s'il n'existe pas (je ne sais pas si quand on clône le projet le fichier est présent ou non (comme il contient un fichier ça ne devrait pas être le cas mais je le laisse au cas où))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        for document in data:
            json.dump(document, file, ensure_ascii=False)
            file.write("\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <start_url> <max_pages>")
        sys.exit(1)

    start_url = sys.argv[1]

    try:
        max_pages = int(sys.argv[2])
    except ValueError:
        print("Le nombre de pages doit être un entier.") #pour éviter un problème que j'ai eu en scrapant où une erreur de requêtage a rendus le nombre le page non entière
        sys.exit(1)

    results = crawl(start_url, max_pages)
    save_to_jsonl(results)

    print("{} pages crawlées.".format(len(results)))


if __name__ == "__main__":
    main()
