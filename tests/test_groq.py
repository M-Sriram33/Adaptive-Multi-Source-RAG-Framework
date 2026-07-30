from app.llm.groq_client import GroqClient

client = GroqClient()

response = client.generate(
    "Explain Retrieval-Augmented Generation in one sentence."
)

print(response)