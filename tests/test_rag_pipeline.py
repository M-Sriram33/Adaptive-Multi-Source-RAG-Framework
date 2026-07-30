from app.pipeline.rag_pipeline import RAGPipeline

rag = RAGPipeline()

question = input("Ask a question: ")

result = rag.answer_question(question)

print("=" * 80)
print("ANSWER")
print("=" * 80)

print(result["answer"])

print("\n")

print("=" * 80)
print("SOURCES")
print("=" * 80)

for i, source in enumerate(result["sources"], start=1):
    print(f"{i}. {source['document']} (Page {source['page']})")