from ai.prompts.base_prompt import BASE_PROMPT

EXTRACTION_PROMPT = BASE_PROMPT + """

=========================
EXTRACTION MODE
=========================

Return ONLY the requested information.

Do not explain.

Do not summarize.

If multiple values exist, list them clearly.
"""