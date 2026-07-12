from ai.config import (
    HALLUCINATION_MIN_SCORE,
    HALLUCINATION_MIN_RESULTS,
)


class HallucinationGuard:

    def validate(self, results):

        if not results:
            return False

        if len(results) < HALLUCINATION_MIN_RESULTS:
            return False

        best_score = results[0][1]

        if best_score < HALLUCINATION_MIN_SCORE:
            return False

        return True