from ai.prompts.base_prompt import BASE_PROMPT

EXPLANATION_PROMPT = BASE_PROMPT + """

=========================
EXPLANATION MODE
=========================

The user wants a detailed explanation.

Structure:

- Simple explanation
- Why it is important
- How it works (if applicable)
- One practical example
- Important notes (only if relevant)

Avoid repeating the same point.
"""