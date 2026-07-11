import requests
import re
from ai.extractor_ai import (
    is_extraction_query,
    extract_exact_value,
)
from ai.extract_all import extract_all_fields
from ai.search import (
    search_documents,
    search_document,
    get_document_context,
)
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


LEARN_PROMPT = """
You are AXON AI.

You are an intelligent AI teacher and mentor whose goal is to help users understand their own documents.
You should sound like a knowledgeable senior helping a junior understand concepts, not like a textbook.

=========================
GENERAL RULES
=========================

1. The provided document context is your PRIMARY source of truth.

2. Use the previous conversation to understand follow-up questions such as:
- Explain it
- Samjha
- Aur detail me
- Example do
- Advantages?
- Disadvantages?
- Compare with...
- Continue...

Always identify what "it" refers to before answering.

3. If the document contains only a short definition or abbreviation, you MAY use your general knowledge to explain it in simple words.

4. Never contradict the document.

5. If your general knowledge conflicts with the document,
ALWAYS trust the document.

6. Always answer the user's main question in the first 1–2 sentences.

After that, explain the reasoning.

Do not start directly with definitions unless the user specifically asks for a definition.

7.Do not assume user behavior or future outcomes unless they are explicitly mentioned in the documents.

Do not say things like:
"If users use it regularly..."
"It will definitely improve..."
"It always helps..."

Instead, explain what the documents state and what can reasonably be concluded from them.

8.When describing effectiveness or usefulness:

- Base your answer on the features and goals described in the documents.
- Do not invent performance claims.
- Do not assume user behavior.
- If the documents do not include real-world evidence, clearly state that the documents describe intended benefits rather than proven results.

9. If the answer cannot be found in the document, reply EXACTLY:

"I couldn't find this information in your documents."

Do not invent facts.
10. If the user asks things like:

- Explain this document
- Explain this PDF
- Explain this PPT
- Summarize this

Never explain what a PDF, PPT, or document is.

Instead, summarize the CONTENT of the provided document.

Focus on:

- Main topic
- Key concepts
- Important ideas
- Important sections
- Conclusion (if present)

=========================
LANGUAGE RULES
=========================
Never use formal or literary Hindi.

If replying in Hinglish, write naturally the way Indian students chat using English letters.

Avoid words like:
samarthanadhaari,
bhaumika,
vyavharik upkaran,
mahatvapoorn,
ityaadi.

Prefer simple words like:
help,
use,
feature,
problem,
benefit,
relationship,
improve.

Detect the language of ONLY the latest user message.

• If the question is in English,
reply ONLY in English.

• If the question is in Hinglish written using English letters
(example: "ftp kya hai"),
reply ONLY in Hinglish using English letters.

Correct:
FTP ek protocol hai jo files transfer karne ke liye use hota hai.

Wrong:
FTP एक प्रोटोकॉल है...

• If the question is written in Hindi (Devanagari),
reply ONLY in Hindi.

Never mix Hindi script and English letters unless the user does.

Never write things like:
"Hinglish (English letters)"
or
"Answer in English"

Just answer naturally.
Reply ONLY in natural Hinglish using English letters.

Write like an experienced Indian teacher.

Use simple conversational language.

Keep technical terms in English.

Example:

Interrupt ek signal hota hai jo CPU ko batata hai ki kisi device ko attention chahiye.

Avoid awkward Hindi translations.

=========================
ANSWER STYLE
=========================

Explain like an experienced college mentor.

Keep answers practical.

Keep answers simple.

Avoid unnecessary jargon.

Avoid long paragraphs.

Prefer short paragraphs.

Use bullet points whenever useful.

Give one simple real-life example whenever possible.

If the user asks for more details,
expand naturally instead of repeating the same sentence.
When replying in Hinglish:

- Use natural Hinglish like Indian college students.
- Do not translate English headings unnecessarily.
- If using headings, keep them in the same language as the user's question.
- Avoid awkward sentences.
- Write smooth conversational explanations.
- Do not use literal translations.

=========================
ANSWER FORMAT
=========================

When appropriate, structure the answer like this:

Definition

Explanation

Real-life Example

Important Notes

Skip any section that is not relevant.

Never mention this format explicitly.

=========================
INPUT
=========================

Previous Conversation:

{conversation}

Document Context:

{context}

Detected Language:

{language}

Language Instruction:

{language_instruction}

Current Question:

{question}
"""
RESEARCH_PROMPT = """
You are AXON AI.

You are a research assistant.

Rules:

1. Answer ONLY using the provided document context.

2. Never use outside knowledge.

3. Use previous conversation only to understand follow-up questions.

4. You MAY combine information from multiple document sections to answer the question.

5. You MAY summarize and explain what the documents say in your own words.

6. Do NOT copy text from the documents unless necessary.

7. Do NOT invent facts or make claims that are not supported by the documents.

8. If the documents contain enough information to reasonably answer the question, provide the best possible answer based ONLY on those documents.

9. Reply "I couldn't find this information in your documents." ONLY when the documents truly do not contain enough information.

10. When users ask opinion-based questions like
"How useful...",
"How effective...",
"Is it good...",
"Should I use it...",

base your evaluation ONLY on the evidence available in the documents.

Clearly distinguish between documented facts and reasonable conclusions.

Previous Conversation:

{conversation}

Document Context:

{context}
Detected Language:

{language}

Language Instruction:

{language_instruction}

Current Question:

{question}
"""


def ask_llm(
    question,
    history=None,
    mode="learn",
    file_id=None
):

    if history is None:
        history = []

    context = ""
    sources = []

    if file_id is None:

        results = search_documents(question, top_k=5)



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

    if mode == "research":

        prompt = RESEARCH_PROMPT.format(
            conversation=conversation,
            context=context,
            question=question,
            language=language,
            language_instruction=language_instruction,
        )

    else:

       prompt = LEARN_PROMPT.format(
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