def filter_any_token(tokens, indexes):
    """At least one token present"""
    docs = set()

    for token in tokens:
        for index in indexes:
            if token in index:
                docs.update(index[token])

    return docs

def filter_all_tokens(tokens, indexes):
    """All tokens must be present"""
    docs = None

    for token in tokens:
        token_docs = set()
        for index in indexes:
            if token in index:
                token_docs.update(index[token])

        if not token_docs:
            return set()

        docs = token_docs if docs is None else docs & token_docs

    return docs or set()
