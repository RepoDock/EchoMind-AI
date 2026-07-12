from ai.prompts.base_prompt import (
    BASE_PROMPT
)
from ai.prompts.followup_prompt import FOLLOWUP_PROMPT
from ai.prompts.research_prompt import RESEARCH_PROMPT
from ai.prompts.definition_prompt import DEFINITION_PROMPT
from ai.prompts.explanation_prompt import EXPLANATION_PROMPT
from ai.prompts.comparison_prompt import COMPARISON_PROMPT
from ai.prompts.summary_prompt import SUMMARY_PROMPT
from ai.prompts.extraction_prompt import EXTRACTION_PROMPT


class PromptSelector:

    def get_prompt(self, intent, mode="learn"):
        if intent == "followup":
            return FOLLOWUP_PROMPT
        if mode == "research":
            return RESEARCH_PROMPT

        if intent == "definition":
            return DEFINITION_PROMPT

        elif intent == "compare":
            return COMPARISON_PROMPT

        elif intent == "summary":
            return SUMMARY_PROMPT

        elif intent == "extract":
            return EXTRACTION_PROMPT

        elif intent == "explanation":
            return EXPLANATION_PROMPT

        return BASE_PROMPT