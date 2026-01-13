def build_reviews_index(documents: list) -> dict:
    """
    Build a reviews index using the product_reviews field.
    """
    index = {}

    for doc in documents:
        url = doc.get("url")
        reviews = doc.get("product_reviews", [])

        if reviews:
            count = len(reviews)
            average = sum(r.get("rating", 0) for r in reviews) / count
            last = reviews[-1].get("rating")
        else:
            count = 0
            average = None
            last = None

        index[url] = {
            "total_reviews": count,
            "average_rating": average,
            "last_rating": last
        }

    return index
