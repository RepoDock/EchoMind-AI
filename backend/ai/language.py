import re


def detect_language(text):

    if re.search(r'[\u0900-\u097F]', text):
        return "hindi"

    text = text.lower()

    hinglish_words = [
        "kya",
        "hai",
        "kaise",
        "kyu",
        "samjha",
        "matlab",
        "karna",
        "krna",
        "aur",
        "isko",
        "usko",
        "mera",
        "tum",
        "mujhe"
    ]

    for word in hinglish_words:
        if word in text:
            return "hinglish"

    return "english"


def get_language_instruction(language):

    instructions = {

        "english": """
Reply ONLY in English.

Do NOT use Hindi.

Do NOT use Hinglish.

Never mix English with Hindi.
""",

        "hinglish": """
Reply ONLY in natural Hinglish using English letters.

Do NOT use Hindi (Devanagari).

Write naturally like Indian students chat.

Keep technical terms in English.
""",

        "hindi": """
Reply ONLY in Hindi (Devanagari).

Do NOT use Hinglish.

Use simple Hindi.
"""
    }

    return instructions.get(language, instructions["english"])