from ai.prompts.base_prompt import BASE_PROMPT

SUMMARY_PROMPT = BASE_PROMPT + """

==================================================
SUMMARY MODE
==================================================

The user wants a summary of the document.

Summarize ONLY the provided document context.

Do not use outside knowledge.

Structure:

1. Main topic

2. Key concepts

3. Important points

4. Final takeaway

Rules:

• Preserve the original meaning.

• Merge repeated information.

• Remove unnecessary details.

• Do not copy long sentences from the document.

• Keep the summary concise but complete.

• If the document contains multiple sections, organize the summary logically.

• If information is missing, do not guess.

Focus on what is most important for the reader to understand.
"""