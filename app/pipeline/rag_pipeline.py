from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.llm.groq_client import GroqClient
from app.config.settings import TOP_K_RESULTS

class RAGPipeline:
    """
    Complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(self):
        self.retrieval_pipeline = RetrievalPipeline()
        self.llm = GroqClient()

    def answer_question(self, question: str, top_k: int = TOP_K_RESULTS):

        retrieved_chunks = self.retrieval_pipeline.retrieve(
            question,
            top_k=top_k
        )
        if not retrieved_chunks:
            return {
                "answer": "I could not find the answer in the provided documents.",
                "sources": []
            }
        context = ""

        for chunk in retrieved_chunks:
            context += (
                f"[Page {chunk['page_number']}| Page: {chunk['page_number']}]\n"
                f"{chunk['text']}\n\n"
            )
        
        prompt = f"""
You are an AI assistant that answers questions using only the supplied document context.

Guidelines:
1. Use ONLY the provided context.
2. Do NOT invent or assume information.
3. If the answer is not present in the context, reply:
   "I could not find the answer in the provided document."
4. If multiple context sections contain relevant information, combine them into one coherent answer.
5. Keep the response clear, concise, and professional.
6. Do not mention information outside the supplied context.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self.llm.generate(prompt)

        sources = []

        seen = set()

        for chunk in retrieved_chunks:

            key = (
            chunk["document_name"],
            chunk["page_number"]
            )

            if key not in seen:
                seen.add(key)

                sources.append({
                    "document": chunk["document_name"],
                    "page": chunk["page_number"]
                })

        return {
            "answer": answer,
            "sources": sources
        }
       