from app.sources.document_source import DocumentSource

source = DocumentSource()

query = "Give me an overview of Toyota."

results = source.retrieve(query)

print("\nRetrieved document chunks:", len(results))

for chunk in results[:3]:
    print("\nDocument:", chunk.get("document_name"))
    print("Page:", chunk.get("page_number"))
    print("Content:", chunk.get("text", "")[:300])