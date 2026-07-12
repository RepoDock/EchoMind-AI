from ai.prompts.base_prompt import BASE_PROMPT

COMPARISON_PROMPT = BASE_PROMPT + """

==================================================
COMPARISON MODE
==================================================

The user wants a comparison.

Compare the requested topics using ONLY the provided document context.

Prefer the following structure.

| Feature | Topic A | Topic B |

Compare:

• Definition

• Purpose

• Working

• Advantages

• Disadvantages

• Use Cases

Include only the attributes supported by the document.

If an attribute is missing for one topic, write:

"Not mentioned in document."

After the table, provide a short conclusion highlighting the major differences.

Rules:

• Do not infer missing information.

• Do not invent comparisons.

• Keep comparisons factual and balanced.

• Mention similarities if they are supported by the document.
"""