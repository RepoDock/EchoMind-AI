from ai.prompts.base_prompt import (
    LEARN_PROMPT,
    RESEARCH_PROMPT
)


class PromptSelector:

    def get_prompt(self, intent, mode="learn"):

        if mode == "research":
            return RESEARCH_PROMPT

        return LEARN_PROMPT