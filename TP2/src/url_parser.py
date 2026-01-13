from urllib.parse import urlparse, parse_qs

def extract_product_metadata(url: str) -> dict:
    """
    Extract product id and variant from a product URL.
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")

    product_id = None
    if "product" in path_parts:
        product_id = path_parts[-1]

    query_params = parse_qs(parsed_url.query)
    variant = query_params.get("variant", [None])[0]

    return {
        "product_id": product_id,
        "variant": variant
    }
