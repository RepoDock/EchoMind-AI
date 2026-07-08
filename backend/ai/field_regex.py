FIELD_REGEX = {

    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}",

    "phone": r"(?:\+91[- ]?)?[6-9]\d{9}",

    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",

    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    "gstin": r"\b\d{2}[A-Z]{5}[0-9]{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b",

    "vin": r"\b[A-HJ-NPR-Z0-9]{17}\b",

    "vehicle_number": r"\b[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{4}\b",

    "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

    "currency": r"(?:₹|Rs\.?|INR)\s?\d[\d,]*(?:\.\d+)?",

}