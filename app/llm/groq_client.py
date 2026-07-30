import os

from dotenv import load_dotenv
from groq import Groq
from app.config.settings import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

load_dotenv()


class GroqClient:
    """
    Handles communication with the Groq API.
    """

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables."
            )

        self.client = Groq(api_key=api_key)

        self.model = LLM_MODEL

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )

        return response.choices[0].message.content