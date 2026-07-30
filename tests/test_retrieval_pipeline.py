from app.pipeline.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

results = pipeline.retrieve(
    "What is this document about?"
)

for i, chunk in enumerate(results, start=1):

    print("=" * 60)
    print(f"Result {i}")
    print(f"Score : {chunk['score']:.4f}")
    print(f"Page  : {chunk['page_number']}")
    print()
    print(chunk["text"])