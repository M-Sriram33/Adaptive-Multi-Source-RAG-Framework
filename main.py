from fastapi import FastAPI

app = FastAPI(
    title="Adaptive Multi-Source RAG Framework",
    description="Review 1 - PDF RAG Baseline",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Adaptive Multi-Source RAG Framework"
    }