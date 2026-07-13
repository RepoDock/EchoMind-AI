INTENT_TOP_K = {
    "definition": 2,
    "explanation": 6,
    "compare": 8,
    "summary": 10,
    "extract": 3,
    "general": 5,
}
OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "qwen2.5:7b"

DEBUG = True

HALLUCINATION_MIN_SCORE = 0.35
HALLUCINATION_MIN_RESULTS = 2

MAX_CONTEXT_CHARS = 2500