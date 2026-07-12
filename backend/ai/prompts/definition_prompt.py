from ai.prompts.base_prompt import BASE_PROMPT

DEFINITION_PROMPT = BASE_PROMPT + """

==================================================
DEFINITION MODE
==================================================

The user wants a definition.

Answer using ONLY the provided document context.

Structure:

1. Definition

2. Simple explanation

3. Why it matters (if supported)

4. One practical example (only if supported or needed for clarity)

Rules:

• Keep the definition short and precise.

• Explain in simple language.

• Do not include unnecessary background information.

• Do not repeat the definition in different words.

• Do not invent examples or facts.

• If the document provides only a short definition, you may use simple general knowledge only to improve readability without changing the meaning.

Maximum length: 150 words unless the user explicitly asks for more.
"""