import re


class IntentClassifier:

    def detect(self, query):

        q = query.lower().strip()

        # -----------------------
        # Follow-up
        # -----------------------

        if re.fullmatch(
            r"(continue|explain more|tell me more|go deeper|elaborate|why\??|how\??|what about.*|and then.*)",
            q
        ):
            return "followup"

        # -----------------------
        # Summary
        # -----------------------

        if any(x in q for x in [
            "summarize",
            "summary",
            "overview",
            "brief",
            "gist",
            "tldr",
            "tl;dr",
            "main points",
            "key points",
            "key takeaways",
            "in short"
        ]):
            return "summary"

        # -----------------------
        # Comparison
        # -----------------------

        if (
            any(x in q for x in [
                "compare",
                "difference",
                "versus",
                "vs",
                "similarities",
                "advantages and disadvantages",
                "pros and cons"
            ])
            or re.search(r"\b.+\s+vs\s+.+\b", q)
        ):
            return "compare"

        # -----------------------
        # Extraction
        # -----------------------

        if any(x in q for x in [
            "extract",
            "find",
            "list",
            "show all",
            "give all",
            "names",
            "dates",
            "emails",
            "phone numbers",
            "companies",
            "addresses",
            "ids"
        ]):
            return "extract"

        # -----------------------
        # Definition
        # -----------------------

        if (
            re.match(
                r"^(what is|what are|define|meaning of|full form of|expand)\b",
                q
            )
            or "stands for" in q
        ):
            return "definition"

        # -----------------------
        # Explanation
        # -----------------------

        if any(x in q for x in [
            "explain",
            "working",
            "how does",
            "how do",
            "why does",
            "why do",
            "how it works",
            "why it works"
        ]):
            return "explanation"

        return "general"