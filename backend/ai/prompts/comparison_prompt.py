from ai.prompts.base_prompt import BASE_PROMPT

COMPARISON_PROMPT = BASE_PROMPT + """

=========================
COMPARISON MODE
=========================

The user wants a comparison.

Always compare both topics directly.

Prefer a markdown table.

After the table, summarize the key differences.
"""