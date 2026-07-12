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
def get_last_topic(history):

    if not history:
        return None

    # latest user messages first
    for message in reversed(history):

        if message.get("role") != "user":
            continue

        text = message.get("text", "").strip()

        if not text:
            continue

        text = clean_query(text)

        lower = text.lower()

        m = re.match(
        r"^(what is|what are|define|explain|compare)\s+(.+)$",
        lower
    )

        if m:
            return m.group(2).strip()
    return None
def rewrite_query(query, history=None):

    query = clean_query(query)

    queries = set()

    queries.add(query)

    q = query.lower()
    topic = get_last_topic(history)

    FOLLOWUPS = [

        "advantages",
        "advantages?",
        "benefits",
        "benefits?",
        "limitations",
        "limitations?",
        "disadvantages",
        "uses",
        "uses?",
        "features",
        "features?",
        "working",
        "working?",
        "how",
        "how?",
        "why",
        "why?",
        "continue",
        "continue.",
        "explain more",
        "tell me more",
        "more",
        "more details"
    ]

    if topic and q in FOLLOWUPS:

        query = f"{q.rstrip('?')} of {topic}"

        q = query.lower()

        queries.add(query)

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
    elif topic and q in [

        "compare",

        "compare both",

        "difference",

        "difference?",

        "compare them"

    ]:

        query = f"Compare {topic}"

        queries.add(query)
    elif re.match(r"^(what is|what are)\s+", q):

        topic = re.sub(r"^(what is|what are)\s+", "", query, flags=re.I).strip()

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