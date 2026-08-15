from __future__ import annotations


class PromptBuilder:
    """
    Builds prompts for Retrieval-Augmented Generation (RAG).
    """

    @staticmethod
    def build(
        context: str,
        question: str,
    ) -> str:

        return f"""
You are an AI assistant.

Your job is to answer ONLY using the provided context.

Rules:

1. Never make up information.
2. If the answer is not present in the context,
   reply exactly:

I couldn't find that information in the knowledge base.

3. Answer in clear professional language.
4. Use bullet points whenever appropriate.

----------------------------

Context:

{context}

----------------------------

Question:

{question}

----------------------------

Answer:
"""