class HallucinationGuard:

    def validate(self, confidence):

        score = confidence["score"]
        level = confidence["level"]

        if level == "High":
            return True

        if level == "Medium" and score >= 0.60:
            return True

        return False