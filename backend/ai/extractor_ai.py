import re
from ai.field_aliases import FIELD_ALIASES
from ai.field_regex import FIELD_REGEX

EXTRACTION_KEYWORDS = {
    alias.lower()
    for aliases in FIELD_ALIASES.values()
    for alias in aliases
}
def build_patterns():

    patterns = {}

    for field, aliases in FIELD_ALIASES.items():

        label = "|".join(
            re.escape(alias)
            for alias in aliases
        )

        patterns[field] = (
        rf"(?:{label})"
        rf"\s*[:\-]?\s*"
        rf"([^\n\r]{{2,200}})"
    )

    return patterns


PATTERNS = build_patterns()


def is_extraction_query(query):

    query = query.lower()

    extraction_words = [
        "extract",
        "show",
        "find",
        "give",
        "tell",
        "display",
        "what is my",
        "what's my",
        "what is the",
        "what's the",
    ]

    if not any(word in query for word in extraction_words):
        return False

    return any(
        alias.lower() in query
        for aliases in FIELD_ALIASES.values()
        for alias in aliases
    )
def extract_exact_value(question, context):

    question = question.lower()

    field = None

    for key, aliases in FIELD_ALIASES.items():

        if any(alias in question for alias in aliases):
            field = key
            break

    if field is None:
        return None

    aliases = FIELD_ALIASES[field]

    label = "|".join(
        re.escape(alias)
        for alias in sorted(aliases, key=len, reverse=True)
    )

    pattern = (
        rf"(?:{label})"
        rf"(?:\s*[:\-]?\s*)"
        rf"(?:\r?\n\s*)?"
        rf"([A-Za-z0-9\/\-. ]{{2,150}})"
    )

    index = context.lower().find("chassis")

    if index != -1:
        print("========== CONTEXT ==========")
        print(context[index:index+300])
    print("=============================")

    match = re.search(
        pattern,
        context,
        re.IGNORECASE | re.MULTILINE
    )

    if not match:
        return None

    # Extract value
    value = match.group(1).strip()

    # Validate with regex if available
    if field in FIELD_REGEX:

        regex = FIELD_REGEX[field]

        valid = re.search(
            regex,
            value,
            re.IGNORECASE
        )

        if valid:
            return valid.group(0)

    # Otherwise return extracted value
    return value
    lines = context.splitlines()

    for i, line in enumerate(lines):

        if any(alias.lower() in line.lower() for alias in aliases):

            # Same line ke baad value
            if ":" in line:

                after = line.split(":", 1)[1].strip()

                if after:
                    return after

            # Next line me value ho
            if i + 1 < len(lines):

                next_line = lines[i + 1].strip()

                if next_line:
                    return next_line

    return None