import requests
import re
from ai.extractor_ai import (
    is_extraction_query,
    extract_exact_value,
)
from ai.prompts.base_prompt import (
    LEARN_PROMPT,
    RESEARCH_PROMPT
)
from ai.prompts.prompt_selector import PromptSelector
from ai.hallucination_guard import HallucinationGuard
from ai.extract_all import extract_all_fields
from ai.search import (
    search_documents,
    search_document,
    get_document_context,
)
from ai.intent_classifier import IntentClassifier
from ai.hybrid_search import HybridSearch
def detect_language(text):

    if re.search(r'[\u0900-\u097F]', text):
        return "hindi"

    text = text.lower()

    hinglish_words = [
        "kya",
        "hai",
        "kaise",
        "kyu",
        "samjha",
        "matlab",
        "karna",
        "krna",
        "aur",
        "isko",
        "usko",
        "mera",
        "tum",
        "mujhe"
    ]

    for word in hinglish_words:
        if word in text:
            return "hinglish"

    return "english"
OLLAMA_URL = "http://localhost:11434/api/generate"




def ask_llm(
    question,
    history=None,
    mode="learn",
    file_id=None
):

    if history is None:
        history = []
    
    guard = HallucinationGuard()
    hybrid = HybridSearch()
    intent = IntentClassifier()

    query_type = intent.detect(question)
    context = ""
    sources = []

    if file_id is None:

        results = hybrid.search(
            query=question,
            top_k=5
        )
        # if not guard.validate(results):

        #     return {
        #         "answer": "I couldn't find enough information in your documents to answer this question reliably.",
        #         "sources": []
        #     }



        if not results:
            return {
                "answer": "I couldn't find this information in your documents.",
                "sources": []
            }
        seen_files = set()

        for _, score, chunk, file_name, page_number in results:

            context += f"""
            Source: {file_name}
            Page: {page_number}

            {chunk}

            --------------------
            """


            if score >= 0.25 and file_name not in seen_files:
                sources.append({
                    "file": file_name,
                    "page": page_number
                })
                seen_files.add(file_name)

    else:

        summary_keywords = [
                "summarize",
                "summary",
                "overview",
                "explain this",
                "explain this document",
                "explain this ppt",
                "explain this pdf",
                "explain the document",
                "summarise",
                "describe this",
                "what is this document about",
            ]

        if any(k in question.lower() for k in summary_keywords):

                context = get_document_context(file_id)

                question = """
            Summarize this document.

            Your answer should include:

            1. Main topic
            2. Important concepts
            3. Key points
            4. Important sections
            5. Final conclusion (if present)

            Do NOT explain what a PDF, PPT or document is.

            Explain only the CONTENT of the provided document.
            """
        else:

            results = search_document(
                file_id,
                question,
                top_k=5
            )
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
            # Smart Information Extraction
            q = question.lower()

            extract_all = (
                "extract" in q
                or ("all" in q and "information" in q)
                or ("all" in q and "details" in q)
                or ("key" in q and "information" in q)
                or ("important" in q and "information" in q)
                or ("summary" in q)
                or ("summarize" in q)
                or ("show" in q and "information" in q)
                or ("give" in q and "information" in q)
            )

            if extract_all:

                search_context = get_document_context(file_id)

                fields = extract_all_fields(search_context)
# Debug

                if fields:

                    answer = ""

                    for key, value in fields.items():
                        answer += f"{key.replace('_',' ').title()}: {value}\n"

                    return {
                        "answer": value,
                        "sources": [{
                            "file": results[0][3],
                            "page": results[0][4]
                        }]
                    }
          
            if is_extraction_query(question):

                search_context = get_document_context(file_id)

                fields = extract_all_fields(search_context)
                value = extract_exact_value(
                    question,
                    search_context
                )

                print("Extracted:", value)

                if value:
                    return {
                        "answer": value,
                        "sources": [{
                            "file": results[0][3],
                            "page": "Entire Document"
                        }]
                    }

            seen_sources = set()

            for _, score, chunk, file_name, page_number in results:

                context += f"""
                Page: {page_number}

                {chunk}

                """

                source_key = (file_name, page_number)

                if source_key not in seen_sources:

                    sources.append({
                        "file": file_name,
                        "page": page_number
                    })

                    seen_sources.add(source_key)
    language = detect_language(question)
    if language == "english":

        language_instruction = """
        Reply ONLY in English.

        Do NOT use Hindi.

        Do NOT use Hinglish.

        Never mix English with Hindi.
        """

    elif language == "hinglish":

        language_instruction = """
    Reply ONLY in Hinglish using English letters.

    Do NOT use Hindi (Devanagari).

    Write naturally like Indian students chat.

    Example:

    FTP ek protocol hai jo files transfer karne ke liye use hota hai.
    """

    else:

        language_instruction = """
    Reply ONLY in Hindi (Devanagari).

    Do NOT use Hinglish.

    Use simple Hindi.
    """
    conversation = ""

    for message in history:

        role = "User" if message["role"] == "user" else "Assistant"

        conversation += f"{role}: {message['text']}\n"

    selector = PromptSelector()

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
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
        }
    )
    print("Status: ",response.status_code)
    print("Response: ",response.text)
    answer = response.json()["response"]

    return {
        "answer": answer,
        "sources": sources
    }