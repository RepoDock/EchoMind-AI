class HallucinationGuard:

    def validate(self, results):

        if not results:
            return False

        # Minimum retrieved chunks
        if len(results) < 2:
            return False

        # Minimum retrieval score
        best_score = results[0][1]

        if best_score < 0.35:
            return False

        return True