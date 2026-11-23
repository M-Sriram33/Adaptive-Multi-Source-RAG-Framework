
import pytest

from app.pipeline.multi_source_answer_generator import (
    MultiSourceAnswerGenerator
)


class MockGroqClient:
    """
    Mock Groq client for testing answer generation.
    """

    def __init__(self):
        self.received_prompt = None

    def generate(self, prompt):
        self.received_prompt = prompt

        return (
            "Arun has taken 5 leave days. "
            "The policy provides 15 annual leave days."
        )


def test_multi_source_answer_generation():

    mock_llm = MockGroqClient()

    generator = MultiSourceAnswerGenerator(
        groq_client=mock_llm
    )

    fused_context = {
        "context": """
        Document: Annual leave entitlement is 15 days.

        SQL: Arun has taken 5 leave days.
        """,
        "sources": [
            {
                "source_type": "document",
                "document": "leave_policy.pdf",
                "page": 3
            },
            {
                "source_type": "sql",
                "query": "SELECT * FROM leaves;",
                "record_count": 1
            }
        ]
    }

    result = generator.generate_answer(
        question="How many leave days has Arun taken?",
        fused_context=fused_context
    )

    assert "Arun" in result["answer"]
    assert len(result["sources"]) == 2

    assert "15 days" in mock_llm.received_prompt
    assert "5 leave days" in mock_llm.received_prompt


def test_answer_generator_handles_empty_context():

    mock_llm = MockGroqClient()

    generator = MultiSourceAnswerGenerator(
        groq_client=mock_llm
    )

    result = generator.generate_answer(
        question="What is the leave policy?",
        fused_context={
            "context": "",
            "sources": []
        }
    )

    assert "could not find" in result["answer"].lower()
    assert result["sources"] == []

    # LLM should not be called for empty context
    assert mock_llm.received_prompt is None


def test_answer_generator_rejects_empty_question():

    generator = MultiSourceAnswerGenerator(
        groq_client=MockGroqClient()
    )

    with pytest.raises(ValueError):
        generator.generate_answer(
            question="",
            fused_context={
                "context": "Some information",
                "sources": []
            }
        )
