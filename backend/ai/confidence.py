class ConfidenceScorer:

    def calculate(self, results):

        if not results:
            return {
                "score": 0.0,
                "level": "Low"
            }

        scores = [score for _, _, score, *_ in results]

        avg_score = sum(scores) / len(scores)

        if avg_score >= 0.80:
            level = "High"

        elif avg_score >= 0.50:
            level = "Medium"

        else:
            level = "Low"

        return {
            "score": round(avg_score, 3),
            "level": level
        }