QUERY_MAP = {

    "advantages": [
        "benefits",
        "features",
        "uses"
    ],

    "benefits": [
        "advantages",
        "features",
        "uses"
    ],

    "disadvantages": [
        "limitations",
        "drawbacks"
    ],

    "difference": [
        "comparison",
        "compare"
    ],

    "compare": [
        "difference",
        "comparison"
    ],

    "header": [
        "format",
        "structure"
    ]
}


def rewrite_query(query):

    queries = {query}

    words = query.lower().split()

    for i, word in enumerate(words):

        if word in QUERY_MAP:

            for replacement in QUERY_MAP[word]:

                new_words = words.copy()

                new_words[i] = replacement

                queries.add(
                    " ".join(new_words)
                )

    return list(queries)