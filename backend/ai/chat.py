import requests
from ai.language import (
    detect_language,
    get_language_instruction
)
from ai.extraction_handler import ExtractionHandler
from ai.summary_handler import SummaryHandler
from ai.context_builder import ContextBuilder
from ai.citation_engine import CitationEngine
from ai.confidence import ConfidenceScorer
from ai.config import (
    INTENT_TOP_K,
    OLLAMA_URL,
    OLLAMA_MODEL,
    DEBUG,
)
from ai.prompts.prompt_selector import PromptSelector
from ai.hallucination_guard import HallucinationGuard
from ai.search import (
    search_document
)
from ai.intent_classifier import IntentClassifier
from ai.hybrid_search import HybridSearch

extraction_handler = ExtractionHandler()
summary_handler = SummaryHandler()
confidence = ConfidenceScorer()
citation = CitationEngine()
context_builder = ContextBuilder()
guard = HallucinationGuard()
hybrid = HybridSearch()
intent = IntentClassifier()
selector = PromptSelector()



def ask_llm(
    question,
    history=None,
    mode="learn",
    file_id=None
):

    if history is None:
        history = []
    

    query_type = intent.detect(question)
    context = ""
    sources = []
    confidence_info = {
        "score": 0.0,
        "level": "Low"
    }
    warning = ""

    if file_id is None:

        top_k = INTENT_TOP_K.get(query_type, 5)

        results = hybrid.search(
            query=question,
            history=history,
            top_k=top_k
        )

        if not results:
            return {
                "answer": "I couldn't find this information in your documents.",
                "sources": []
            }
        confidence_info = confidence.calculate(results)
        if not guard.validate(results):

            warning = (
                "⚠️ This answer is based on limited information "
                "found in your documents.\n\n"
            )
        context = context_builder.build(results)
        sources = citation.build(results)

    else:

        if summary_handler.is_summary_request(question):

            context, question = summary_handler.prepare(file_id)

            sources = [{
                "file": "Current Document",
                "page": "Entire Document"
            }]
        else:

            top_k = INTENT_TOP_K.get(query_type, 5)

            results = search_document(
                file_id,
                question,
                top_k=top_k
            )
            if DEBUG:

                print("=" * 60)

                for _, score, chunk, file_name, page_number in results:

                    print(page_number, score)
                    print(chunk[:250])
                    print("-" * 40)

                print("=" * 60)

            if not results:
                return {
                    "answer": "I couldn't find this information in your document.",
                    "sources": []
                }
            confidence_info = confidence.calculate(results)
            if not guard.validate(results):

                warning = (
                    "⚠️ This answer is based on limited information "
                    "found in your document.\n\n"
                )
            # Smart Information Extraction
            result = extraction_handler.handle(
                question=question,
                file_id=file_id,
                results=results,
                warning=warning,
                confidence_info=confidence_info,
                citation_engine=citation,
            )

            if result:
                return result

            context = context_builder.build(
                results,
                include_source=False
            )

            sources = citation.build(results)
    language = detect_language(question)

    language_instruction = get_language_instruction(language)
    conversation = ""

    for message in history:

        role = "User" if message["role"] == "user" else "Assistant"

        conversation += f"{role}: {message['text']}\n"


    template = selector.get_prompt(
        intent=query_type,
        mode=mode
    )

    prompt = template.format(
        conversation=conversation,
        context=context,
        question=question,
        language=language,
        language_instruction=language_instruction,
    )
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }
    )
    if DEBUG:

        print("Status:", response.status_code)
        print("Response:", response.text)
    answer = response.json()["response"]
    answer = warning + answer

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence_info
    }