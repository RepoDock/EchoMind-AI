import re


class IntentClassifier:

    def detect(self, query):

        q = query.lower().strip()

        # -----------------------
        # Summary
        # -----------------------

        if any(x in q for x in [
            "summarize",
            "summary",
            "overview",
            "brief",
            "gist"
        ]):
            return "summary"

        # -----------------------
        # Compare
        # -----------------------

        if any(x in q for x in [
            "compare",
            "difference",
            "vs",
            "versus"
        ]):
            return "compare"

        # -----------------------
        # Extraction
        # -----------------------

        if any(x in q for x in [
            "extract",
            "find",
            "list",
            "show all"
        ]):
            return "extract"

        # -----------------------
        # Definition
        # -----------------------

        if re.match(
            r"^(what is|what are|define)\b",
            q
        ):
            return "definition"

        # -----------------------
        # Explanation
        # -----------------------

        if any(x in q for x in [
            "explain",
            "how",
            "why",
            "working"
        ]):
            return "explanation"

        return "general"