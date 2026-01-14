def expand_with_synonyms(tokens: list[str], synonyms: dict) -> list[str]:
    expanded = set(tokens)

    for token in tokens:
        if token in synonyms:
            expanded.update(synonyms[token])
        for key, values in synonyms.items():
            if token in values:
                expanded.add(key)

    return list(expanded)
