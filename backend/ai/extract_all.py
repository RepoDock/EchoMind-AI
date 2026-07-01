import re

from ai.field_aliases import FIELD_ALIASES
from ai.field_regex import FIELD_REGEX
from ai.extractor_ai import build_patterns

PATTERNS = build_patterns()

INVALID_VALUES = {
    "",
    "-",
    ":",
    "n/a",
    "na",
    "null",
    "none"
}
FIELD_PRIORITY = [

    "name",
    "owner",

    "phone",
    "email",

    "aadhaar",
    "pan",
    "passport",

    "registration",
    "vehicle_number",
    "vin",
    "chassis",
    "engine",

    "gst",
    "invoice",
    "amount"

]
def extract_all_fields(context):

    extracted = {}

    ordered_fields = FIELD_PRIORITY + [

        f for f in FIELD_ALIASES

        if f not in FIELD_PRIORITY
    ]

    for field in ordered_fields:

        value = None

        # ------------------------
        # 1. Field Specific Regex
        # ------------------------
        if field in FIELD_REGEX:

            match = re.search(
                FIELD_REGEX[field],
                context,
                re.IGNORECASE
            )

            if match:
                value = match.group(0).strip()

        # ------------------------
        # 2. Alias Pattern
        # ------------------------
        if value is None:

            pattern = PATTERNS.get(field)

            if pattern is None:
                continue

            match = re.search(
                pattern,
                context,
                re.IGNORECASE | re.MULTILINE
            )

            if not match:

                multiline_pattern = pattern.replace(
                    r"\s*[:\-]?\s*",
                    r"\s*[:\-]?\s*\n+\s*"
                )

                match = re.search(
                    multiline_pattern,
                    context,
                    re.IGNORECASE | re.MULTILINE
                )

            if match:

                value = match.group(1).strip()

        # ------------------------
        # Save Result
        # ------------------------
        if value:

            value = value.strip()

            if value.lower() in INVALID_VALUES:
                continue

            # Ignore very short garbage values
            if len(value) < 2:
                continue

            if value not in extracted.values():

                extracted[field] = value

    return extracted