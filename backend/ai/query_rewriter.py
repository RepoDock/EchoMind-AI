import re

QUERY_MAP = {
    "advantages": [
        "benefits",
        "uses",
        "features",
        "importance"
    ],
    "benefits": [
        "advantages",
        "uses",
        "features"
    ],
    "disadvantages": [
        "limitations",
        "drawbacks",
        "cons"
    ],
    "compare": [
        "difference between",
        "comparison of",
        "vs"
    ],
    "difference": [
        "compare",
        "comparison between",
        "vs"
    ],
}


def clean_query(query):
    query = re.sub(r"[^\w\s]", "", query)
    return query.strip()


def rewrite_query(query):

    query = clean_query(query)

    queries = set()

    queries.add(query)

    q = query.lower()

    # -----------------------------
    # Explain
    # -----------------------------

    if q.startswith("explain "):

        topic = query[8:].strip()

        queries.update([
            topic,
            f"What is {topic}",
            f"{topic} definition",
            f"{topic} overview",
            f"{topic} working",
            f"Functions of {topic}"
        ])

    # -----------------------------
    # What is
    # -----------------------------

    elif q.startswith("what is "):

        topic = query[8:].strip()

        queries.update([
            topic,
            f"{topic} definition",
            f"{topic} overview",
            f"{topic} working"
        ])

    # -----------------------------
    # Advantages
    # -----------------------------

    elif "advantages" in q:

        topic = q.replace("advantages of", "").strip()

        queries.update([
            f"Benefits of {topic}",
            f"Uses of {topic}",
            f"Features of {topic}",
            f"Importance of {topic}"
        ])

    # -----------------------------
    # Compare
    # -----------------------------

    elif q.startswith("compare"):

        topic = query[7:].strip()

        queries.update([
            f"Difference between {topic}",
            f"{topic} comparison",
            f"{topic} vs"
        ])

    # -----------------------------
    # Dictionary Expansion
    # -----------------------------

    words = q.split()

    for i, word in enumerate(words):

        if word in QUERY_MAP:

            for replacement in QUERY_MAP[word]:

                new_words = words.copy()

                new_words[i] = replacement

                queries.add(
                    " ".join(new_words)
                )

    return list(queries)