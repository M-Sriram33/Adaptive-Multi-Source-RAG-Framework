
from app.retrieval.query_analyzer import QueryAnalyzer

analyzer = QueryAnalyzer()

queries = [
    "Explain Toyota's sustainability strategy",
    "Find the exact phrase Toyota Research Institute",
    "How much does Toyota invest annually in R&D?",
    "Describe Toyota's global operations",
    "Search for Toyota hybrid powertrains"
]

print("\nAdaptive Query Analysis")
print("=" * 70)

for query in queries:
    result = analyzer.analyze(query)

    print(f"\nQuery: {result['query']}")
    print(f"Selected Strategy: {result['strategy']}")
