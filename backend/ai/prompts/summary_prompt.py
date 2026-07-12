from ai.prompts.base_prompt import BASE_PROMPT

SUMMARY_PROMPT = BASE_PROMPT + """

=========================
SUMMARY MODE
=========================

Summarize only the document content.

Include:

- Main topic
- Key concepts
- Important points
- Final takeaway

Avoid unnecessary details.
"""