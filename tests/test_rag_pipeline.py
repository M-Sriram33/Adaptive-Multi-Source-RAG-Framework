
from app.pipeline.rag_pipeline import RAGPipeline


def test_rag_pipeline():
    rag = RAGPipeline()

    question = "Give me an overview of Toyota."

    result = rag.answer_question(question)

    # Verify answer generation
    assert result["answer"] is not None
    assert len(result["answer"].strip()) > 0

    # Verify source attribution
    assert isinstance(result["sources"], list)

    # If an answer is retrieved from the document,
    # source references should be available.
    if "could not find" not in result["answer"].lower():
        assert len(result["sources"]) > 0
