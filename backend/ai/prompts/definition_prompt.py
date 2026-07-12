from ai.prompts.base_prompt import BASE_PROMPT

DEFINITION_PROMPT = BASE_PROMPT + """

=========================
DEFINITION MODE
=========================

The user wants a definition.

Structure:

1. Short definition.

2. Simple explanation.

3. One example ONLY if it improves understanding.

Maximum 150 words.

Do not add unnecessary notes.
"""