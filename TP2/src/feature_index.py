from collections import defaultdict
from urllib.parse import urlparse, parse_qs


def build_category_index(documents: list) -> dict:
    """
    Build an inverted index for product categories extracted from URLs.
    """
    index = defaultdict(set)

    for doc in documents:
        url = doc.get("url")
        if not url:
            continue

        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)

        category = params.get("category", [None])[0]
        if category:
            index[category.lower()].add(url)

    return {k: list(v) for k, v in index.items()}


def build_feature_index(documents: list) -> dict:
    """
    Build feature indexes for:
    - brand
    - origin (made in)
    - material
    - review date (YYYY-MM)
    """

    brand_index = defaultdict(set)
    origin_index = defaultdict(set)
    material_index = defaultdict(set)
    date_index = defaultdict(set)

    for doc in documents:
        url = doc.get("url")
        if not url:
            continue

        features = doc.get("product_features", {})

        # ---------- BRAND ----------
        brand = features.get("brand")
        if brand:
            brand_index[brand.lower()].add(url)

        # ---------- ORIGIN ----------
        origin = (
            features.get("origin")
            or features.get("made in")
            or features.get("made_in")
        )
        if origin:
            origin_index[origin.lower()].add(url)

        # ---------- MATERIAL ----------
        material = features.get("material")
        if material:
            material_index[material.lower()].add(url)

        # ---------- REVIEW DATE (YYYY-MM) ----------
        reviews = doc.get("product_reviews", [])
        for review in reviews:
            date = review.get("date")  # ex: 2022-06-15
            if date and len(date) >= 7:
                year_month = date[:7]  # 2022-06
                date_index[year_month].add(url)

    return {
        "brand": {k: list(v) for k, v in brand_index.items()},
        "origin": {k: list(v) for k, v in origin_index.items()},
        "material": {k: list(v) for k, v in material_index.items()},
        "date": {k: list(v) for k, v in date_index.items()},
    }
