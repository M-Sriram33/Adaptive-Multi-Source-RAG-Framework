
from app.pipeline.multi_source_pipeline import MultiSourcePipeline
from app.pipeline.context_fusion import ContextFusion
from app.pipeline.multi_source_answer_generator import (
    MultiSourceAnswerGenerator
)


class MultiSourceRAGPipeline:
    """
    Complete multi-source Retrieval-Augmented Generation pipeline.
    """

    def __init__(self, router, groq_client=None):

        # Source routing and retrieval
        self.retrieval_pipeline = MultiSourcePipeline(router)

        # Context fusion
        self.context_fusion = ContextFusion()

        # Answer generation
        self.answer_generator = MultiSourceAnswerGenerator(
            groq_client=groq_client
        )

    def answer_question(self, question: str) -> dict:
        """
        Execute the complete multi-source RAG workflow.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # Step 1: Retrieve information from selected sources
        retrieval_output = self.retrieval_pipeline.retrieve(
            question
        )

        # Step 2: Combine retrieved information
        fused_context = self.context_fusion.fuse(
            retrieval_output
        )

        # Step 3: Generate grounded answer
        answer_output = self.answer_generator.generate_answer(
            question=question,
            fused_context=fused_context
        )

        # Step 4: Return final response
        return {
            "question": question,
            "answer": answer_output["answer"],
            "sources": answer_output["sources"],
            "sources_used": retrieval_output["sources_used"]
        }
